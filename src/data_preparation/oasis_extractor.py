import os
import shutil

# --- CONFIGURATION ---
# Unga original raw dataset path
source_root = r"D:\pep_2026\dataset\oasis_normal_class_1\oasis_cross-sectional_disc3"
# Pudhusa create aaga vendiya folder
target_root = r"D:\pep_2026\dataset\oasis_normal_class_1\oasis_disc_batch_3"

# Target folder illana create pannikko
if not os.path.exists(target_root):
    os.makedirs(target_root)
    print(f"Created target directory: {target_root}")

print("🚀 Starting Selective Extraction...")

count = 0
# os.walk moolama subfolders kulla poi search pannuvom
for root, dirs, files in os.walk(source_root):
    for file in files:
        # Namma "Gold Data" - masked_gfc header file-ah mattum target panrom
        if file.endswith("_masked_gfc.hdr"):
            # Header file path
            hdr_source_path = os.path.join(root, file)
            
            # Adhe name la extension illama (or .img extension la) irukkira image file path
            # Sila system la extension kaattaadhu, so base name vachu edukkuron
            base_name = file.replace(".hdr", "")
            
            # Possible image file names (with or without .img)
            img_file_candidates = [f"{base_name}.img", base_name]
            
            # Check for the image file in the same folder
            img_source_path = None
            for candidate in img_file_candidates:
                candidate_path = os.path.join(root, candidate)
                if os.path.exists(candidate_path) and candidate_path != hdr_source_path:
                    img_source_path = candidate_path
                    break
            
            if img_source_path:
                # Patient ID (Folder name) eduthukkuvom (Example: OAS1_0001_MR1)
                # Path split panni folder name-ah identifier-ah use panrom
                patient_id = hdr_source_path.split(os.sep)[-5] # Inga unga path structure padi logic
                
                patient_target_dir = os.path.join(target_root, patient_id)
                os.makedirs(patient_target_dir, exist_ok=True)
                
                # Files-ah copy pannuvom (Original delete aagaadhu)
                shutil.copy2(hdr_source_path, os.path.join(patient_target_dir, f"{patient_id}_masked.hdr"))
                shutil.copy2(img_source_path, os.path.join(patient_target_dir, f"{patient_id}_masked.img"))
                
                print(f"✅ Extracted: {patient_id}")
                count += 1

print(f"\n✨ Mission Accomplished! Total Patients Extracted: {count}")
print(f"Files are ready in: {target_root}")