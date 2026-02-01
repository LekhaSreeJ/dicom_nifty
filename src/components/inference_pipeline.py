import torch
import SimpleITK as sitk
import numpy as np
from src.components.model_trainer import PEPNet3D

class PEPInference:
    def __init__(self, model_dir="models/"):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.classes = ['normal', 'stroke', 'tumor', 'ms', 'infection']
        self.models = {}

        # 5 binary models-aiyum load panrom
        for cls in self.classes:
            model = PEPNet3D(num_classes=1).to(self.device)
            model_path = f"{model_dir}pep_binary_{cls}.pth"
            model.load_state_dict(torch.load(model_path, map_location=self.device))
            model.eval()
            self.models[cls] = model

    def predict(self, nifty_path):
        # 1. Image Preprocessing
        img = sitk.GetArrayFromImage(sitk.ReadImage(nifty_path))
        img_tensor = torch.tensor(img).float().unsqueeze(0).unsqueeze(0).to(self.device)

        probabilities = {}
        
        # 2. Get probabilities from all models
        with torch.no_grad():
            for cls, model in self.models.items():
                output = model(img_tensor)
                prob = torch.sigmoid(output).item()
                probabilities[cls] = prob

        # 3. Probability Elimination Logic (If-Else)
        if probabilities['normal'] > 0.80:
            final_pred = "Normal"
        else:
            # Normal illana, bakki irukura 4-la edhu high probability-nu paarkanum
            remaining = {k: v for k, v in probabilities.items() if k != 'normal'}
            final_pred = max(remaining, key=remaining.get).capitalize()

        return final_pred, probabilities