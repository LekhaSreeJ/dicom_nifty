import streamlit as st
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
import torch
import plotly.graph_objects as go
from src.components.inference_pipeline import PEPInference
import os

# Page Config
st.set_page_config(page_title="PEP - Probability Elimination Pipeline", layout="wide")

st.title("🧠 PEP: Probability Elimination Pipeline")
st.markdown("### 3D MRI Diagnostic Prototype | End-to-End Medical AI")

# Engine initialization with Cache
@st.cache_resource
def load_engine():
    return PEPInference(model_dir="models/")

try:
    engine = load_engine()
except Exception as e:
    st.error(f"Models load aagala bro. Models folder-la 5 .pth files irukka-nu paarunga. Error: {e}")

# Layout: 2 Columns
col1, col2 = st.columns([1.5, 1])

with col1:
    st.subheader("📁 Upload & Interactive 3D Explorer")
    uploaded_file = st.file_uploader("Upload Brain MRI (.nii.gz)", type=["gz", "nii"])

    if uploaded_file:
    # 1. Load Data
        temp_path = "temp_upload.nii.gz"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        nii_img = nib.load(temp_path)
        data = nii_img.get_fdata() 

        st.subheader("📁 3D Multi-Planar Reconstruction")
        
        # 2. Controls - Row 1
        c1, c2 = st.columns([1, 2])
        with c1:
            view_to_scroll = st.selectbox("Which plane to scroll?", ["Axial", "Sagittal", "Coronal"])
        with c2:
            # Dynamic slider based on selection
            if view_to_scroll == "Sagittal":
                max_v = data.shape[0] - 1
            elif view_to_scroll == "Coronal":
                max_v = data.shape[1] - 1
            else:
                max_v = data.shape[2] - 1
            
            slice_idx = st.slider(f"Move {view_to_scroll} Slider", 0, max_v, max_v // 2)

        # 3. The "Triple View" Plot
        fig, axes = plt.subplots(1, 3, figsize=(18, 6), facecolor='#0e1117')
        
        # Static Centers for other two (Scroll panradhu mattum slider-la maarum)
        s_idx = slice_idx if view_to_scroll == "Sagittal" else data.shape[0] // 2
        c_idx = slice_idx if view_to_scroll == "Coronal" else data.shape[1] // 2
        a_idx = slice_idx if view_to_scroll == "Axial" else data.shape[2] // 2

        # Sagittal
        axes[0].imshow(np.rot90(data[s_idx, :, :]), cmap='gray')
        axes[0].set_title(f"Sagittal {'(Active)' if view_to_scroll == 'Sagittal' else ''}", color='cyan')
        
        # Coronal
        axes[1].imshow(np.rot90(data[:, c_idx, :]), cmap='gray')
        axes[1].set_title(f"Coronal {'(Active)' if view_to_scroll == 'Coronal' else ''}", color='cyan')
        
        # Axial
        axes[2].imshow(np.rot90(data[:, :, a_idx]), cmap='gray')
        axes[2].set_title(f"Axial {'(Active)' if view_to_scroll == 'Axial' else ''}", color='cyan')

        for ax in axes: ax.axis('off')
        plt.tight_layout()
        st.pyplot(fig)
    else:
        st.info("👈 Please upload a .nii.gz file to start the 3D visualization.")

with col2:
    st.subheader("📊 Diagnostic Analysis")
    # Only show button if file is uploaded
    if uploaded_file:
        if st.button("🚀 Run PEP Inference"):
            with st.spinner("Eliminating Probabilities... Running 5 Binary Models..."):
                # Inference using the temp_path defined in col1
                prediction, scores = engine.predict("temp_upload.nii.gz")
                
                st.metric(label="Final Diagnosis", value=prediction)
                
                # Probability Graph
                labels = list(scores.keys())
                values = list(scores.values())

                fig_bar = go.Figure(go.Bar(
                    x=values,
                    y=labels,
                    orientation='h',
                    marker_color='indianred'
                ))
                fig_bar.update_layout(
                    title="Elimination Probability Chart",
                    xaxis_title="Probability (0 to 1)",
                    xaxis=dict(range=[0, 1]),
                    template="plotly_dark",
                    height=400
                )
                st.plotly_chart(fig_bar, width="stretch")
                
                if prediction == "Normal":
                    st.success("Analysis Complete: No significant pathology detected.")
                else:
                    st.warning(f"Analysis Complete: Potential {prediction} detected.")
    else:
        st.write("Results will appear here after inference.")

# Footer
st.divider()
st.caption("Developed by Lekha Sree J | 50+ LPA Career Comeback Project 2026")