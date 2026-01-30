import os
import shutil

# --- CONFIGURATION ---
# Unga ISLES dataset root (Ex: D:\pep_2026\dataset\ISLES2022)
source_root = r"D:\pep_2026\dataset\stroke lession_isles_class_2\ISLES-2022\ISLES-2022"
# Target folder
target_root = r"D:\pep_2026\dataset\stroke lession_isles_class_2\isles_extracted_batch_1"

# Folder names
sub_folders = ['adc', 'flair', 'mask']

# Folders-ah create pannuvom
for folder in sub_folders:
    os.makedirs(os.path.join(target_root, folder), exist_ok=True)

print("🚀 ISLES Extraction Start aagudhu... Locked In!")

count = 0

# ISLES folder structure: sub-XXX/ses-XXX/dwi or anat
for root, dirs, files in os.walk(source_root):
    # Subject ID-ah path-la irundhu edupom (sub-case001)
    path_parts = root.split(os.sep)
    subject_id = next((p for p in path_parts if p.startswith('sub-')), None)
    
    if not subject_id:
        continue

    for file in files:
        if not file.endswith('.nii.gz'):
            continue
            
        target_file_name = f"{subject_id}_{file}"
        source_path = os.path.join(root, file)

        # 1. ADC Extraction (For PEP)
        if 'adc' in file.lower() and 'derivatives' not in root:
            shutil.copy2(source_path, os.path.join(target_root, 'adc', target_file_name))
            
        # 2. FLAIR Extraction (For Harmonization Paper)
        elif 'flair' in file.lower() and 'derivatives' not in root:
            shutil.copy2(source_path, os.path.join(target_root, 'flair', target_file_name))
            
        # 3. Mask Extraction (For Validation/XAI)
        elif 'msk' in file.lower() or 'label-lesion' in file.lower():
            # Usually masks are in 'derivatives' folder
            shutil.copy2(source_path, os.path.join(target_root, 'mask', target_file_name))

    # Progress Update (Optional: just to know it's working)
    if subject_id:
        print(f"✅ Processed: {subject_id}")
        count += 1

# Note: os.walk thirumba thirumba same sub folders-ku pogum, 
# so real count subject level-la calculate pannanum.
print(f"\n✨ Success! Files organized in {target_root}")