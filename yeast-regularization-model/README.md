# Yeast Protein Localization — Regularization Study

## Overview

This project implements and compares multiple **regularization techniques** on a multiclass classification problem using the Yeast dataset. The goal is to analyze how different strategies affect generalization performance in a Feedforward Neural Network (FNN).

## Objectives

* Build a baseline neural network (no regularization)
* Apply and evaluate:

  * Dropout
  * L2 Regularization (Weight Decay)
  * Combined Dropout + L2
* Compare models using:

  * Test Accuracy
  * Macro F1 Score
* Visualize training dynamics and overfitting behavior

## Models Compared

| Model | Description       |
| ----- | ----------------- |
| M1    | No Regularization |
| M2    | Dropout           |
| M3    | L2 Regularization |
| M4    | Dropout + L2      |

## Tech Stack

* Python
* PyTorch
* NumPy
* Pandas
* Scikit-learn
* Matplotlib

## Project Structure

```
.
├── yeast_regularization_project.py
├── yeast.csv
├── outputs/
│   ├── regularization_loss_comparison.png
│   ├── validation_loss_overlay.png
│   ├── confusion_matrix_*.png
│   ├── *.pth
│   ├── test_performance_summary.csv
│   └── class_names.json
└── README.md
```

## Dataset

* Input: Numerical protein features
* Output: Protein localization site (multiclass classification)

Ensure the dataset file is named:

```
yeast.csv
```

and contains a target column:

```
localization_site
```

## Installation

Install dependencies:

```bash
pip install torch numpy pandas scikit-learn matplotlib
```

## How to Run

```bash
python yeast_regularization_project.py --data yeast.csv
```

### Optional Arguments

| Argument         | Description               | Default |
| ---------------- | ------------------------- | ------- |
| `--epochs`       | Number of training epochs | 1000    |
| `--batch-size`   | Batch size                | 32      |
| `--hidden-dim`   | Hidden layer size         | 32      |
| `--lr`           | Learning rate             | 0.01    |
| `--weight-decay` | L2 strength               | 1e-4    |
| `--dropout`      | Dropout rate              | 0.5     |
| `--output-dir`   | Output directory          | outputs |

Example:

```bash
python yeast_regularization_project.py --epochs 500 --dropout 0.3
```

## Outputs

The script generates:

### 1. Loss Curves

* Training vs Validation loss for each model

### 2. Validation Comparison Plot

* Overlay of validation loss across models

### 3. Confusion Matrices

* One per model

### 4. Model Checkpoints

* Saved as `.pth` files

### 5. Performance Table

Saved as:

```
outputs/test_performance_summary.csv
```

Example:

| Model             | Test Accuracy | Macro F1 Score |
| ----------------- | ------------- | -------------- |
| No Reg (M1)       | 0.58          | 0.52           |
| Dropout (M2)      | 0.61          | 0.56           |
| L2 (M3)           | 0.60          | 0.55           |
| Dropout + L2 (M4) | 0.64          | 0.59           |

## Key Insights

* Dropout helps reduce overfitting by randomly deactivating neurons
* L2 regularization penalizes large weights, improving generalization
* Combining both often yields the best performance

## Reproducibility

* Fixed random seed ensures consistent results
* Deterministic PyTorch settings enabled

## Future Improvements

* Add early stopping
* Hyperparameter tuning (Grid Search / Bayesian)
* Try deeper architectures
* Add cross-validation
* Deploy as a web app (Streamlit)

## License

This project is open-source and free to use for academic purposes.

## Author

Developed as part of a machine learning coursework project focused on neural network regularization.
