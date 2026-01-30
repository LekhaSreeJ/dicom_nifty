import os
import SimpleITK as sitk
import matplotlib.pyplot as plt
import numpy as np

def visualize_sample(image_path, title="MRI Sample"):
    # Load and convert to array
    img = sitk.ReadImage(image_path)
    img_array = sitk.GetArrayFromImage(img)
    
    # Get the middle slice
    mid_slice = img_array[img_array.shape[0] // 2, :, :]
    
    plt.figure(figsize=(6, 6))
    plt.imshow(mid_slice, cmap='gray')
    plt.title(f"{title}\nShape: {img_array.shape}")
    plt.axis('off')
    plt.show()

def test_preprocess_sample():
    base_in = "data/1_pep_pipeline"
    base_out = "data/processed"
    classes = ['X1_Normal', 'X2_Stroke', 'X3_MS', 'X4_Mets', 'X5_GBM']
    
    for cls in classes:
        in_dir = os.path.join(base_in, cls)
        if not os.path.exists(in_dir): continue
        
        # Pick ONLY THE FIRST file in the folder for testing
        files = [f for f in os.listdir(in_dir) if f.endswith(('.nii', '.nii.gz'))]
        if not files: continue
        
        filename = files[0]
        in_path = os.path.join(in_dir, filename)
        out_dir = os.path.join(base_out, cls)
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, f"test_{filename}")
        
        print(f"🧪 Testing Class: {cls} | File: {filename}")
        
        # --- Simple Preprocessing Logic ---
        img = sitk.ReadImage(in_path)
        
        # Intensity Normalization only for test viz
        img_arr = sitk.GetArrayFromImage(img)
        img_arr = (img_arr - np.mean(img_arr)) / (np.std(img_arr) + 1e-8)
        
        processed_img = sitk.GetImageFromArray(img_arr)
        sitk.WriteImage(processed_img, out_path)
        
        # Visualize the PROCESSED image
        visualize_sample(out_path, title=f"Processed {cls}")
        break # Oru class pathaale podhum, illana break-ah remove pannunga 5-um paaka

if __name__ == "__main__":
    test_preprocess_sample()