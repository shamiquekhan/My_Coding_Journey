const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, HeadingLevel, LevelFormat,
  BorderStyle, WidthType, ShadingType, VerticalAlign,
  PageNumber, PageBreak, TabStopType, TabStopPosition
} = require('docx');
const fs = require('fs');

// ─── Colour Palette ───────────────────────────────────────────────────────────
const BLUE_DARK   = "1F4E79";
const BLUE_MID    = "2E75B6";
const BLUE_LIGHT  = "D6E8F7";
const BLUE_XLIGHT = "EEF5FC";
const TEAL        = "00838F";
const TEAL_LIGHT  = "E0F4F5";
const ORANGE      = "E65100";
const ORANGE_LIGHT= "FFF3E0";
const GREY_TEXT   = "444444";
const GREY_LIGHT  = "F5F5F5";
const WHITE       = "FFFFFF";
const GREEN_DARK  = "1B5E20";
const GREEN_LIGHT = "E8F5E9";

// ─── Border helpers ───────────────────────────────────────────────────────────
const cell_border = (color="CCCCCC") => ({
  top:    { style: BorderStyle.SINGLE, size: 1, color },
  bottom: { style: BorderStyle.SINGLE, size: 1, color },
  left:   { style: BorderStyle.SINGLE, size: 1, color },
  right:  { style: BorderStyle.SINGLE, size: 1, color },
});
const no_border = () => ({
  top:    { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
  bottom: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
  left:   { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
  right:  { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
});

// ─── Helper: plain paragraph ──────────────────────────────────────────────────
const p = (text, opts={}) => new Paragraph({
  children: [new TextRun({
    text,
    font: "Arial",
    size: opts.size || 22,
    bold: opts.bold || false,
    italics: opts.italic || false,
    color: opts.color || GREY_TEXT,
  })],
  spacing: { before: opts.spaceBefore || 80, after: opts.spaceAfter || 80 },
  alignment: opts.align || AlignmentType.LEFT,
});

// ─── Helper: heading paragraph ────────────────────────────────────────────────
const h1 = (text) => new Paragraph({
  heading: HeadingLevel.HEADING_1,
  children: [new TextRun({ text, font: "Arial", size: 36, bold: true, color: WHITE })],
  spacing: { before: 320, after: 200 },
  shading: { fill: BLUE_DARK, type: ShadingType.CLEAR },
  indent: { left: 240, right: 240 },
});

const h2 = (text) => new Paragraph({
  heading: HeadingLevel.HEADING_2,
  children: [new TextRun({ text, font: "Arial", size: 28, bold: true, color: BLUE_DARK })],
  spacing: { before: 280, after: 140 },
  border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: BLUE_MID, space: 2 } },
});

const h3 = (text) => new Paragraph({
  heading: HeadingLevel.HEADING_3,
  children: [new TextRun({ text, font: "Arial", size: 24, bold: true, color: TEAL })],
  spacing: { before: 200, after: 100 },
});

// ─── Helper: code block ───────────────────────────────────────────────────────
const code_block = (lines) => {
  const border_style = { style: BorderStyle.SINGLE, size: 1, color: "BBBBBB" };
  return lines.map((line, i) => new Paragraph({
    children: [new TextRun({
      text: line === "" ? " " : line,
      font: "Courier New",
      size: 18,
      color: "1A1A2E",
    })],
    spacing: { before: i === 0 ? 0 : 0, after: 0 },
    indent: { left: 200 },
    shading: { fill: "F8F8F8", type: ShadingType.CLEAR },
    border: {
      top:    i === 0 ? border_style : { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
      bottom: i === lines.length-1 ? border_style : { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
      left:   { style: BorderStyle.THICK, size: 6, color: BLUE_MID },
      right:  border_style,
    },
  }));
};

// ─── Helper: info box ─────────────────────────────────────────────────────────
const info_box = (lines, fill=BLUE_XLIGHT, textColor=BLUE_DARK) =>
  new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [9360],
    rows: [new TableRow({ children: [new TableCell({
      borders: cell_border(BLUE_MID),
      width: { size: 9360, type: WidthType.DXA },
      shading: { fill, type: ShadingType.CLEAR },
      margins: { top: 120, bottom: 120, left: 200, right: 200 },
      children: lines.map(ln => new Paragraph({
        children: [new TextRun({ text: ln, font: "Arial", size: 20, color: textColor,
          bold: ln.startsWith("✅") || ln.startsWith("📌") || ln.startsWith("💡") || ln.startsWith("🎯") })],
        spacing: { before: 40, after: 40 },
      })),
    })]})],
  });

// ─── Helper: two-column table ─────────────────────────────────────────────────
const two_col_table = (rows, col1W=3000, col2W=6360, headerFill=BLUE_DARK) => {
  const total = col1W + col2W;
  return new Table({
    width: { size: total, type: WidthType.DXA },
    columnWidths: [col1W, col2W],
    rows: rows.map((row, ri) => new TableRow({
      children: row.map((cell, ci) => new TableCell({
        borders: cell_border(),
        width: { size: ci === 0 ? col1W : col2W, type: WidthType.DXA },
        shading: { fill: ri === 0 ? headerFill : (ri % 2 === 0 ? GREY_LIGHT : WHITE), type: ShadingType.CLEAR },
        margins: { top: 80, bottom: 80, left: 120, right: 120 },
        children: [new Paragraph({ children: [new TextRun({
          text: cell, font: "Arial", size: 20,
          bold: ri === 0, color: ri === 0 ? WHITE : GREY_TEXT,
        })], spacing: { before: 40, after: 40 } })],
      })),
    })),
  });
};

// ─── Helper: bullet ───────────────────────────────────────────────────────────
const bullet = (text, level=0, color=GREY_TEXT) => new Paragraph({
  numbering: { reference: "bullets", level },
  children: [new TextRun({ text, font: "Arial", size: 21, color })],
  spacing: { before: 40, after: 40 },
});

// ─── Helper: spacer ───────────────────────────────────────────────────────────
const spacer = (h=120) => new Paragraph({ children: [new TextRun("")], spacing: { before: h, after: 0 } });

// ─── Helper: formula ─────────────────────────────────────────────────────────
const formula = (text) => new Paragraph({
  children: [new TextRun({ text, font: "Courier New", size: 22, color: BLUE_DARK, bold: true })],
  alignment: AlignmentType.CENTER,
  spacing: { before: 100, after: 100 },
  shading: { fill: BLUE_XLIGHT, type: ShadingType.CLEAR },
  border: { left: { style: BorderStyle.THICK, size: 8, color: BLUE_MID } },
  indent: { left: 400, right: 400 },
});

// ═══════════════════════════════════════════════════════════════════════════════
//  DOCUMENT CONTENT
// ═══════════════════════════════════════════════════════════════════════════════

const children = [];

// ─── COVER PAGE ───────────────────────────────────────────────────────────────
children.push(
  new Paragraph({
    children: [new TextRun({ text: " ", size: 24 })],
    spacing: { before: 1440, after: 0 },
  }),
  new Paragraph({
    children: [new TextRun({
      text: "MULTILAYER PERCEPTRONS", font: "Arial", size: 64, bold: true, color: WHITE,
    })],
    alignment: AlignmentType.CENTER,
    shading: { fill: BLUE_DARK, type: ShadingType.CLEAR },
    spacing: { before: 240, after: 0 },
    border: { top: { style: BorderStyle.SINGLE, size: 8, color: BLUE_MID } },
    indent: { left: 0, right: 0 },
  }),
  new Paragraph({
    children: [new TextRun({
      text: "Forward Pass  ·  Backpropagation  ·  PyTorch Training",
      font: "Arial", size: 28, color: BLUE_LIGHT, italics: true,
    })],
    alignment: AlignmentType.CENTER,
    shading: { fill: BLUE_DARK, type: ShadingType.CLEAR },
    spacing: { before: 0, after: 0 },
    indent: { left: 0, right: 0 },
  }),
  new Paragraph({
    children: [new TextRun({ text: " ", size: 24 })],
    shading: { fill: BLUE_DARK, type: ShadingType.CLEAR },
    spacing: { before: 0, after: 0 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: BLUE_MID } },
  }),
  spacer(400),
  new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [3120, 3120, 3120],
    rows: [new TableRow({ children: [
      ["Notebook 2.2", "Notebook 2.3", "Notebook 2.4"].map((title, ci) =>
        new TableCell({
          borders: cell_border(BLUE_MID),
          width: { size: 3120, type: WidthType.DXA },
          shading: { fill: ci === 0 ? BLUE_MID : (ci === 1 ? TEAL : ORANGE), type: ShadingType.CLEAR },
          margins: { top: 160, bottom: 160, left: 200, right: 200 },
          children: [
            new Paragraph({ children: [new TextRun({ text: title, font: "Arial", size: 22, bold: true, color: WHITE })],
              alignment: AlignmentType.CENTER, spacing: { before: 40, after: 40 } }),
            new Paragraph({ children: [new TextRun({ text:
              ci === 0 ? "MLP Deep Dive" : (ci === 1 ? "Backpropagation" : "PyTorch MLP"),
              font: "Arial", size: 20, color: WHITE })],
              alignment: AlignmentType.CENTER, spacing: { before: 20, after: 40 } }),
          ],
        })
      ),
    ]})],
  }),
  spacer(600),
  new Paragraph({
    children: [new TextRun({ text: "Course: CSA2001  ·  Deep Learning Fundamentals", font: "Arial", size: 22, color: GREY_TEXT })],
    alignment: AlignmentType.CENTER,
    spacing: { before: 80, after: 40 },
  }),
  new Paragraph({
    children: [new TextRun({ text: "Project Report — Compiled Reference", font: "Arial", size: 22, color: GREY_TEXT })],
    alignment: AlignmentType.CENTER,
    spacing: { before: 40, after: 80 },
  }),
  new Paragraph({ children: [new PageBreak()] }),
);

