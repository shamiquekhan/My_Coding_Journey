import os
import random
from collections import defaultdict
from torch.utils.data import DataLoader, Subset
from torchvision import datasets, transforms

def get_loaders(train_dir, val_dir, test_dir, batch_size=16, img_size=224):
    # ImageNet stats for normalization
    IMAGENET_MEAN = [0.485, 0.456, 0.406]
    IMAGENET_STD = [0.229, 0.224, 0.225]

    # Advanced Augmentation Pipeline
    train_transform = transforms.Compose([
        transforms.RandomResizedCrop(img_size, scale=(0.7, 1.0)),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomVerticalFlip(p=0.5),
        transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.02),
        transforms.ToTensor(),
        transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
    ])

    val_test_transform = transforms.Compose([
        transforms.Resize((img_size, img_size)),
        transforms.ToTensor(),
        transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
    ])

    # Load Full Datasets
    full_train_ds = datasets.ImageFolder(train_dir, transform=train_transform)
    val_ds = datasets.ImageFolder(val_dir, transform=val_test_transform)
    test_ds = datasets.ImageFolder(test_dir, transform=val_test_transform)

    # Stratified 25% Subset Logic
    class_indices = defaultdict(list)
    for idx, (_, lbl) in enumerate(full_train_ds):
        class_indices[lbl].append(idx)

    subset_indices = []
    for lbl, indices in class_indices.items():
        k = max(1, int(len(indices) * 0.25)) # 25% fraction
        subset_indices.extend(random.sample(indices, k))

    train_subset = Subset(full_train_ds, subset_indices)

    # DataLoaders
    train_loader = DataLoader(train_subset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False)
    test_loader = DataLoader(test_ds, batch_size=batch_size, shuffle=False)

    return train_loader, val_loader, test_loader, full_train_ds.classes
