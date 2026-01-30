import os
import shutil

# --- CONFIGURATION ---
source_root = r"D:\pep_2026\dataset\multiple sclerosis_class_3\MSLesSeg Dataset\MSLesSeg Dataset" 
target_root = r"D:\pep_2026\dataset\multiple sclerosis_class_3\ms_extracted_batch_1"

os.makedirs(os.path.join(target_root, 'flair'), exist_ok=True)
os.makedirs(os.path.join(target_root, 'mask'), exist_ok=True)

print("🔍 Bulletproof Extraction Starting...")

count = 0

for root, dirs, files in os.walk(source_root):
    for file in files:
        file_upper = file.upper()
        
        # Check for MRI files with FLAIR or MASK in name
        if ".NII" in file_upper:
            source_path = os.path.join(root, file)
            
            # Determine Category
            category = None
            if "FLAIR" in file_upper:
                category = 'flair'
            elif "MASK" in file_upper:
                category = 'mask'
            
            if category:
                # Path structure-la irundhu Patient ID (P1, P2...) eduppom
                # D:\...\train\P1\T1\P1_T1_FLAIR.nii.gz -> root la P1 kandupidippom
                path_parts = root.split(os.sep)
                patient_id = "unknown"
                
                for part in reversed(path_parts):
                    # P followed by numbers (P1, P10 etc)
                    if part.upper().startswith('P') and any(char.isdigit() for char in part):
                        patient_id = part.upper()
                        break
                
                dest_name = f"{patient_id}_{file_upper}"
                dest_path = os.path.join(target_root, category, dest_name)
                
                shutil.copy2(source_path, dest_path)
                print(f"✅ SUCCESS: {dest_name}")
                count += 1

print(f"\n✨ Mission Accomplished! Extracted {count} files.")