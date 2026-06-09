# MLP Classifier Project

A self-contained PyTorch project that trains a multilayer perceptron (MLP) on the built-in Breast Cancer Wisconsin dataset from scikit-learn. The project is designed to be easy to run, easy to extend, and suitable as a reusable starter repo for future deep learning experiments.

## What this project does

- Loads a binary classification dataset without requiring any external data files.
- Standardizes input features with `StandardScaler`.
- Trains a small MLP using PyTorch.
- Evaluates the model with accuracy, classification report, and confusion matrix.
- Saves the trained model and metrics into an `artifacts/` directory.

## Why this repo is useful

This repo gives you a clean baseline for binary classification work. You can use it as a starting point for:

- learning how a feedforward neural network is built in PyTorch,
- testing GPU availability on a new machine,
- comparing different hidden layer sizes and learning rates,
- adding new datasets later without changing the overall project structure.

## Project structure

```text
mlp-classifier-project/
├─ project.py
└─ README.md
```

## Requirements

Install these Python packages:

- `torch`
- `numpy`
- `scikit-learn`

If you want to use a virtual environment, create one first:

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install torch numpy scikit-learn
```

## How to run

From the repository folder:

```powershell
python project.py
```

You can also tune the main training settings:

```powershell
python project.py --epochs 100 --batch-size 64 --lr 0.0005 --hidden-1 64 --hidden-2 32
```

## Expected output

When the script finishes, it will create:

- `artifacts/mlp_breast_cancer.pt` for the trained model weights
- `artifacts/metrics.json` for training history and evaluation results

The console will print:

- the selected device (`cuda` if available, otherwise `cpu`),
- training loss and accuracy for each epoch,
- test accuracy,
- the confusion matrix.

## Model details

The default model is a simple MLP with:

- input layer matching the number of dataset features,
- two hidden layers with ReLU activations,
- a single output neuron for binary classification,
- `BCEWithLogitsLoss` for stable training.

## Evaluation details

The script evaluates the model using:

- accuracy,
- `classification_report` from scikit-learn,
- confusion matrix.

## Notes for reuse in other projects

If you want to adapt this repo for another dataset, the main places to change are:

1. `build_dataloaders()` in `project.py`, where the dataset is loaded and split.
2. `MLPClassifier`, where the layer sizes can be adjusted.
3. The command-line arguments in `main()`, where you can expose new training settings.
