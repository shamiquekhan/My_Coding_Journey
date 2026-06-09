"""Train a simple multilayer perceptron on the breast cancer dataset.

This script is self-contained and does not require any local dataset files.
It loads the built-in Breast Cancer Wisconsin dataset from scikit-learn,
standardizes the features, trains a small PyTorch MLP, and writes the
trained weights plus metrics to an output directory.
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
from sklearn.datasets import load_breast_cancer
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from torch.utils.data import DataLoader, TensorDataset


class MLPClassifier(nn.Module):
    def __init__(self, input_dim: int, hidden_dim_1: int = 32, hidden_dim_2: int = 16):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, hidden_dim_1),
            nn.ReLU(),
            nn.Linear(hidden_dim_1, hidden_dim_2),
            nn.ReLU(),
            nn.Linear(hidden_dim_2, 1),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.network(x)


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


def build_dataloaders(batch_size: int, seed: int):
    data = load_breast_cancer()
    features = data.data
    targets = data.target.astype(np.float32).reshape(-1, 1)

    x_train, x_test, y_train, y_test = train_test_split(
        features,
        targets,
        test_size=0.2,
        random_state=seed,
        stratify=targets,
    )

    scaler = StandardScaler()
    x_train = scaler.fit_transform(x_train)
    x_test = scaler.transform(x_test)

    x_train_tensor = torch.tensor(x_train, dtype=torch.float32)
    y_train_tensor = torch.tensor(y_train, dtype=torch.float32)
    x_test_tensor = torch.tensor(x_test, dtype=torch.float32)
    y_test_tensor = torch.tensor(y_test, dtype=torch.float32)

    train_dataset = TensorDataset(x_train_tensor, y_train_tensor)
    test_dataset = TensorDataset(x_test_tensor, y_test_tensor)

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

    return data, scaler, train_loader, test_loader, (x_test_tensor, y_test_tensor)


def train_model(model: nn.Module, train_loader: DataLoader, epochs: int, lr: float, device: torch.device):
    loss_fn = nn.BCEWithLogitsLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    history = []

    for epoch in range(1, epochs + 1):
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0

        for batch_x, batch_y in train_loader:
            batch_x = batch_x.to(device)
            batch_y = batch_y.to(device)

            optimizer.zero_grad()
            logits = model(batch_x)
            loss = loss_fn(logits, batch_y)
            loss.backward()
            optimizer.step()

            running_loss += loss.item() * batch_x.size(0)
            predictions = (torch.sigmoid(logits) >= 0.5).float()
            correct += (predictions == batch_y).sum().item()
            total += batch_x.size(0)

        epoch_loss = running_loss / total
        epoch_acc = correct / total
        history.append({"epoch": epoch, "train_loss": epoch_loss, "train_accuracy": epoch_acc})
        print(f"Epoch {epoch:03d} | loss={epoch_loss:.4f} | acc={epoch_acc:.4f}")

    return history


def evaluate_model(model: nn.Module, test_loader: DataLoader, device: torch.device):
    model.eval()
    probabilities = []
    targets = []

    with torch.no_grad():
        for batch_x, batch_y in test_loader:
            batch_x = batch_x.to(device)
            logits = model(batch_x)
            probs = torch.sigmoid(logits).cpu().numpy().ravel()
            probabilities.extend(probs.tolist())
            targets.extend(batch_y.numpy().ravel().tolist())

    predictions = [1 if prob >= 0.5 else 0 for prob in probabilities]
    accuracy = accuracy_score(targets, predictions)
    report = classification_report(targets, predictions, target_names=["malignant", "benign"], output_dict=True)
    matrix = confusion_matrix(targets, predictions).tolist()

    return {
        "accuracy": accuracy,
        "classification_report": report,
        "confusion_matrix": matrix,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Train a multilayer perceptron classifier on breast cancer data.")
    parser.add_argument("--epochs", type=int, default=50, help="Number of training epochs.")
    parser.add_argument("--batch-size", type=int, default=32, help="Training batch size.")
    parser.add_argument("--lr", type=float, default=0.001, help="Learning rate.")
    parser.add_argument("--hidden-1", type=int, default=32, help="First hidden layer width.")
    parser.add_argument("--hidden-2", type=int, default=16, help="Second hidden layer width.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed.")
    parser.add_argument("--output-dir", type=Path, default=Path("artifacts"), help="Directory for saved outputs.")
    args = parser.parse_args()

    set_seed(args.seed)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    data, _, train_loader, test_loader, _ = build_dataloaders(args.batch_size, args.seed)
    model = MLPClassifier(
        input_dim=data.data.shape[1],
        hidden_dim_1=args.hidden_1,
        hidden_dim_2=args.hidden_2,
    ).to(device)

    history = train_model(model, train_loader, args.epochs, args.lr, device)
    metrics = evaluate_model(model, test_loader, device)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    model_path = args.output_dir / "mlp_breast_cancer.pt"
    metrics_path = args.output_dir / "metrics.json"

    torch.save(model.state_dict(), model_path)
    with metrics_path.open("w", encoding="utf-8") as f:
        json.dump({"history": history, "evaluation": metrics}, f, indent=2)

    print(f"\nSaved model to: {model_path}")
    print(f"Saved metrics to: {metrics_path}")
    print(f"Test accuracy: {metrics['accuracy']:.4f}")
    print("Confusion matrix:")
    for row in metrics["confusion_matrix"]:
        print(row)


if __name__ == "__main__":
    main()