// ─── SECTION 0: OVERVIEW TABLE ────────────────────────────────────────────────
children.push(
  h1("📋  Project Overview"),
  spacer(),
  p("This document consolidates all three notebooks of the Multilayer Perceptron module into a single structured reference. It covers theoretical foundations, mathematical derivations, NumPy implementations, and full PyTorch training pipelines.", { size: 22 }),
  spacer(160),
  two_col_table([
    ["Notebook", "Topics Covered"],
    ["2.2 — MLP Deep Dive", "FNN structure, forward pass in NumPy & PyTorch, activation functions, hidden layer visualisation, heart disease demo"],
    ["2.3 — Backpropagation", "Gradient derivation, chain rule, manual backward pass in NumPy, SGD training loop, loss curve"],
    ["2.4 — MLPs with PyTorch", "Dataset prep, nn.Sequential, BCELoss, Adam optimiser, training loop, confusion matrix"],
  ], 3000, 6360),
  spacer(200),
  info_box([
    "💡  Learning Objectives",
    "",
    "✅  Understand the architecture of a feedforward neural network",
    "✅  Implement forward and backward passes from scratch",
    "✅  Apply the chain rule to derive parameter gradients",
    "✅  Train a binary classifier using PyTorch on real medical data",
    "✅  Evaluate model performance with loss curves and confusion matrices",
  ]),
  new Paragraph({ children: [new PageBreak()] }),
);

