import os
import shutil
import nibabel as nib

# --- CONFIGURATION ---
raw_base = r"D:\pep_2026\dataset\final_dataset"
pep_base = r"D:\pep_2026\dataset\final_dataset\1_PEP_Pipeline"

class_mapping = {
    'X1_Normal': '1_oasis_disc_batch_1',
    'X2_Stroke': '2_isles_extracted_batch_1',
    'X3_MS': '3_ms_extracted_batch_1',
    'X4_Mets': '4_mets_extracted_batch_1',
    'X5_GBM': '5_gbm_extracted_batch_1'
}

# 1. Setup Base Folders
for cls in class_mapping.keys():
    os.makedirs(os.path.join(pep_base, cls, 'images'), exist_ok=True)
    os.makedirs(os.path.join(pep_base, cls, 'masks'), exist_ok=True)

print("📁 PEP Structure Created. Processing Files...")

# 2. Process OASIS (X1) - HDR/IMG Conversion
oasis_path = os.path.join(raw_base, class_mapping['X1_Normal'])
for root, dirs, files in os.walk(oasis_path):
    for f in files:
        if f.lower().endswith('.hdr'):
            hdr_path = os.path.join(root, f)
            try:
                img = nib.load(hdr_path)
                patient_id = os.path.basename(root)
                save_path = os.path.join(pep_base, 'X1_Normal', 'images', f"{patient_id}_normal.nii.gz")
                nib.save(img, save_path)
                print(f"✅ X1 Converted: {patient_id}")
            except Exception as e:
                print(f"❌ Error converting {f}: {e}")

# 3. Process X2 to X5 (Moving & Renaming)
for cls, folder_name in list(class_mapping.items())[1:]:
    src_folder = os.path.join(raw_base, folder_name)
    
    # Standard sub-folder search
    for sub in os.listdir(src_folder):
        sub_path = os.path.join(src_folder, sub)
        if not os.path.isdir(sub_path): continue
        
        # Decide destination based on folder name
        dest_type = 'masks' if 'mask' in sub.lower() else 'images'
        target_dir = os.path.join(pep_base, cls, dest_type)
        
        for f in os.listdir(sub_path):
            f_lower = f.lower()
            if '.nii' in f_lower or '.gz' in f_lower:
                # Standardizing extension to .nii.gz for our pipeline
                new_name = f_lower if f_lower.endswith('.gz') else f_lower + '.gz'
                shutil.copy2(os.path.join(sub_path, f), os.path.join(target_dir, new_name))
    
    print(f"✅ {cls} Organized!")

print(f"\n✨ DONE! Check {pep_base} for the final structured data.")