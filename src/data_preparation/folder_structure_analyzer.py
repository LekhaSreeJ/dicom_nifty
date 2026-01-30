import os
from collections import Counter

def analyze_data_structure(root_path):
    print(f"🔍 Analyzing: {root_path}")
    print("-" * 50)
    
    # Tracking folder structure
    for folder in sorted(os.listdir(root_path)):
        folder_path = os.path.join(root_path, folder)
        
        if os.path.isdir(folder_path):
            print(f"\n📂 Folder: {folder}")
            
            # Sub-analysis for each class folder
            extensions = []
            file_count = 0
            subfolders = []

            for root, dirs, files in os.walk(folder_path):
                for d in dirs:
                    subfolders.append(d)
                for f in files:
                    file_count += 1
                    # Extension-ah extract pannuvom
                    ext = os.path.splitext(f)[1].lower()
                    if f.endswith('.nii.gz'): # Special case for double extension
                        ext = '.nii.gz'
                    extensions.append(ext)
            
            # Count extension frequency
            ext_counts = Counter(extensions)
            
            # Print Summary
            print(f"   ├── Total Files: {file_count}")
            print(f"   ├── Unique Extensions: {dict(ext_counts)}")
            if subfolders:
                # Top 5 subfolders mattum kaatuvoom overload aagama irukka
                print(f"   └── Sample Subfolders: {list(set(subfolders))[:5]}")
        else:
            print(f"📄 Root File: {folder}")

# --- EXECUTION ---
# Unga main folder path-ah inga kudunga
main_path = r"D:\pep_2026\dataset\final_dataset\1_PEP_Pipeline" 
analyze_data_structure(main_path)