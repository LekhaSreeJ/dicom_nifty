import os
import pydicom
import nibabel as nib
import numpy as np

def convert_memory_safe(dicom_dir, output_path):
    """
    Core engine: Folders-ah deep-ah search panni DICOM-ah NIfTI-ah mathum.
    """
    try:
        # 1. Deep search for .dcm files using os.walk
        all_dcm_files = []
        for root, dirs, filenames in os.walk(dicom_dir):
            for f in filenames:
                if f.lower().endswith('.dcm'):
                    all_dcm_files.append(os.path.join(root, f))

        if not all_dcm_files:
            return False, "No DICOM files found in the folder!"

        # 2. Read and Sort
        files = [pydicom.dcmread(f) for f in all_dcm_files]
        files.sort(key=lambda x: float(x.ImagePositionPatient[2]) if 'ImagePositionPatient' in x else 0)

        # 3. Create 3D Array (Float32 for Memory)
        img_shape = list(files[0].pixel_array.shape) + [len(files)]
        img3d = np.zeros(img_shape, dtype=np.float32)

        for i, s in enumerate(files):
            img3d[:, :, i] = s.pixel_array.astype(np.float32)

        # 4. Save NIfTI
        nifti_img = nib.Nifti1Image(img3d, np.eye(4))
        nib.save(nifti_img, output_path)
        
        return True, output_path

    except Exception as e:
        return False, str(e)

if __name__ == "__main__":
    # Terminal-la direct-ah test panna indha block
    input_folder = "data/raw/dicom/dicom_file"
    output_file = "data/processed/manual_test.nii.gz"
    success, result = convert_memory_safe(input_folder, output_file)
    print(f"Success: {success}, Result: {result}")