// ─── SECTION 1: MLP ARCHITECTURE ─────────────────────────────────────────────
children.push(
  h1("🧠  Section 1: Feedforward Neural Networks"),
  spacer(),
  h2("1.1  What is a Feedforward Neural Network?"),
  p("A Feedforward Neural Network (FNN) extends the single-neuron Perceptron by stacking multiple neurons into layers, enabling non-linear transformations that can model complex patterns."),
  spacer(80),
  two_col_table([
    ["Property", "Description"],
    ["Perceptron", "Single neuron — linear decision boundary only"],
    ["FNN / MLP", "Multiple stacked layers — can learn non-linear boundaries"],
    ["Hidden Layers", "Intermediate feature transformers between input and output"],
    ["Activation Function", "Introduces non-linearity (ReLU, Sigmoid, Tanh, …)"],
    ["Universal Approx.", "One hidden layer with enough neurons can approximate any continuous function"],
  ], 2800, 6560),
  spacer(160),

  h2("1.2  Network Architecture"),
  p("A simple two-layer FNN with a 2-feature input, 3 hidden neurons, and 1 output:"),
  spacer(80),
  ...code_block([
    "Input x  (1 × 2)",
    "    │",
    "    ▼  z₁ = x @ W₁ + b₁          W₁ ∈ R(2×3)",
    "    │",
    "    ▼  h  = φ(z₁)                 φ = ReLU or Sigmoid",
    "    │",
    "    ▼  ŷ  = h @ W₂ + b₂          W₂ ∈ R(3×1)",
    "    │",
    "   Output ŷ  (1 × 1)",
  ]),
  spacer(160),

  h2("1.3  Shape Intuition"),
  two_col_table([
    ["Tensor", "Shape", "Description"],
    ["x",  "(1 × 2)",  "Input: 1 sample, 2 features"],
    ["W₁", "(2 × 3)",  "Weights: 2 inputs → 3 hidden neurons"],
    ["b₁", "(1 × 3)",  "Bias vector for hidden layer"],
    ["h",  "(1 × 3)",  "Hidden activations"],
    ["W₂", "(3 × 1)",  "Weights: 3 hidden → 1 output"],
    ["ŷ",  "(1 × 1)",  "Scalar prediction"],
  ].map(r => r), 1800, ...([2000, 5560])),
  spacer(200),

  h2("1.4  Forward Pass — NumPy Implementation"),
  p("The manual forward pass using only NumPy:"),
  spacer(80),
  ...code_block([
    "import numpy as np",
    "",
    "np.random.seed(42)",
    "x  = np.array([[1.5, -0.5]])   # shape (1, 2)",
    "W1 = np.random.randn(2, 3)",
    "b1 = np.random.randn(1, 3)",
    "W2 = np.random.randn(3, 1)",
    "b2 = np.random.randn(1, 1)",
    "",
    "def relu(z):    return np.maximum(0, z)",
    "def sigmoid(z): return 1 / (1 + np.exp(-z))",
    "",
    "# Forward pass",
    "z1    = np.dot(x, W1) + b1    # hidden pre-activation  (1, 3)",
    "h     = relu(z1)               # hidden activation       (1, 3)",
    "y_hat = np.dot(h, W2) + b2    # output prediction       (1, 1)",
    "",
    "print('Hidden:', h)",
    "print('Prediction:', y_hat)",
  ]),
  spacer(200),

  h2("1.5  Why Non-Linearity Matters"),
  p("Without activation functions, stacking linear layers collapses to a single linear transformation, regardless of depth:"),
  spacer(80),
  formula("h = x W₁ + b₁  →  ŷ = h W₂ + b₂  =  x(W₁W₂) + (b₁W₂ + b₂)"),
  spacer(80),
  p("The product W₁W₂ is still just one matrix — the network has no additional expressive power."),
  spacer(80),
  two_col_table([
    ["Activation", "Formula", "Key Property"],
    ["ReLU",    "max(0, z)",          "Sparse, fast, default choice for hidden layers"],
    ["Sigmoid", "1 / (1 + e^-z)",     "Output in (0,1) — used for binary classification output"],
    ["LeakyReLU", "max(0.01z, z)",    "Prevents dying ReLU problem with small negative slope"],
    ["Tanh",    "(e^z - e^-z)/(e^z + e^-z)", "Output in (-1,1), zero-centred"],
  ], 1600, ...([1800, 5960])),
  spacer(160),

  h2("1.6  Forward Pass — PyTorch (No Autograd)"),
  spacer(80),
  ...code_block([
    "import torch",
    "",
    "x_torch = torch.tensor([[1.5, -0.5]], dtype=torch.float32)",
    "",
    "torch.manual_seed(0)",
    "W1_t = torch.randn(2, 3)",
    "b1_t = torch.randn(1, 3)",
    "W2_t = torch.randn(3, 1)",
    "b2_t = torch.randn(1, 1)",
    "",
    "def relu(z): return torch.maximum(z, torch.tensor(0.0))",
    "",
    "# Forward pass",
    "z1_t   = x_torch @ W1_t + b1_t",
    "h_t    = relu(z1_t)",
    "y_hat_t = h_t @ W2_t + b2_t",
    "",
    "print('Prediction:', y_hat_t.item())",
  ]),
  new Paragraph({ children: [new PageBreak()] }),
);

