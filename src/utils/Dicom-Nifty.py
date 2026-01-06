import os
import pydicom
import nibabel as nib
import numpy as np

def convert_memory_safe(dicom_dir, output_path):
    print(f"🔄 Memory-Safe Processing: {dicom_dir}")
    
    try:
        # 1. Ella .dcm files-ahyum list edukkrom
        files = [pydicom.dcmread(os.path.join(dicom_dir, f)) for f in os.listdir(dicom_dir) if f.endswith('.dcm')]
        
        # 2. Slice location vachu sort pandrom (Brain order-ku mukkiyam)
        files.sort(key=lambda x: float(x.ImagePositionPatient[2]))

        # 3. Pixel data-vah mattum eduthu 3D array-va mathrom
        # float32 use panni memory-ah save pandrom
        img_shape = list(files[0].pixel_array.shape) + [len(files)]
        img3d = np.zeros(img_shape, dtype=np.float32)

        for i, s in enumerate(files):
            img3d[:, :, i] = s.pixel_array.astype(np.float32)

        # 4. Simple affine matrix (Identity)
        affine = np.eye(4)

        # 5. Save as NIfTI
        nifti_img = nib.Nifti1Image(img3d, affine)
        nib.save(nifti_img, output_path)
        
        print(f"✅ FINAL SUCCESS! Saved to: {output_path}")

    except Exception as e:
        print(f"❌ Error again: {e}")

if __name__ == "__main__":
    input_folder = "data/raw/dicom/dicom_file"
    output_file = "data/processed/sample_brain_mri.nii.gz"
    
    if os.path.exists(input_folder):
        convert_memory_safe(input_folder, output_file)
    else:
        print("⚠️ Folder innum missing bro!")