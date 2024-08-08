import torch
import torch.nn.functional as F
import numpy as np
from PIL import Image
import io
import base64

def compute_similarity(feature1, feature2):
    # Cosine similarity
    cos_sim = F.cosine_similarity(feature1, feature2)
    return cos_sim

def preprocess_image(image_data: bytes) -> np.ndarray:
    try:
        image_file = io.BytesIO(image_data)
        image = Image.open(image_file).convert("L")
        resized_img = image.resize((96, 96))
        np_array = np.array(resized_img, dtype=np.float32)
        np_array = np.expand_dims(np_array, axis=0)  # Add channel dimension
        np_array /= 255.0
        return np_array
    except Exception as e:
        raise ValueError(f"Failed to preprocess image: {e}")

def base64_to_image(base64_data: str) -> np.ndarray:
    try:
        image_bytes = base64.b64decode(base64_data)
        image_file = io.BytesIO(image_bytes)
        image = Image.open(image_file).convert("L")
        resized_img = image.resize((96, 96))
        np_array = np.array(resized_img, dtype=np.float32)
        np_array = np.expand_dims(np_array, axis=0)  # Add channel dimension
        np_array /= 255.0
        return np_array
    except Exception as e:
        raise ValueError(f"Failed to decode base64 data: {e}")