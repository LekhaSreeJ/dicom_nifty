import os
import torch
import SimpleITK as sitk
from torch.utils.data import Dataset, DataLoader

class PEPDataset(Dataset):
    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.samples = []
        # Unga 5 brain cases categories
        self.classes = ['X1_Normal', 'X2_Stroke', 'X3_MS', 'X4_Mets', 'X5_GBM']
        
        for idx, cls in enumerate(self.classes):
            cls_path = os.path.join(root_dir, cls, "images")
            if os.path.exists(cls_path):
                for f in os.listdir(cls_path):
                    if f.endswith('.nii.gz'):
                        self.samples.append((os.path.join(cls_path, f), idx))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        path, label = self.samples[idx]
        img = sitk.ReadImage(path)
        img_array = sitk.GetArrayFromImage(img)
        # 3D CNN-ku [Channel, Depth, Height, Width] format venum
        tensor = torch.from_numpy(img_array).unsqueeze(0).float()
        return tensor, label