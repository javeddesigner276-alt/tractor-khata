import streamlit as st
import pandas as pd
import os

# --- 1. App Configuration ---
st.set_page_config(page_title="JAVED RANGHAD TRACTOR KHATA", layout="wide")

# --- 2. Custom Design (Sidebar Color Shift & Clear Main Screen) ---
def apply_custom_design(tractor_name):
    name_up = tractor_name.upper()
    
    # Asli Tractor Images
    if "FARMTRACK" in name_up:
        img_url = "https://th.bing.com/th/id/OIP.UeE_7mY6x89-f5v_F8Gj_AHaE8?rs=1&pid=ImgDetMain"
    elif "NOVO" in name_up or "605" in name_up:
        img_url = "https://th.bing.com/th/id/OIP.H_6E4-x2-x-S_0tS3n08RAHaFj?rs=1&pid=ImgDetMain"
    else:
        img_url = "https://images.pexels.com/photos/162637/tractor-agriculture-farm-drive-162637.jpeg"

    st.markdown(f"""
    <style>
    /* 1. Main Background: NO COLOR OVERLAY, ONLY CLEAR WATERMARK */
    .stApp {{
        background: url("{img_url}") !important;
        background-repeat: no-repeat !important;
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }}

    /* 2. Sidebar: CHERRY COLOUR SHIFTED HERE */
    section[data-testid="stSidebar"] {{
        background-color: #700000 !important; /* Gehra Cherry Colour */
    }}
    
    /* Sidebar text colour to white for visibility */
    section[data-testid="stSidebar"] .stMarkdown, 
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] h1 {{
        color: white !important;
    }}

    /* 3. Title Styling */
    .tractor-title {{
        font-size: 80px !important;
        font-weight: 900 !important;
        color: #D32F2F !important; 
        text-align: center !important;
        margin-top: -50px !important;
        text-shadow: 2px 2px 8px rgba(255,255,255,0.8) !important;
        font-family: 'Arial Black', sans-serif !important;
    }}

    /* 4. Metrics Cards (Semi-Transparent) */
    [data-testid="stMetric"] {{
        background-color: rgba(255, 255, 255, 0.9) !important;
        padding: 15px !important;
        border-radius: 10px !important;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.2) !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. Data Loading ---
DATA_FILE = "tractor_data.csv"
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    cols = ["DATE", "TRACTOR", "DRIVER_NAME", "ROUND", "WEIGHT", "RATE", "KAMAI", "DIESEL", "DRIVER_EXP", "OTHER", "TOTAL_INV", "PROFIT"]
    df = pd.DataFrame(columns=cols)

# --- 4. Sidebar Menu (NOW CHERRY COLOR) ---
with st.sidebar:
    st.header("🚜 DASHBOARD MENU")
    base_tractors = ["FARMTRACK 60", "MAHINDRA NOVO 605"]
    active_tractor = st.selectbox("Apna Tractor Chunein", base_tractors)
    st.divider()
    
    st.subheader("📝 Nayi Entry")
    date = st.date_input("Tarik")
    d_name = st.text_input("Driver ka Naam")
    weight = st.number_input("Weight (KG)", min_value=0.0)
    rate = st.number_input("Rate", min_value=0.0, format="%.4f")
    
    st.markdown("**Kharche**")
    diesel = st.number_input("Diesel Kharcha", min_value=0.0)
    d_pay = st.number_input("Driver Kharcha", min_value=0.0)
    other = st.number_input("Other Kharcha", min_value=0.0)

    if st.button("💾 SAVE RECORD"):
        kamai = weight * rate
        total_inv = diesel + d_pay + other
        new_row = {
            "DATE": str(date), "TRACTOR": active_tractor, "DRIVER_NAME": d_name,
            "ROUND": 1, "WEIGHT": weight, "RATE": rate, "KAMAI": round(kamai, 2),
            "DIESEL": diesel, "DRIVER_EXP": d_pay, "OTHER": other,
            "TOTAL_INV": round(total_inv, 2), "PROFIT": round(kamai - total_inv, 2)
