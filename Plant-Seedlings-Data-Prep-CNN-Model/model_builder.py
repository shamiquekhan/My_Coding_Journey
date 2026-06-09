import torch.nn as nn
from torchvision import models

def build_alexnet(num_classes=12):
    # Load pretrained AlexNet
    model = models.alexnet(weights=models.AlexNet_Weights.IMAGENET1K_V1)

    # Freeze all parameters to prevent updating pretrained weights
    for p in model.parameters():
        p.requires_grad = False

    # Replace the final linear layer (index 6)
    in_feats = model.classifier[6].in_features
    model.classifier[6] = nn.Linear(in_feats, num_classes)
    
    return model
