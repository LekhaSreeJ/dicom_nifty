import streamlit as st
import os
import zipfile
import shutil
# Import both engines
from src.utils.Dicom_Nifty import convert_memory_safe
from src.utils.Nifty_Dicom import convert_nifti_to_dicom

st.set_page_config(page_title="PEP Medical AI Portal", page_icon="🧠", layout="wide")

# Sidebar for Navigation
st.sidebar.title("📑 Control Center")
page = st.sidebar.radio("Select Tool:", ["DICOM to NIfTI (Standard)", "NIfTI to DICOM (Inverse)"])

# Temporary directory cleanup function
def cleanup():
    for folder in ["temp_data", "data/raw/web_extract", "data/raw/dicom/inverse_test"]:
        if os.path.exists(folder):
            shutil.rmtree(folder)

# --- PAGE 1: DICOM TO NIFTI ---
if page == "DICOM to NIfTI (Standard)":
    st.title("🧠 DICOM to NIfTI Converter")
    st.info("Upload a ZIP file containing DICOM slices to generate a 3D NIfTI volume.")
    
    uploaded_zip = st.file_uploader("Upload DICOM ZIP", type="zip")
    
    if uploaded_zip:
        if st.button("Start Conversion 🚀"):
            with st.spinner("Processing..."):
                cleanup() # Clear old files
                os.makedirs("temp_data", exist_ok=True)
                
                # 1. Save and Extract ZIP
                zip_path = "temp_data/upload.zip"
                with open(zip_path, "wb") as f:
                    f.write(uploaded_zip.getbuffer())
                
                extract_dir = "temp_data/extract"
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_dir)
                
                # 2. Convert
                output_nifti = "temp_data/output.nii.gz"
                success, message = convert_memory_safe(extract_dir, output_nifti)
                
                if success:
                    st.success("✅ Conversion Complete!")
                    with open(output_nifti, "rb") as f:
                        st.download_button("Download NIfTI (.nii.gz)", f, file_name="output.nii.gz")
                else:
                    st.error(f"❌ Error: {message}")

# --- PAGE 2: NIFTI TO DICOM ---
elif page == "NIfTI to DICOM (Inverse)":
    st.title("🔄 NIfTI to DICOM Inverse Engine")
    st.warning("Professional Tool: Converts 3D NIfTI back to 2D DICOM slices with metadata.")
    
    uploaded_nifti = st.file_uploader("Upload NIfTI file", type=["nii", "gz"])
    
    if uploaded_nifti:
        if st.button("Generate DICOM Slices 🛠️"):
            with st.spinner("Slicing Volume..."):
                cleanup()
                os.makedirs("temp_data", exist_ok=True)
                
                # 1. Save NIfTI
                nifti_path = f"temp_data/{uploaded_nifti.name}"
                with open(nifti_path, "wb") as f:
                    f.write(uploaded_nifti.getbuffer())
                
                # 2. Convert
                output_dicom_dir = "temp_data/dicom_output"
                success, message = convert_nifti_to_dicom(nifti_path, output_dicom_dir)
                
                if success:
                    st.success(message)
                    # 3. Zip the output DICOMs for download
                    zip_results = "temp_data/converted_dicoms.zip"
                    with zipfile.ZipFile(zip_results, 'w') as zipf:
                        for root, _, files in os.walk(output_dicom_dir):
                            for file in files:
                                zipf.write(os.path.join(root, file), file)
                    
                    with open(zip_results, "rb") as f:
                        st.download_button("Download DICOM Slices (ZIP)", f, file_name="dicom_slices.zip")
                else:
                    st.error(f"❌ Error: {message}")

st.sidebar.markdown("---")
st.sidebar.write("Developed for **PEP Pipeline 2026**")