// ─── SECTION 2: BACKPROPAGATION ───────────────────────────────────────────────
children.push(
  h1("⬅️  Section 2: Backpropagation"),
  spacer(),
  h2("2.1  Why Backpropagation?"),
  p("Backpropagation is the algorithm used to compute gradients of the loss with respect to every parameter in the network. These gradients guide the weight updates that make the network learn."),
  spacer(80),
  info_box([
    "📌  Gradient Descent Update Rule",
    "",
    "    θ  ←  θ  −  η · ∂L/∂θ",
    "",
    "  θ  = parameter (weight or bias)",
    "  η  = learning rate (small positive scalar)",
    "  ∂L/∂θ = gradient of loss w.r.t. that parameter",
  ], BLUE_XLIGHT, BLUE_DARK),
  spacer(160),

  h2("2.2  Notation Guide"),
  two_col_table([
    ["Symbol", "Meaning"],
    ["x",          "Input vector"],
    ["z₁ = xW₁+b₁","Hidden layer pre-activation (linear output)"],
    ["h = φ(z₁)",  "Hidden layer post-activation"],
    ["z₂ = hW₂+b₂","Output layer pre-activation"],
    ["ŷ = σ(z₂)",  "Final prediction after sigmoid"],
    ["L",           "Loss comparing ŷ to true label y"],
  ], 2000, 7360),
  spacer(160),

  h2("2.3  Loss Functions"),
  p("Choosing the right loss function depends on the task:"),
  spacer(80),
  two_col_table([
    ["Loss Function", "Use When", "Formula"],
    ["MSE  (Mean Squared Error)", "Regression — continuous targets", "L = ½(ŷ − y)²"],
    ["Binary Cross-Entropy",      "Binary classification (0/1 labels)", "L = −[y log ŷ + (1−y) log(1−ŷ)]"],
    ["Categorical Cross-Entropy", "Multi-class classification",        "L = −Σ yₖ log ŷₖ"],
  ], 2500, ...([2500, 4360])),
  spacer(160),

  h2("2.4  Chain Rule Derivation (ReLU + MSE)"),
  p("For the network  x → z₁ → h=ReLU(z₁) → ŷ=hW₂+b₂ → L=½(ŷ−y)²:"),
  spacer(80),
  ...["Step 1:  ∂L/∂ŷ   =  ŷ − y",
      "Step 2:  ∂L/∂W₂  =  hᵀ · (ŷ − y)          shape: (hidden × 1)",
      "Step 3:  ∂L/∂b₂  =  ŷ − y                   shape: (1 × 1)",
      "Step 4:  ∂L/∂h   =  (ŷ − y) · W₂ᵀ          shape: (1 × hidden)",
      "Step 5:  ∂L/∂z₁  =  ∂L/∂h  ⊙  ReLU'(z₁)   (element-wise)",
      "Step 6:  ∂L/∂W₁  =  xᵀ · ∂L/∂z₁            shape: (input × hidden)",
      "Step 7:  ∂L/∂b₁  =  ∂L/∂z₁                  shape: (1 × hidden)",
  ].map(f => formula(f)),
  spacer(160),

  h2("2.5  Manual Backward Pass — NumPy"),
  spacer(80),
  ...code_block([
    "# ── Forward ──────────────────────────────────────────",
    "z1    = x @ W1 + b1",
    "h     = relu(z1)",
    "y_hat = h @ W2 + b2",
    "loss  = 0.5 * (y_hat - y)**2",
    "",
    "# ── Backward ─────────────────────────────────────────",
    "dL_dyhat = y_hat - y                      # (1,1)",
    "",
    "# Output layer",
    "dL_dW2   = h.T @ dL_dyhat                 # (3,1)",
    "dL_db2   = dL_dyhat                       # (1,1)",
    "",
    "# Hidden layer",
    "dL_dh    = dL_dyhat @ W2.T                # (1,3)",
    "dL_dz1   = dL_dh * (z1 > 0).astype(float)# (1,3)  ReLU'",
    "dL_dW1   = x.T @ dL_dz1                  # (2,3)",
    "dL_db1   = dL_dz1                         # (1,3)",
    "",
    "# ── Parameter Update (SGD) ──────────────────────────",
    "lr = 0.01",
    "W2 -= lr * dL_dW2;  b2 -= lr * dL_db2",
    "W1 -= lr * dL_dW1;  b1 -= lr * dL_db1",
  ]),
  spacer(200),

  h2("2.6  Full Training Loop"),
  spacer(80),
  ...code_block([
    "np.random.seed(42)",
    "lr, epochs = 0.1, 200",
    "losses = []",
    "",
    "for epoch in range(epochs):",
    "    # Forward",
    "    z1 = x @ W1 + b1",
    "    h  = relu(z1)",
    "    y_hat = h @ W2 + b2",
    "    loss = 0.5 * (y_hat - y)**2",
    "    losses.append(loss.item())",
    "",
    "    # Backward",
    "    dL_dyhat = y_hat - y",
    "    dL_dW2 = h.T @ dL_dyhat",
    "    dL_db2 = dL_dyhat",
    "    dL_dh  = dL_dyhat @ W2.T",
    "    dL_dz1 = dL_dh * (z1 > 0).astype(float)",
    "    dL_dW1 = x.T @ dL_dz1",
    "    dL_db1 = dL_dz1",
    "",
    "    # Update",
    "    W2 -= lr*dL_dW2; b2 -= lr*dL_db2",
    "    W1 -= lr*dL_dW1; b1 -= lr*dL_db1",
  ]),
  new Paragraph({ children: [new PageBreak()] }),
);

