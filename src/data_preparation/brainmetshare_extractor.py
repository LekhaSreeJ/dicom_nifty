import os
import shutil

# --- CONFIGURATION ---
# Pointing directly to the train folder
source_root = r"D:\pep_2026\dataset\brainmetshare_class_4\train" 
target_root = r"D:\pep_2026\dataset\mets_extracted_batch_1"

os.makedirs(os.path.join(target_root, 't1_gd'), exist_ok=True)
os.makedirs(os.path.join(target_root, 'mask'), exist_ok=True)

print("🚀 BrainMetShare Extraction (Train Set Only) Start...")

count = 0

# os.listdir will give Mets_001, Mets_002, etc.
for patient_folder in os.listdir(source_root):
    patient_path = os.path.join(source_root, patient_folder)
    
    if os.path.isdir(patient_path):
        # We need specific files: t1_gd.nii.gz and seg.nii.gz
        t1_gd_file = "t1_gd.nii.gz"
        seg_file = "seg.nii.gz"
        
        t1_gd_src = os.path.join(patient_path, t1_gd_file)
        seg_src = os.path.join(patient_path, seg_file)
        
        # Check if both exist before copying
        if os.path.exists(t1_gd_src) and os.path.exists(seg_src):
            # Destination with patient ID prefix to keep it organized
            shutil.copy2(t1_gd_src, os.path.join(target_root, 't1_gd', f"{patient_folder}_t1_gd.nii.gz"))
            shutil.copy2(seg_src, os.path.join(target_root, 'mask', f"{patient_folder}_seg.nii.gz"))
            
            print(f"✅ Extracted: {patient_folder}")
            count += 1
        else:
            print(f"⚠️ Skipping {patient_folder}: Missing t1_gd or seg file.")

print(f"\n✨ Done! Extracted {count} Mets cases from the Train folder.")