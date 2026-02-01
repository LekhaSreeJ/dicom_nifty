from src.components.inference_pipeline import PEPInference
import os

# Initialize Engine
engine = PEPInference(model_dir="models/")

# 5 classes-layum irundhu samples-ah test pannuvom
test_samples = {
    "Normal": "data\processed\X1_Normal\images\OAS1_0001_MR1_normal.nii.gz",
    "Stroke": "data\processed\X2_Stroke\images\sub-strokecase0001_sub-strokecase0001_ses-0001_flair.nii.gz",
    "MS": "data\processed\X3_MS\images\p1_p1_t2_flair.nii.gz",
    "Mets": "data\processed\X4_Mets\images\mets_005_t1_gd.nii.gz",
    "GBM": "data\processed\X5_GBM\images\brats-gli-00005-100-t1c.nii.gz",
}

for actual_cls, path in test_samples.items():
    if os.path.exists(path):
        pred, scores = engine.predict(path)
        print(f"Actual: {actual_cls} | Predicted: {pred}")
        print(f"Full Scores: {scores}\n")
    else:
        print(f"Path missing for {actual_cls}")