// ─── SECTION 3: PYTORCH ───────────────────────────────────────────────────────
children.push(
  h1("🔥  Section 3: MLPs with PyTorch"),
  spacer(),
  h2("3.1  Manual vs. PyTorch — What Changes?"),
  two_col_table([
    ["Task", "Manual (Notebooks 2.2–2.3)", "PyTorch (Notebook 2.4)"],
    ["Model definition", "Write W, b, forward() yourself", "nn.Sequential / nn.Module"],
    ["Gradient computation", "Derive + code chain rule by hand", "loss.backward() — autograd"],
    ["Weight update", "θ -= lr * grad (your code)", "optimizer.step()"],
    ["Loss function", "MSE coded manually", "nn.BCELoss / BCEWithLogitsLoss"],
    ["Batch ops / efficiency", "Manual loops", "Tensor ops, GPU-ready"],
  ], 2200, ...([3000, 4160])),
  spacer(160),

  h2("3.2  Dataset Preparation (Heart Disease)"),
  p("The UCI Heart Disease dataset has 13 input features and a target column num (0–4). We binarise it:"),
  spacer(80),
  ...code_block([
    "import pandas as pd",
    "from sklearn.preprocessing import StandardScaler",
    "from sklearn.model_selection import train_test_split",
    "import torch",
    "",
    "df = pd.read_csv('heart.csv').dropna()",
    "df['target'] = (df['num'] > 0).astype(int)   # binary: 0 or 1",
    "",
    "X = df.drop(columns=['num', 'target'])",
    "y = df['target']",
    "",
    "# Standardise: mean=0, std=1",
    "scaler   = StandardScaler()",
    "X_scaled = scaler.fit_transform(X)",
    "",
    "# Convert to tensors",
    "X_tensor = torch.tensor(X_scaled, dtype=torch.float32)",
    "y_tensor = torch.tensor(y.values, dtype=torch.float32).view(-1, 1)",
    "",
    "# 80/20 split",
    "X_train, X_test, y_train, y_test = train_test_split(",
    "    X_tensor, y_tensor, test_size=0.2, random_state=42)",
  ]),
  spacer(160),

  h2("3.3  Model Definition — nn.Sequential"),
  spacer(80),
  ...code_block([
    "import torch.nn as nn",
    "",
    "# Simple 2-layer FNN (13 → 16 → 1)",
    "model = nn.Sequential(",
    "    nn.Linear(13, 16),   # Input → Hidden (13 features, 16 neurons)",
    "    nn.ReLU(),            # Activation",
    "    nn.Linear(16, 1),    # Hidden → Output",
    "    nn.Sigmoid()          # Probability output for binary classification",
    ")",
    "",
    "# Custom 3-layer FNN (code task 2.4.3.1)",
    "custom_model = nn.Sequential(",
    "    nn.Linear(13, 32),",
    "    nn.LeakyReLU(),",
    "    nn.Linear(32, 16),",
    "    nn.Sigmoid(),",
    "    nn.Linear(16, 1),",
    "    nn.Sigmoid()",
    ")",
    "",
    "# Count parameters",
    "print(sum(p.numel() for p in model.parameters()))  # 241",
  ]),
  spacer(160),

  h2("3.4  Loss Function & Optimizer"),
  spacer(80),
  info_box([
    "📌  BCELoss vs BCEWithLogitsLoss",
    "",
    "  BCELoss               → expects model output to already be a probability (after Sigmoid)",
    "  BCEWithLogitsLoss     → applies Sigmoid internally; more numerically stable",
    "",
    "  Rule of thumb: if your last layer has nn.Sigmoid() → use BCELoss",
    "                 if your last layer is nn.Linear()   → use BCEWithLogitsLoss",
  ], ORANGE_LIGHT, ORANGE),
  spacer(120),
  ...code_block([
    "import torch.optim as optim",
    "",
    "loss_fn   = nn.BCELoss()                         # Binary Cross-Entropy",
    "optimizer = optim.Adam(model.parameters(), lr=0.01)  # Adam: adaptive lr",
  ]),
  spacer(160),

  h2("3.5  Training Loop"),
  spacer(80),
  ...code_block([
    "num_epochs  = 200",
    "train_losses = []",
    "test_losses  = []",
    "",
    "for epoch in range(num_epochs):",
    "    # ── Training ────────────────────────────────────",
    "    model.train()",
    "    outputs = model(X_train)",
    "    loss    = loss_fn(outputs, y_train)",
    "",
    "    optimizer.zero_grad()  # clear gradients from last step",
    "    loss.backward()        # backpropagate",
    "    optimizer.step()       # update weights",
    "    train_losses.append(loss.item())",
    "",
    "    # ── Validation ──────────────────────────────────",
    "    model.eval()",
    "    with torch.no_grad():",
    "        test_out  = model(X_test)",
    "        test_loss = loss_fn(test_out, y_test)",
    "        test_losses.append(test_loss.item())",
    "",
    "    if (epoch + 1) % 10 == 0:",
    "        print(f'Epoch [{epoch+1}/{num_epochs}]  '",
    "              f'Train: {loss.item():.4f}  '",
    "              f'Test: {test_loss.item():.4f}')",
  ]),
  spacer(160),

  h2("3.6  Evaluation — Loss, Accuracy, Confusion Matrix"),
  spacer(80),
  ...code_block([
    "from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay",
    "",
    "model.eval()",
    "with torch.no_grad():",
    "    y_logits = model(X_test)",
    "    y_probs  = torch.sigmoid(y_logits)",
    "    y_preds  = (y_probs >= 0.5).float()        # threshold = 0.5",
    "    test_loss = loss_fn(y_logits, y_test)",
    "",
    "test_acc = accuracy_score(y_test.numpy(), y_preds.numpy())",
    "print(f'Test Loss:     {test_loss.item():.4f}')",
    "print(f'Test Accuracy: {test_acc*100:.2f}%')",
    "",
    "# Confusion matrix",
    "cm   = confusion_matrix(y_test.numpy(), y_preds.numpy())",
    "disp = ConfusionMatrixDisplay(cm, display_labels=['No Disease','Disease'])",
    "disp.plot(cmap='Blues')",
  ]),
  new Paragraph({ children: [new PageBreak()] }),
);

