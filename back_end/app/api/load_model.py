import torch
from app.api.model import CNNModel

def load_model(checkpoint_path: str, device: torch.device):
    # Instantiate the model
    model = CNNModel()
    
    # Load the checkpoint
    checkpoint = torch.load(checkpoint_path, map_location=device)
    
    # Load model state
    model.load_state_dict(checkpoint)
    
    # Set the model to evaluation mode
    model.eval()
    
    return model
