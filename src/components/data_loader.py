import os
import torch
import SimpleITK as sitk
from torch.utils.data import Dataset
import torchvision.transforms as T

class PEPBinaryDataset(Dataset):
    def __init__(self, root_dir, target_class, is_train=True):
        self.root_dir = root_dir
        self.target_class = target_class
        self.samples = []
        
        # Iterating through 5 classes (Normal, Stroke, etc.)
        for cls in os.listdir(root_dir):
            cls_path = os.path.join(root_dir, cls)
            if not os.path.isdir(cls_path):
                continue
            
            label = 1 if cls == target_class else 0
            
            # Entering the 'images' folder inside each class
            images_dir = os.path.join(cls_path, "images")
            
            if os.path.exists(images_dir):
                for img_name in os.listdir(images_dir):
                    if img_name.endswith(('.nii', '.nii.gz')):
                        img_path = os.path.join(images_dir, img_name)
                        self.samples.append((img_path, label))
            else:
                # Oru velai Normal folder-la direct-ah files irundha (safety check)
                for img_name in os.listdir(cls_path):
                    if img_name.endswith(('.nii', '.nii.gz')):
                        img_path = os.path.join(cls_path, img_name)
                        self.samples.append((img_path, label))

        self.heavy_transform = T.Compose([
            T.RandomRotation(degrees=10),
            T.GaussianBlur(kernel_size=3)
        ])
        self.is_train = is_train

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        path, label = self.samples[idx]
        img = sitk.GetArrayFromImage(sitk.ReadImage(path))
        img = torch.tensor(img).float().unsqueeze(0)

        # Minority class augmentation (Stroke, Infection, etc.)
        if self.is_train and label == 1:
            # Applying 2D transform to 3D slices
            img = self.heavy_transform(img)

        return img, label