// ─── SECTION 4: CODE TASKS SUMMARY ───────────────────────────────────────────
children.push(
  h1("✅  Section 4: Code Tasks — Solutions"),
  spacer(),

  h2("Task 2.2.2.1 — Manual Forward Pass (NumPy, 2×2 network)"),
  ...code_block([
    "x   = np.array([[1.0, -1.0]])",
    "np.random.seed(42)",
    "W1p = np.random.randn(2, 2)",
    "b1p = np.random.randn(1, 2)",
    "W2p = np.random.randn(2, 1)",
    "b2p = np.random.randn(1, 1)",
    "",
    "def relu(z): return np.maximum(0, z)",
    "",
    "z1p    = x @ W1p + b1p      # hidden pre-activation",
    "h      = relu(z1p)           # hidden activation",
    "y_pred = h @ W2p + b2p       # output   shape: (1, 1)",
  ]),
  spacer(140),

  h2("Task 2.2.4.1 — Manual Forward Pass (PyTorch, 2×4 network)"),
  ...code_block([
    "import torch",
    "x_task = torch.tensor([[0.8, -1.2]], dtype=torch.float32)",
    "torch.manual_seed(42)",
    "W1_task = torch.randn(2, 4)",
    "b1_task = torch.randn(1, 4)",
    "W2_task = torch.randn(4, 1)",
    "b2_task = torch.randn(1, 1)",
    "",
    "def relu(z): return torch.maximum(z, torch.tensor(0.0))",
    "",
    "z1         = x_task @ W1_task + b1_task   # (1,4)",
    "h          = relu(z1)                      # (1,4)",
    "y_hat_task = h @ W2_task + b2_task         # (1,1)",
  ]),
  spacer(140),

  h2("Task 2.2.7.1 — Inference on Heart Disease Data"),
  ...code_block([
    "def relu(z): return np.maximum(0, z)",
    "",
    "z1      = X_real @ W1_real + b1_real",
    "h1      = relu(z1)",
    "logits  = h1 @ W2_real + b2_real",
    "y_preds = (logits.flatten() >= 0).astype(int)    # threshold at 0",
    "",
    "model_accuracy = np.mean(y_preds == y_real)",
    "print('Accuracy:', model_accuracy)",
  ]),
  spacer(140),

  h2("Task 2.3.2.1 — Sigmoid → ReLU Forward Pass"),
  ...code_block([
    "x_custom = np.array([[2.0, -1.0]])",
    "np.random.seed(123)",
    "W1_custom = np.random.randn(2, 4)",
    "b1_custom = np.random.randn(1, 4)",
    "W2_custom = np.random.randn(4, 1)",
    "b2_custom = np.random.randn(1, 1)",
    "",
    "def sigmoid(z): return 1 / (1 + np.exp(-z))",
    "def relu(z):    return np.maximum(0, z)",
    "",
    "z1    = x_custom @ W1_custom + b1_custom   # Linear",
    "h     = sigmoid(z1)                         # Sigmoid hidden",
    "z2    = h @ W2_custom + b2_custom           # Linear",
    "y_out = relu(z2)                            # ReLU output  (1,1)",
  ]),
  spacer(140),

  h2("Task 2.3.4.1 — Manual Backpropagation"),
  ...code_block([
    "np.random.seed(123)",
    "x_custom = np.array([[1.0, 3.0]])",
    "y_custom = np.array([[2.0]])",
    "",
    "# Forward",
    "z1    = x_custom @ W1 + b1",
    "h     = relu(z1)",
    "y_hat = h @ W2 + b2",
    "loss  = 0.5 * (y_hat - y_custom)**2",
    "",
    "# Backward",
    "dL_dyhat = y_hat - y_custom               # (1,1)",
    "dL_dW2   = h.T @ dL_dyhat                 # (3,1)",
    "dL_db2   = dL_dyhat                       # (1,1)",
    "dL_dh    = dL_dyhat @ W2.T               # (1,3)",
    "dL_dz1   = dL_dh * (z1 > 0).astype(float)# (1,3)",
    "dL_dW1   = x_custom.T @ dL_dz1           # (2,3)",
    "dL_db1   = dL_dz1                         # (1,3)",
  ]),
  spacer(140),

  h2("Task 2.4.3.1 — Custom PyTorch Model"),
  ...code_block([
    "custom_model = nn.Sequential(",
    "    nn.Linear(13, 32),    # 13 features → 32 hidden",
    "    nn.LeakyReLU(),",
    "    nn.Linear(32, 16),    # 32 → 16 hidden",
    "    nn.Sigmoid(),",
    "    nn.Linear(16, 1),     # 16 → 1 output",
    "    nn.Sigmoid()          # probability output",
    ")",
    "print(custom_model)",
  ]),
  spacer(140),

  h2("Task 2.4.5.1 — Training Loop with Test Loss"),
  ...code_block([
    "train_losses, test_losses = [], []",
    "",
    "for epoch in range(num_epochs):",
    "    model.train()",
    "    outputs = model(X_train)",
    "    loss    = loss_fn(outputs, y_train)",
    "    optimizer.zero_grad()",
    "    loss.backward()",
    "    optimizer.step()",
    "    train_losses.append(loss.item())",
    "",
    "    model.eval()",
    "    with torch.no_grad():",
    "        test_out  = model(X_test)",
    "        test_loss = loss_fn(test_out, y_test)",
    "    test_losses.append(test_loss.item())",
    "",
    "    if (epoch + 1) % 10 == 0:",
    "        print(f'Epoch [{epoch+1}/{num_epochs}]  '",
    "              f'Train: {loss.item():.4f}  Test: {test_loss.item():.4f}')",
  ]),
  spacer(140),

  h2("Task 2.4.6.1 — Test Set Evaluation"),
  ...code_block([
    "from sklearn.metrics import accuracy_score",
    "",
    "model.eval()",
    "with torch.no_grad():",
    "    y_test_logits = model(X_test)",
    "    y_test_probs  = torch.sigmoid(y_test_logits)",
    "    y_test_preds  = (y_test_probs >= 0.5).float()",
    "    test_loss     = loss_fn(y_test_logits, y_test)",
    "",
    "test_acc = accuracy_score(y_test.numpy(), y_test_preds.numpy())",
    "print(f'Test Loss:     {test_loss.item():.4f}')",
    "print(f'Test Accuracy: {test_acc*100:.2f}%')",
  ]),
  new Paragraph({ children: [new PageBreak()] }),
);

