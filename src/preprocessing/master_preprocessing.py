import os
import SimpleITK as sitk
import numpy as np

def resample_image(itk_image, target_size=(128, 128, 128), is_mask=False):
    """
    Resamples an ITK image to a fixed size. 
    Uses Linear interpolation for images and Nearest Neighbor for masks.
    """
    original_size = itk_image.GetSize()
    original_spacing = itk_image.GetSpacing()
    
    # Calculate new spacing to fit the target_size
    new_spacing = [
        original_size[i] * original_spacing[i] / target_size[i]
        for i in range(3)
    ]
    
    resample = sitk.ResampleImageFilter()
    resample.SetOutputSpacing(new_spacing)
    resample.SetSize(target_size)
    resample.SetOutputDirection(itk_image.GetDirection())
    resample.SetOutputOrigin(itk_image.GetOrigin())
    resample.SetTransform(sitk.Transform())
    
    # CRITICAL: Masks use NearestNeighbor to keep labels as 0, 1, 2...
    # Images use Linear for smooth intensity transition.
    if is_mask:
        resample.SetInterpolator(sitk.sitkNearestNeighbor)
    else:
        resample.SetInterpolator(sitk.sitkLinear)
        
    return resample.Execute(itk_image)

def process_and_save(image_path, mask_path, out_img_path, out_mask_path):
    # 1. Process IMAGE
    img = sitk.ReadImage(image_path)
    img_resampled = resample_image(img, is_mask=False)
    
    img_arr = sitk.GetArrayFromImage(img_resampled).astype(np.float32)
    # Z-Score Normalization
    img_arr = (img_arr - np.mean(img_arr)) / (np.std(img_arr) + 1e-8)
    
    final_img = sitk.GetImageFromArray(img_arr)
    final_img.CopyInformation(img_resampled)
    sitk.WriteImage(final_img, out_img_path)
    
    # 2. Process MASK (If exists)
    if mask_path and os.path.exists(mask_path):
        mask = sitk.ReadImage(mask_path)
        mask_resampled = resample_image(mask, is_mask=True)
        sitk.WriteImage(mask_resampled, out_mask_path)

def run_full_pipeline():
    base_in = "data/1_pep_Pipeline"
    base_out = "data/processed" # Stick to our agreed structure
    classes = ['X1_Normal', 'X2_Stroke', 'X3_MS', 'X4_Mets', 'X5_GBM']
    
    for cls in classes:
        img_in_dir = os.path.join(base_in, cls, "images")
        mask_in_dir = os.path.join(base_in, cls, "masks")
        
        img_out_dir = os.path.join(base_out, cls, "images")
        mask_out_dir = os.path.join(base_out, cls, "masks")
        
        if not os.path.exists(img_in_dir):
            print(f"⏩ Skipping {cls}: Image folder not found")
            continue
            
        os.makedirs(img_out_dir, exist_ok=True)
        os.makedirs(mask_out_dir, exist_ok=True)
        
        files = [f for f in os.listdir(img_in_dir) if f.lower().endswith(('.nii', '.nii.gz'))]
        print(f"🚀 Processing {len(files)} files in {cls}...")
        
        for filename in files:
            img_in_path = os.path.join(img_in_dir, filename)
            # Assuming mask has same name as image
            mask_in_path = os.path.join(mask_in_dir, filename) 
            
            img_out_path = os.path.join(img_out_dir, filename)
            mask_out_path = os.path.join(mask_out_dir, filename)
            
            try:
                process_and_save(img_in_path, mask_in_path, img_out_path, mask_out_path)
            except Exception as e:
                print(f"❌ Error in {filename}: {e}")
                
    print("\n✅ ALL IMAGES AND MASKS PREPROCESSED SUCCESSFULLY!")

if __name__ == "__main__":
    run_full_pipeline()