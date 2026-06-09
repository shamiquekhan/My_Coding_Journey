import os
import copy
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader, random_split
from torch.optim import lr_scheduler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# -----------------------------
# 1. Configuration
# -----------------------------
CONFIG = {
    "batch_size": 32,
    "num_epochs": 10,
    "learning_rate": 1e-4,
    "data_path": "./data",
    "model_save_path": "best_pet_model.pth",
    "val_split": 0.2,
    "num_workers": 2,
    "device": "cuda" if torch.cuda.is_available() else "cpu",
}

# -----------------------------
# 2. Data Preparation
# -----------------------------
def get_dataloaders():
    train_transform = transforms.Compose([
        transforms.RandomResizedCrop(224),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(15),
        transforms.ColorJitter(brightness=0.2, contrast=0.2),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406],
                             [0.229, 0.224, 0.225]),
    ])

    test_transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406],
                             [0.229, 0.224, 0.225]),
    ])

    full_train_dataset = datasets.OxfordIIITPet(
        root=CONFIG["data_path"],
        split="trainval",
        target_types="category",
        download=True,
        transform=train_transform
    )

    test_dataset = datasets.OxfordIIITPet(
        root=CONFIG["data_path"],
        split="test",
        target_types="category",
        download=True,
        transform=test_transform
    )

    num_train = len(full_train_dataset)
    num_val = int(CONFIG["val_split"] * num_train)
    num_train_final = num_train - num_val

    train_dataset, val_dataset = random_split(
        full_train_dataset,
        [num_train_final, num_val],
        generator=torch.Generator().manual_seed(42)
    )

    # Use test-style transform for validation
    val_dataset.dataset = copy.deepcopy(full_train_dataset)
    val_dataset.dataset.transform = test_transform

    train_loader = DataLoader(
        train_dataset,
        batch_size=CONFIG["batch_size"],
        shuffle=True,
        num_workers=CONFIG["num_workers"],
        pin_memory=True if CONFIG["device"] == "cuda" else False
    )

    val_loader = DataLoader(
        val_dataset,
        batch_size=CONFIG["batch_size"],
        shuffle=False,
        num_workers=CONFIG["num_workers"],
        pin_memory=True if CONFIG["device"] == "cuda" else False
    )

    test_loader = DataLoader(
        test_dataset,
        batch_size=CONFIG["batch_size"],
        shuffle=False,
        num_workers=CONFIG["num_workers"],
        pin_memory=True if CONFIG["device"] == "cuda" else False
    )

    return train_loader, val_loader, test_loader, full_train_dataset.classes

# -----------------------------
# 3. Model Architecture
# -----------------------------
def get_transfer_model(num_classes):
    weights = models.ResNet50_Weights.DEFAULT
    model = models.resnet50(weights=weights)

    # Freeze backbone
    for param in model.parameters():
        param.requires_grad = False

    # Replace final classifier
    num_ftrs = model.fc.in_features
    model.fc = nn.Sequential(
        nn.Linear(num_ftrs, 512),
        nn.ReLU(),
        nn.Dropout(0.4),
        nn.Linear(512, num_classes)
    )
    return model

# -----------------------------
# 4. Training / Validation
# -----------------------------
def train_one_epoch(model, dataloader, criterion, optimizer, device):
    model.train()
    running_loss = 0.0
    running_corrects = 0
    total_samples = 0

    for inputs, labels in dataloader:
        inputs, labels = inputs.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        _, preds = torch.max(outputs, 1)
        running_loss += loss.item() * inputs.size(0)
        running_corrects += torch.sum(preds == labels).item()
        total_samples += inputs.size(0)

    epoch_loss = running_loss / total_samples
    epoch_acc = running_corrects / total_samples
    return epoch_loss, epoch_acc

def evaluate(model, dataloader, criterion, device):
    model.eval()
    running_loss = 0.0
    running_corrects = 0
    total_samples = 0

    all_preds = []
    all_labels = []

    with torch.no_grad():
        for inputs, labels in dataloader:
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = model(inputs)
            loss = criterion(outputs, labels)

            _, preds = torch.max(outputs, 1)
            running_loss += loss.item() * inputs.size(0)
            running_corrects += torch.sum(preds == labels).item()
            total_samples += inputs.size(0)

            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())

    epoch_loss = running_loss / total_samples
    epoch_acc = running_corrects / total_samples
    return epoch_loss, epoch_acc, np.array(all_preds), np.array(all_labels)

# -----------------------------
# 5. Main Pipeline
# -----------------------------
def run_complete_pipeline():
    print(f"Using device: {CONFIG['device']}")
    train_loader, val_loader, test_loader, classes = get_dataloaders()

    model = get_transfer_model(num_classes=len(classes)).to(CONFIG["device"])

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.fc.parameters(), lr=CONFIG["learning_rate"])
    scheduler = lr_scheduler.ReduceLROnPlateau(
        optimizer, mode="min", factor=0.1, patience=2
    )

    best_model_wts = copy.deepcopy(model.state_dict())
    best_val_acc = 0.0

    print("\n--- Training Phase ---")
    for epoch in range(CONFIG["num_epochs"]):
        train_loss, train_acc = train_one_epoch(
            model, train_loader, criterion, optimizer, CONFIG["device"]
        )
        val_loss, val_acc, _, _ = evaluate(
            model, val_loader, criterion, CONFIG["device"]
        )

        scheduler.step(val_loss)

        print(
            f"Epoch [{epoch+1}/{CONFIG['num_epochs']}] "
            f"Train Loss: {train_loss:.4f} Train Acc: {train_acc:.4f} | "
            f"Val Loss: {val_loss:.4f} Val Acc: {val_acc:.4f}"
        )

        if val_acc > best_val_acc:
            best_val_acc = val_acc
            best_model_wts = copy.deepcopy(model.state_dict())
            torch.save(model.state_dict(), CONFIG["model_save_path"])
            print(f"Saved best model to {CONFIG['model_save_path']}")

    print(f"\nBest Validation Accuracy: {best_val_acc:.4f}")

    # Load best weights
    model.load_state_dict(best_model_wts)

    print("\n--- Test Phase ---")
    test_loss, test_acc, preds, labels = evaluate(
        model, test_loader, criterion, CONFIG["device"]
    )
    print(f"Test Loss: {test_loss:.4f}")
    print(f"Test Accuracy: {test_acc:.4f}")

    # Report
    print("\nClassification Report:\n")
    print(classification_report(labels, preds, target_names=classes, zero_division=0))

    # Confusion matrix
    cm = confusion_matrix(labels, preds)
    plt.figure(figsize=(14, 12))
    sns.heatmap(cm, cmap="Reds", xticklabels=classes, yticklabels=classes)
    plt.title("Confusion Matrix: Oxford-IIIT Pets")
    plt.xlabel("Predicted")
    plt.ylabel("True")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_complete_pipeline()
