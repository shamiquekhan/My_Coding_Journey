# 🌱 Plant Seedlings Classification: Transfer Learning & Data Augmentation

This project implements a deep learning pipeline to classify **12 species of plant seedlings** using **Transfer Learning** and **Data Augmentation** in PyTorch. By leveraging pretrained models like **AlexNet**, we adapt generic visual features to a specialized botanical dataset.

---

## 🌿 Project Overview

In many agricultural and ecological applications, identifying plant species at the **seedling stage** is critical. However, challenges such as small dataset sizes and environmental noise (soil backgrounds, lighting variations) make this task difficult.

This project addresses these challenges through:

* **Transfer Learning**
  Using pretrained ImageNet weights to provide a strong feature-extraction foundation.

* **Data Augmentation**
  Artificially expanding the dataset to improve robustness and generalization.

* **Stratified Subsetting**
  Ensuring class balance while training efficiently on a **25% subset** of the dataset.

---

## 🛠️ Methodology

### 1. Data Augmentation Strategy

To prevent overfitting and improve generalization, an **on-the-fly augmentation pipeline** is used:

* **Spatial Transforms**

  * `RandomResizedCrop`
  * `RandomHorizontalFlip`
  * `RandomVerticalFlip`
    → Simulates different orientations and growth stages

* **Color Jitter**

  * Adjusts brightness, contrast, and saturation
    → Helps the model ignore lighting variations

* **Normalization**

  * Uses ImageNet mean & standard deviation
    → Ensures compatibility with pretrained models

---

### 2. Model Architecture (AlexNet)

We use a pretrained **AlexNet** model with modifications:

* **Frozen Backbone**

  * All convolutional layers are frozen
    → Preserves learned feature representations

* **Custom Classification Head**

  * Final layer replaced with a **12-class output layer**

* **Optimization Strategy**

  * Optimizer: **Adam**
  * Learning Rate Scheduler: **StepLR (step_size=7)**
    → Gradually reduces learning rate for stable training

---

### 3. Evaluation Metrics

To ensure robust evaluation, multiple metrics are used:

* **Top-1 Accuracy**

  * Standard classification accuracy

* **Top-3 Accuracy**

  * Checks if the correct class is within top 3 predictions
    → Useful for visually similar species

* **Confusion Matrix**

  * Highlights misclassifications
    → Example: confusion between *Black-grass* and *Loose Silky-bent*

* **Per-Class Accuracy**

  * Evaluates performance for each species individually

---

## 📂 Project Structure

```text
├── data/                   # Dataset (Train / Validation / Test)
├── src/
│   ├── data_setup.py       # Data loading & augmentation
│   ├── model_builder.py    # Model setup & transfer learning
│   └── engine.py           # Training & evaluation logic
├── notebooks/
│   └── exploration.ipynb   # Visualization & analysis
├── main.py                 # Entry point
└── README.md
```

---

## 🚀 Getting Started

### 📋 Prerequisites

* Python 3.8+
* PyTorch & Torchvision
* Scikit-learn
* Matplotlib & Seaborn

---

### ⚙️ Installation

1. **Clone the repository**

```bash
git clone https://github.com/shamiquekhan/Plant-Seedlings-Data-Prep-CNN-Model
.git
cd Plant-Seedlings-Data-Prep-CNN-Model
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Run the pipeline**

```bash
python main.py
```

---

## 📈 Results & Key Takeaways

* ✅ **Significant accuracy improvement** using transfer learning vs training from scratch
* ⚡ **Faster convergence** due to pretrained weights
* 🌍 **Better generalization** with data augmentation
* 🎯 Model focuses on **leaf structure and texture** instead of background noise

---

## 🧠 Learnings

* Transfer learning is highly effective for **small datasets**
* Data augmentation is crucial for **real-world robustness**
* Freezing layers reduces **overfitting and compute cost**
* Multi-metric evaluation provides **deeper insights**

---

## 🔮 Future Improvements

* Fine-tune deeper layers of AlexNet
* Experiment with:

  * ResNet
  * EfficientNet
* Use the full dataset instead of a subset
* Implement class balancing techniques
* Deploy as a web/mobile application

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a new branch
3. Submit a pull request

---

## 📜 License

This project is licensed under the **MIT License**.

---

## 👤 Author

**Shamique Khan**
📧 [shamiquekhan18@gmail.com](mailto:shamiquekhan18@gmail.com)

---

⭐ If you found this project useful, consider giving it a star!
