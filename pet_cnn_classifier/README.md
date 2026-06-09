# Oxford-IIIT Pet Classification using Transfer Learning (ResNet50)

## Project Overview

This project is a deep learning image classification pipeline built with PyTorch for classifying pet breeds from the Oxford-IIIT Pet Dataset.

It uses:

* Transfer Learning with pretrained ResNet50
* Advanced Data Augmentation
* Validation Split
* Learning Rate Scheduling
* Model Checkpoint Saving
* Full Evaluation Metrics
* Confusion Matrix Visualization

The model classifies images into **37 pet categories** (cats and dogs).

---

# Features

## Data Processing

* Downloads Oxford-IIIT Pet Dataset automatically
* Train / Validation / Test split
* Data augmentation:

  * RandomResizedCrop
  * Horizontal Flip
  * Rotation
  * ColorJitter
* Image normalization using ImageNet statistics

## Model

* Pretrained ResNet50 backbone
* Frozen convolutional layers
* Custom classifier head:

  * Linear Layer
  * ReLU
  * Dropout
  * Output Layer (37 classes)

## Training

* Adam Optimizer
* CrossEntropyLoss
* ReduceLROnPlateau Scheduler
* Best model checkpoint saving

## Evaluation

* Test Accuracy
* Classification Report
* Confusion Matrix

---

# Folder Structure

```bash
pet-classification-project/
│
├── pet_classifier.py          # Main training and evaluation script
├── requirements.txt           # Required dependencies
├── best_pet_model.pth         # Saved best model (generated after training)
├── data/                      # Dataset download folder
└── README.md                  # Project documentation
```

---

# Installation Guide

## Step 1: Clone or Download Project

```bash
git clone <your-repo-link>
cd pet-classification-project
```

OR manually download the files.

---

## Step 2: Create Virtual Environment (Recommended)

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Mac/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

---

# requirements.txt

```txt
torch
torchvision
scikit-learn
matplotlib
seaborn
numpy
```

---

# Running the Project

```bash
python pet_classifier.py
```

---

# Training Workflow

## Stage 1: Dataset Download

The Oxford-IIIT Pet dataset is automatically downloaded into:

```bash
./data
```

---

## Stage 2: Training

The model trains for:

```python
num_epochs = 10
```

During training:

* Training loss
* Training accuracy
* Validation loss
* Validation accuracy

are displayed.

---

## Stage 3: Best Model Saving

Best performing model:

```bash
best_pet_model.pth
```

---

## Stage 4: Evaluation

Outputs:

* Final Test Accuracy
* Classification Report
* Confusion Matrix

---

# Example Output

```bash
Using device: cuda

Epoch [1/10] Train Loss: 1.2456 Train Acc: 0.6732 | Val Loss: 0.9321 Val Acc: 0.7543
Epoch [2/10] Train Loss: 0.8452 Train Acc: 0.7821 | Val Loss: 0.7124 Val Acc: 0.8245

Best Validation Accuracy: 0.9124

--- Test Phase ---
Test Accuracy: 0.9012
```

---

# Hyperparameters

```python
batch_size = 32
learning_rate = 1e-4
num_epochs = 10
val_split = 0.2
optimizer = Adam
scheduler = ReduceLROnPlateau
```

---

# Customization Options

## Change Epochs

```python
"num_epochs": 20
```

## Change Batch Size

```python
"batch_size": 64
```

## Fine-Tune Entire ResNet

Unfreeze layers:

```python
for param in model.parameters():
    param.requires_grad = True
```

---

# Performance Tips

## For Better Accuracy:

* Increase epochs to 20–30
* Unfreeze deeper ResNet layers
* Use ResNet101 or EfficientNet
* Add EarlyStopping
* Use Mixed Precision Training (AMP)

## For Faster Training:

* Reduce image size
* Use smaller batch size
* Use GPU

---

# Common Errors and Fixes

## CUDA Out of Memory

Solution:

```python
"batch_size": 16
```

---

## Dataset Download Issues

Solution:
Check internet connection or manually download Oxford-IIIT Pet dataset.

---

## Module Not Found

Solution:

```bash
pip install -r requirements.txt
```

---

# Future Improvements

* EfficientNetB3/B4
* MobileNet for lightweight deployment
* Flask/Streamlit web app
* Real-time pet breed prediction
* Grad-CAM visualization

---

# Deployment Ideas

* Web App
* Mobile App
* Veterinary assistant
* Smart pet adoption platforms

---

# Learning Outcomes

This project teaches:

* Transfer Learning
* CNN Fine-Tuning
* PyTorch Pipelines
* Data Augmentation
* Evaluation Metrics
* Model Deployment Basics

---

# Author

Built by Shamique Khan

---

# License

This project is open-source for educational and research purposes.

---

## Quick Start

```bash
pip install -r requirements.txt
python pet_classifier.py
```
