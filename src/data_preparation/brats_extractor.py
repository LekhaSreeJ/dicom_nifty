import os
import shutil

# --- CONFIGURATION ---
# Path pointing to the main training data folder
source_root = r"D:\pep_2026\dataset\brats_glioma_class_5\BraTS2024-BraTS-GLI-TrainingData\training_data1_v2"
target_root = r"D:\pep_2026\dataset\brats_glioma_class_5\gbm_extracted_batch_1"

os.makedirs(os.path.join(target_root, 't1c'), exist_ok=True)
os.makedirs(os.path.join(target_root, 'mask'), exist_ok=True)

print("🚀 BraTS 2024 GBM (GLI) Extraction Starting...")

count = 0
limit = 20 # First 20 cases for 'Rare Class' representation

# Sort and get patient folders (BraTS-GLI-00000-000...)
patient_folders = sorted([f for f in os.listdir(source_root) if os.path.isdir(os.path.join(source_root, f))])

for patient_folder in patient_folders:
    if count >= limit:
        break
        
    patient_path = os.path.join(source_root, patient_folder)
    
    # In BraTS 2024, files are named: <Folder-Name>-t1c.nii.gz and <Folder-Name>-seg.nii.gz
    t1c_file = f"{patient_folder}-t1c.nii.gz"
    seg_file = f"{patient_folder}-seg.nii.gz"
    
    t1c_src = os.path.join(patient_path, t1c_file)
    seg_src = os.path.join(patient_path, seg_file)
    
    if os.path.exists(t1c_src) and os.path.exists(seg_src):
        shutil.copy2(t1c_src, os.path.join(target_root, 't1c', t1c_file))
        shutil.copy2(seg_src, os.path.join(target_root, 'mask', seg_file))
        print(f"✅ Extracted Case {count+1}: {patient_folder}")
        count += 1
    else:
        # If naming is slightly different, we do a quick search inside
        for f in os.listdir(patient_path):
            if "-t1c.nii.gz" in f:
                shutil.copy2(os.path.join(patient_path, f), os.path.join(target_root, 't1c', f))
            if "-seg.nii.gz" in f:
                shutil.copy2(os.path.join(patient_path, f), os.path.join(target_root, 'mask', f))
        print(f"✅ Extracted Case {count+1} (via Search): {patient_folder}")
        count += 1

print(f"\n✨ Mission Success! {count} GBM cases ready.")