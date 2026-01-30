import mlflow
import torch
from src.components.model_trainer import PEPNet3D

def run_training():
    mlflow.set_experiment("PEP_Brain_Classification")
    
    with mlflow.start_run(run_name="GTX_1650_First_Run"):
        # Params log panradhu
        mlflow.log_param("model_type", "3D_CNN")
        mlflow.log_param("batch_size", 2)
        
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model = PEPNet3D().to(device)
        
        # Inga dhaan namma training loop varum
        # Ippodhikku dummy metric log pannuvom work aagudha-nu paaka
        mlflow.log_metric("initial_loss", 0.69)
        
        print("Training stage initiated on GPU!")
        
if __name__ == "__main__":
    run_training()