import torch
from tqdm import tqdm
from sklearn.metrics import confusion_matrix

def train_one_epoch(model, loader, optimizer, criterion, device):
    model.train()
    tr_loss, tr_correct, tr_total = 0.0, 0, 0
    for xb, yb in tqdm(loader, desc="Training"):
        xb, yb = xb.to(device), yb.to(device)
        optimizer.zero_grad()
        logits = model(xb)
        loss = criterion(logits, yb)
        loss.backward()
        optimizer.step()
        
        tr_loss += loss.item() * xb.size(0)
        tr_correct += (logits.argmax(1) == yb).sum().item()
        tr_total += yb.size(0)
    return tr_loss / tr_total, tr_correct / tr_total

def evaluate_metrics(model, loader, device, k=3):
    model.eval()
    y_true, y_pred = [], []
    correct_k, total = 0, 0
    
    with torch.no_grad():
        for xb, yb in loader:
            xb, yb = xb.to(device), yb.to(device)
            logits = model(xb)
            
            # Top-1 Predictions
            preds = logits.argmax(1)
            y_true.extend(yb.cpu().tolist())
            y_pred.extend(preds.cpu().tolist())
            
            # Top-k Accuracy Logic[cite: 2]
            _, topk_idx = logits.topk(k, dim=1)
            match = topk_idx.eq(yb.view(-1, 1).expand_as(topk_idx))
            correct_k += match.sum().item()
            total += yb.size(0)
            
    cm = confusion_matrix(y_true, y_pred)
    top1_acc = (torch.tensor(y_true) == torch.tensor(y_pred)).float().mean().item()
    topk_acc = correct_k / total
    
    return top1_acc, topk_acc, cm
