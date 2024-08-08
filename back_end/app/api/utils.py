import torch
import torch.nn.functional as F

def compute_similarity(feature1, feature2):
    # Cosine similarity
    cos_sim = F.cosine_similarity(feature1, feature2)
    return cos_sim