// ─── SECTION 5: KEY CONCEPTS CHEAT SHEET ─────────────────────────────────────
children.push(
  h1("📚  Section 5: Key Concepts Cheat Sheet"),
  spacer(),

  h2("5.1  Activation Functions"),
  two_col_table([
    ["Function", "Formula", "When to Use"],
    ["ReLU",           "max(0, z)",                  "Default for hidden layers in most networks"],
    ["Leaky ReLU",     "max(0.01z, z)",              "When dying ReLU is a concern"],
    ["Sigmoid",        "1/(1+e^-z)",                 "Output layer for binary classification"],
    ["Softmax",        "e^zₖ / Σe^zⱼ",             "Output layer for multi-class classification"],
    ["Tanh",           "(e^z−e^-z)/(e^z+e^-z)",     "Zero-centred; sometimes better than sigmoid"],
    ["Linear / None",  "z",                           "Regression output or before BCEWithLogitsLoss"],
  ], 1800, ...([2200, 5360])),
  spacer(160),

  h2("5.2  Loss Functions"),
  two_col_table([
    ["Loss", "Task", "PyTorch Class"],
    ["MSE",                    "Regression",             "nn.MSELoss()"],
    ["Binary Cross-Entropy",   "Binary classification",  "nn.BCELoss()"],
    ["BCE with Logits",        "Binary (no final sigmoid)", "nn.BCEWithLogitsLoss()"],
    ["Categorical Cross-Entropy", "Multi-class",         "nn.CrossEntropyLoss()"],
  ], 2600, ...([2800, 3960])),
  spacer(160),

  h2("5.3  Optimizers"),
  two_col_table([
    ["Optimizer", "Description", "PyTorch"],
    ["SGD",       "Classic gradient descent — fixed learning rate",    "optim.SGD(model.parameters(), lr=0.01)"],
    ["SGD+Mom.",  "SGD with momentum — smoother convergence",          "optim.SGD(..., momentum=0.9)"],
    ["Adam",      "Adaptive learning rate — best default choice",      "optim.Adam(model.parameters(), lr=0.001)"],
    ["RMSProp",   "Adaptive, good for recurrent nets",                 "optim.RMSprop(...)"],
  ], 1600, ...([2800, 4960])),
  spacer(160),

  h2("5.4  Training vs. Evaluation Mode"),
  info_box([
    "🎯  Always switch modes correctly in PyTorch:",
    "",
    "  model.train()           → Activates Dropout, BatchNorm in training mode",
    "  model.eval()            → Deactivates them for deterministic inference",
    "  torch.no_grad()         → Disables gradient tracking for inference (saves memory)",
    "",
    "  Pattern:  model.eval() + with torch.no_grad(): ... ",
  ], GREEN_LIGHT, GREEN_DARK),
  spacer(160),

  h2("5.5  Gradient Flow Rules"),
  two_col_table([
    ["Rule", "Detail"],
    ["optimizer.zero_grad()", "Must be called before loss.backward() every step — otherwise gradients accumulate"],
    ["loss.backward()",       "Computes ∂L/∂θ for all parameters in the computational graph"],
    ["optimizer.step()",      "Applies the update  θ ← θ − η·∂L/∂θ  using stored gradients"],
    ["ReLU derivative",       "1 if z > 0, else 0  — acts as a gate in backprop"],
    ["Sigmoid derivative",    "σ(z)·(1−σ(z))  — can cause vanishing gradients in deep nets"],
  ], 2800, 6560),
  spacer(160),

  h2("5.6  Confusion Matrix Terminology"),
  two_col_table([
    ["Term", "Definition", "Formula"],
    ["True Positive (TP)",  "Predicted Disease, actually Disease", "—"],
    ["True Negative (TN)",  "Predicted No Disease, actually No Disease", "—"],
    ["False Positive (FP)", "Predicted Disease, actually No Disease  (Type I Error)", "—"],
    ["False Negative (FN)", "Predicted No Disease, actually Disease  (Type II Error)", "—"],
    ["Accuracy",            "Overall correctness",  "(TP+TN)/(TP+TN+FP+FN)"],
    ["Precision",           "Positive prediction quality", "TP/(TP+FP)"],
    ["Recall / Sensitivity","Disease detection rate",      "TP/(TP+FN)"],
    ["F1 Score",            "Harmonic mean of precision and recall", "2·P·R/(P+R)"],
  ], 2400, ...([3000, 3960])),
  spacer(200),

  info_box([
    "💡  Key Takeaways",
    "",
    "  1. Non-linearity is essential — without it, deep networks reduce to a single linear transform.",
    "  2. Backprop = chain rule applied backwards through the computational graph.",
    "  3. Gradient descent moves parameters in the direction that reduces the loss.",
    "  4. PyTorch automates backprop — you only need to call loss.backward().",
    "  5. Always use model.eval() + torch.no_grad() for validation and inference.",
    "  6. BCELoss requires a sigmoid output; BCEWithLogitsLoss does not.",
    "  7. Adam is a safe default optimiser; tune lr if training stalls.",
  ]),
);

