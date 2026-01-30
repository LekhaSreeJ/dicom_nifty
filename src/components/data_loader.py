import os
import torch
import SimpleITK as sitk
from torch.utils.data import Dataset

class PEPDataset(Dataset):
    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.samples = []
        # Unga 5 brain cases folders
        self.classes = ['X1_Normal', 'X2_Stroke', 'X3_MS', 'X4_Mets', 'X5_GBM']
        
        for idx, cls in enumerate(self.classes):
            img_path = os.path.join(root_dir, cls, "images")
            if os.path.exists(img_path):
                for f in os.listdir(img_path):
                    if f.endswith('.nii.gz'):
                        self.samples.append((os.path.join(img_path, f), idx))
        
        if len(self.samples) == 0:
            raise Exception(f"Data folder-la MRI files illai bro! Path check pannunga: {root_dir}")

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        path, label = self.samples[idx]
        # Reading 3D NIfTI
        img = sitk.ReadImage(path)
        img_array = sitk.GetArrayFromImage(img) # Shape: (D, H, W)
        
        # PyTorch 3D CNN needs (C, D, H, W)
        tensor = torch.from_numpy(img_array).unsqueeze(0).float()
        
        # Normalize to 0-1 (Important for convergence)
        tensor = (tensor - tensor.min()) / (tensor.max() - tensor.min() + 1e-8)
        
        return tensor, label