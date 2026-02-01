import mlflow
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from src.components.model_trainer import PEPNet3D
from src.components.data_loader import PEPBinaryDataset # New binary loader import

mlflow.set_tracking_uri("sqlite:///pep_tracking.db")
mlflow.set_experiment("PEP_Binary_Elimination_Pipeline")

def run_binary_factory():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # Namma pipeline-la irukura 5 classes
    classes = ['Normal', 'Stroke', 'Tumor', 'MS', 'Infection']
    
    for target_disease in classes:
        # Ovvoru disease-kum oru separate MLflow run
        with mlflow.start_run(run_name=f"Binary_Model_{target_disease}"):
            print(f"\n--- Training Binary Model for: {target_disease} ---")
            
            # 1. Load Data (Binary Mode)
            # Imbalance handle panna targeted augmentation inga trigger aagum
            train_dataset = PEPBinaryDataset(root_dir="data\processed", target_class=target_disease, is_train=True)
            train_loader = DataLoader(train_dataset, batch_size=2, shuffle=True)
            
            # 2. Initialize Model (Binary Output: num_classes=1)
            # Binary classification-ku 1 output node dhaan thevai
            model = PEPNet3D(num_classes=1).to(device) 
            
            # BCEWithLogitsLoss is best for Binary Classification
            criterion = nn.BCEWithLogitsLoss() 
            optimizer = optim.Adam(model.parameters(), lr=0.001)

            mlflow.log_param("target_class", target_disease)
            mlflow.log_param("batch_size", 2)
            mlflow.log_param("loss_function", "BCEWithLogitsLoss")

            model.train()
            total_loss = 0
            
            for batch_idx, (data, target) in enumerate(train_loader):
                # Target-ah float format-ku mathanum for BCE Loss
                data, target = data.to(device), target.to(device).float().unsqueeze(1)
                
                optimizer.zero_grad()
                output = model(data)
                loss = criterion(output, target)
                loss.backward()
                optimizer.step()
                
                total_loss += loss.item()
                
                if batch_idx % 2 == 0: # Metrics log
                    mlflow.log_metric("batch_loss", loss.item(), step=batch_idx)

            avg_loss = total_loss / len(train_loader)
            mlflow.log_metric("avg_model_loss", avg_loss)
            
            # Model-ah save pannanum, appo dhaan frontend-la load panna mudiyum
            model_path = f"models/pep_binary_{target_disease.lower()}.pth"
            torch.save(model.state_dict(), model_path)
            mlflow.log_artifact(model_path)
            
            print(f"Finished: {target_disease} | Avg Loss: {avg_loss:.4f}")

if __name__ == "__main__":
    run_binary_factory()