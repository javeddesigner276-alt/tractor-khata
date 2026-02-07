import streamlit as st
import pandas as pd
import os

# --- 1. App Configuration ---
st.set_page_config(page_title="JAVED RANGHAD TRACTOR KHATA", layout="wide")

# --- 2. Custom Design (Cherry Sidebar & Clear Watermark for ALL) ---
def apply_custom_design(tractor_name):
    name_up = tractor_name.upper()
    
    # Sabhi tractors ke liye images
    if "FARMTRACK" in name_up:
        img_url = "https://th.bing.com/th/id/OIP.UeE_7mY6x89-f5v_F8Gj_AHaE8?rs=1&pid=ImgDetMain"
    elif "NOVO" in name_up or "605" in name_up:
        img_url = "https://th.bing.com/th/id/OIP.H_6E4-x2-x-S_0tS3n08RAHaFj?rs=1&pid=ImgDetMain"
    elif "NAGISH" in name_up:
        img_url = "https://th.bing.com/th/id/OIP.XG6nU7L2X_H0O7Q_y_XW_AHaE8?rs=1&pid=ImgDetMain"
    else:
        img_url = "https://cdn.pixabay.com/photo/2014/07/06/17/20/tractor-385681_1280.jpg"

    st.markdown(f"""
    <style>
    /* Main Screen: NO WHITE SHADE, ONLY TRACTOR */
    .stApp {{
        background-image: url("{img_url}") !important;
        background-repeat: no-repeat !important;
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }}

    /* Sidebar: DARK CHERRY RED (Aapki marking ke hisaab se) */
    [data-testid="stSidebar"] {{
        background-color: #800000 !important;
    }}
    
    /* Sidebar text to white */
    [data-testid="stSidebar"] .stMarkdown, 
    [data-testid="stSidebar"] label, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h1 {{
        color: white !important;
        font-weight: bold !important;
    }}

    /* Title: BIG WHITE (With Shadow) */
    .tractor-title {{
        font-size: 85px !important;
        font-weight: 950 !important;
        color: #FFFFFF !important; 
        text-align: center !important;
        margin-top: -50px !important;
        text-shadow: 4px 4px 15px rgba(0,0,0,1) !important;
        font-family: 'Arial Black', sans-serif !important;
        text-transform: uppercase;
    }}

    /* Metrics: Sequence and Design */
    [data-testid="stMetric"] {{
        background-color: rgba(255, 255, 255, 0.95) !important;
        padding: 20px !important;
        border-radius: 12px !important;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.5) !important;
        border-left: 10px solid #800000 !important;
    }}
    
    [data-testid="stMetricValue"] {{
        color: #800000 !important;
        font-weight: 900 !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. Data Management ---
DATA_FILE = "tractor_data.csv"
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    cols = ["DATE", "TRACTOR", "DRIVER_NAME", "ROUND", "WEIGHT", "RATE", "KAMAI", "DIESEL", "DRIVER_EXP", "OTHER", "TOTAL_INV", "PROFIT"]
    df = pd.DataFrame(columns=cols)

# --- 4. Sidebar Setup ---
with st.sidebar:
    st.header("🚜 DASHBOARD MENU")
    base_tractors = ["FARMTRACK 60", "MAHINDRA NOVO 605", "NAGISH 106"]
    active_tractor = st.selectbox("Apna Tractor Chunein", base_tractors)
    st.divider()
    
    st.subheader("📝 Nayi Entry")
    date = st.date_input("Tarik")
    d_name = st.text_input("Driver Name")
    weight = st.number_input("Weight (KG)", min_value=0.0)
    rate = st.number_input("Rate", min_value=0.0, format="%.4f")
    
    st.markdown("---")
