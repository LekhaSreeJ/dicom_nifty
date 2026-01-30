import mlflow
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from src.components.model_trainer import PEPNet3D
from src.components.data_loader import PEPDataset

mlflow.set_tracking_uri("sqlite:///pep_tracking.db")
mlflow.set_experiment("PEP_Final_Experiment")

def run_training():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # 1. Load Data
    train_dataset = PEPDataset(root_dir="data/processed")
    train_loader = DataLoader(train_dataset, batch_size=2, shuffle=True) # Batch 2 for 1650 4GB RAM
    
    # 2. Initialize Model
    model = PEPNet3D(num_classes=5).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    with mlflow.start_run(run_name="GTX_1650_Real_Epoch_1"):
        mlflow.log_param("batch_size", 2)
        mlflow.log_param("lr", 0.001)
        
        model.train()
        total_loss = 0
        
        print(f"Starting Training on {len(train_dataset)} MRI scans...")
        
        for batch_idx, (data, target) in enumerate(train_loader):
            data, target = data.to(device), target.to(device)
            
            optimizer.zero_grad()
            output = model(data)
            loss = criterion(output, target)
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
            
            if batch_idx % 5 == 0:
                print(f"Batch {batch_idx}: Loss {loss.item():.4f}")
                mlflow.log_metric("batch_loss", loss.item(), step=batch_idx)

        avg_loss = total_loss / len(train_loader)
        mlflow.log_metric("avg_epoch_loss", avg_loss)
        print(f"Training Complete! Avg Loss: {avg_loss:.4f}")

if __name__ == "__main__":
    run_training()