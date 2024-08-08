# app/model/model.py

import torch
import torch.nn as nn
import torch.nn.functional as F

class CNNModel(nn.Module):
    def __init__(self):
        super(CNNModel, self).__init__()
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=32, kernel_size=3, stride=1, padding=1)  # 96x96x1 -> 96x96x32
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2, padding=0)  # Halves the spatial dimensions
        
        self.conv2 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, stride=1, padding=1)  # 48x48x32 -> 48x48x64
        self.conv3 = nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3, stride=1, padding=1)  # 24x24x64 -> 24x24x128
        self.conv4 = nn.Conv2d(in_channels=128, out_channels=256, kernel_size=3, stride=1, padding=1)  # 12x12x128 -> 12x12x256
        
        self.global_avg_pool = nn.AdaptiveAvgPool2d(1)  # Output size is 1x1x256
        
        self.fc1 = nn.Linear(256, 512)  # Fully connected layer
        self.fc2 = nn.Linear(512, 256)
        self.fc3 = nn.Linear(256, 600)  # Output size, e.g., number of classes
        
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.relu(self.conv1(x))
        x = self.pool(x)  # 96x96x1 -> 48x48x32
        
        x = self.relu(self.conv2(x))
        x = self.pool(x)  # 48x48x32 -> 24x24x64
        
        x = self.relu(self.conv3(x))
        x = self.pool(x)  # 24x24x64 -> 12x12x128
        
        x = self.relu(self.conv4(x))
        x = self.pool(x)  # 12x12x128 -> 6x6x256
        
        x = self.global_avg_pool(x)  # 6x6x256 -> 1x1x256
        x = torch.flatten(x, 1)  # Flatten the tensor, starting from dimension 1
        
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.fc3(x)
        
        return x

    def extract_features(self, x):
        x = self.relu(self.conv1(x))
        x = self.pool(x)
        
        x = self.relu(self.conv2(x))
        x = self.pool(x)
        
        x = self.relu(self.conv3(x))
        x = self.pool(x)
        
        x = self.relu(self.conv4(x))
        x = self.pool(x)
        
        x = self.global_avg_pool(x)
        x = torch.flatten(x, 1)
        
        return x
