import torch
import SimpleITK as sitk
import numpy as np
import os
# Fix: Relative import for package recognition
from .model_trainer import PEPNet3D

class PEPInference:
    def __init__(self, model_dir="models/"):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.classes = ['normal', 'stroke', 'tumor', 'ms', 'infection']
        self.models = {}

        # 5 binary models load logic
        for cls in self.classes:
            model = PEPNet3D(num_classes=1).to(self.device)
            # Safe path joining
            model_path = os.path.join(model_dir, f"pep_binary_{cls}.pth")
            
            if os.path.exists(model_path):
                model.load_state_dict(torch.load(model_path, map_location=self.device))
                model.eval()
                self.models[cls] = model
            else:
                print(f"Warning: {model_path} missing!")

    def predict(self, nifty_path):
        # 1. Image Preprocessing
        sitk_img = sitk.ReadImage(nifty_path)
        img = sitk.GetArrayFromImage(sitk_img)
        
        # Simple Normalization (Very Important for Medical AI)
        img = (img - np.mean(img)) / (np.std(img) + 1e-8)
        
        # 2. Resize/Crop logic (Ensure it matches your model's input size)
        # If your model trained on 64x64x64, you must resize here. 
        # For now, converting to tensor:
        img_tensor = torch.tensor(img).float().unsqueeze(0).unsqueeze(0).to(self.device)

        probabilities = {}
        
        # 3. Get probabilities
        with torch.no_grad():
            for cls, model in self.models.items():
                output = model(img_tensor)
                prob = torch.sigmoid(output).item()
                probabilities[cls] = prob

        # 4. PEP Elimination Logic
        if probabilities.get('normal', 0) > 0.80:
            final_pred = "Normal"
        else:
            remaining = {k: v for k, v in probabilities.items() if k != 'normal'}
            final_pred = max(remaining, key=remaining.get).capitalize()

        return final_pred, probabilities
