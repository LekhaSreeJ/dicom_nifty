import os
import nibabel as nib
import pydicom
from pydicom.dataset import Dataset, FileDataset
from pydicom.uid import ExplicitVRLittleEndian
import datetime
import numpy as np

def convert_nifti_to_dicom(nifti_path, output_dir):
    """
    Core engine: 3D NIfTI-ah slices-ah pirichu professional DICOM format-la mathum.
    """
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # 1. Load NIfTI volume
        nifti_img = nib.load(nifti_path)
        data = nifti_img.get_fdata().astype(np.uint16) # DICOM usually 16-bit
        
        # NIfTI (X, Y, Z) order-la irukkum
        slices = data.shape[2]

        # 2. Loop through slices and save each as a DICOM file
        for i in range(slices):
            pixel_array = data[:, :, i]
            
            # DICOM header creation (The Professional Way)
            file_meta = Dataset()
            file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.2' # CT Image Storage
            file_meta.MediaStorageSOPInstanceUID = pydicom.uid.generate_uid()
            file_meta.ImplementationClassUID = pydicom.uid.generate_uid()
            file_meta.TransferSyntaxUID = ExplicitVRLittleEndian

            filename = os.path.join(output_dir, f"slice_{i:03d}.dcm")
            ds = FileDataset(filename, {}, file_meta=file_meta, preamble=b"\0" * 128)

            # Essential Metadata
            ds.PatientName = "PEP_Subject"
            ds.PatientID = "123456"
            ds.ContentDate = datetime.datetime.now().strftime('%Y%m%d')
            ds.ContentTime = datetime.datetime.now().strftime('%H%M%S.%f')
            ds.Modality = 'MR'
            ds.SeriesNumber = 1
            ds.InstanceNumber = i + 1
            ds.SliceLocation = i * 1.0
            ds.ImagePositionPatient = [0, 0, i]
            ds.ImageOrientationPatient = [1, 0, 0, 0, 1, 0]
            ds.SamplesPerPixel = 1
            ds.PhotometricInterpretation = "MONOCHROME2"
            ds.PixelRepresentation = 0
            ds.HighBit = 15
            ds.BitsStored = 16
            ds.BitsAllocated = 16
            
            # Shape and Data
            ds.Rows = pixel_array.shape[0]
            ds.Columns = pixel_array.shape[1]
            ds.PixelData = pixel_array.tobytes()

            ds.save_as(filename)

        return True, f"Successfully saved {slices} slices to {output_dir}"

    except Exception as e:
        return False, str(e)

if __name__ == "__main__":
    # Local Test
    input_nifti = "data/processed/manual_test.nii.gz"
    output_folder = "data/processed/inverse_test"
    success, result = convert_nifti_to_dicom(input_nifti, output_folder)
    print(f"Success: {success}, Result: {result}")