// ─── FOOTER ───────────────────────────────────────────────────────────────────
const footer = new Footer({
  children: [new Paragraph({
    children: [
      new TextRun({ text: "MLP Project — CSA2001  |  Page ", font: "Arial", size: 18, color: "888888" }),
      new TextRun({ children: [PageNumber.CURRENT], font: "Arial", size: 18, color: "888888" }),
      new TextRun({ text: " of ", font: "Arial", size: 18, color: "888888" }),
      new TextRun({ children: [PageNumber.TOTAL_PAGES], font: "Arial", size: 18, color: "888888" }),
    ],
    alignment: AlignmentType.CENTER,
    border: { top: { style: BorderStyle.SINGLE, size: 2, color: BLUE_MID } },
    spacing: { before: 80 },
  })],
});

// ─── BUILD DOCUMENT ───────────────────────────────────────────────────────────
const doc = new Document({
  numbering: {
    config: [
      { reference: "bullets",
        levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    ]
  },
  styles: {
    default: { document: { run: { font: "Arial", size: 22 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 36, bold: true, font: "Arial", color: WHITE },
        paragraph: { spacing: { before: 320, after: 200 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 28, bold: true, font: "Arial", color: BLUE_DARK },
        paragraph: { spacing: { before: 280, after: 140 }, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 24, bold: true, font: "Arial", color: TEAL },
        paragraph: { spacing: { before: 200, after: 100 }, outlineLevel: 2 } },
    ]
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 1080, right: 1080, bottom: 1080, left: 1080 },
      },
    },
    footers: { default: footer },
    children,
  }],
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync('/home/claude/MLP_Project_Report.docx', buf);
  console.log('Done: MLP_Project_Report.docx');
});
