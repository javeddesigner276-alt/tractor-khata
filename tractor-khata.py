import streamlit as st
import pandas as pd
import os

# --- 1. App Configuration ---
st.set_page_config(page_title="JAVED RANGHAD TRACTOR KHATA", layout="wide")

# --- 2. Custom Design (DARK SIDEBAR & FULL CLEAR WATERMARK) ---
def apply_custom_design(tractor_name):
    name_up = tractor_name.upper()
    
    # Asli Tractor Images (Direct Links)
    if "FARMTRACK" in name_up:
        img_url = "https://th.bing.com/th/id/OIP.UeE_7mY6x89-f5v_F8Gj_AHaE8?rs=1&pid=ImgDetMain"
    elif "NOVO" in name_up or "605" in name_up:
        img_url = "https://th.bing.com/th/id/OIP.H_6E4-x2-x-S_0tS3n08RAHaFj?rs=1&pid=ImgDetMain"
    else:
        img_url = "https://images.pexels.com/photos/162637/tractor-agriculture-farm-drive-162637.jpeg"

    st.markdown(f"""
    <style>
    /* 1. Main Background: FULL VISIBILITY (No Lightness) */
    .stApp {{
        background-image: url("{img_url}") !important;
        background-repeat: no-repeat !important;
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }}

    /* 2. Sidebar: DARK CHERRY COLOUR (Shifted from Main) */
    [data-testid="stSidebar"] {{
        background-color: #800000 !important; /* Pakka Cherry Red */
    }}
    
    /* Sidebar text to White */
    [data-testid="stSidebar"] .stMarkdown, 
    [data-testid="stSidebar"] label, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h1 {{
        color: white !important;
        font-weight: bold !important;
    }}

    /* 3. Tractor Title: BADA AUR SAFED (Shadow ke saath taaki photo pe dikhe) */
    .tractor-title {{
        font-size: 90px !important;
        font-weight: 950 !important;
        color: #FFFFFF !important; 
        text-align: center !important;
        margin-top: -60px !important;
        text-shadow: 5px 5px 15px rgba(0,0,0,0.9) !important;
        font-family: 'Arial Black', sans-serif !important;
    }}

    /* 4. Metrics: Readable White Glass Look */
    [data-testid="stMetric"] {{
        background-color: rgba(255, 255, 255, 0.95) !important;
        padding: 20px !important;
        border-radius: 15px !important;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.5) !important;
        border-bottom: 5px solid #800000 !important;
    }}
    
    [data-testid="stMetricValue"] {{
