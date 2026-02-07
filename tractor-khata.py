import streamlit as st
import pandas as pd
import os

# --- 1. App Config ---
st.set_page_config(page_title="JAVED RANGHAD TRACTOR KHATA", layout="wide")

# --- 2. Custom Design (Watermark & Sidebar Color) ---
def apply_design(tractor_name):
    name_up = tractor_name.upper()
    # High Quality Direct Image Links
    if "FARMTRACK" in name_up:
        img = "https://th.bing.com/th/id/OIP.UeE_7mY6x89-f5v_F8Gj_AHaE8?rs=1&pid=ImgDetMain"
    elif "605" in name_up or "NOVO" in name_up:
        img = "https://th.bing.com/th/id/OIP.H_6E4-x2-x-S_0tS3n08RAHaFj?rs=1&pid=ImgDetMain"
    else:
        img = "https://images.pexels.com/photos/162637/tractor-agriculture-farm-drive-162637.jpeg"

    st.markdown(f"""
    <style>
    /* Main Screen: ONLY TRACTOR WATERMARK (NO WHITE OVERLAY) */
    .stApp {{
        background-image: url("{img}") !important;
        background-repeat: no-repeat !important;
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
        background-blend-mode: normal !important;
    }}

    /* Sidebar: DARK CHERRY RED (Aapki marking ke hisaab se) */
    [data-testid="stSidebar"] {{
        background-color: #800000 !important;
        opacity: 1 !important;
    }}
    
    /* Sidebar text color and inputs */
    [data-testid="stSidebar"] * {{
        color: white !important;
    }}
    
    /* Title: Huge & Clear on Photo */
    .tractor-title {{
        font-size: 90px !important;
        font-weight: 900 !important;
        color: #FFFFFF !important;
        text-align: center !important;
        text-shadow: 5px 5px 20px black !important;
        margin-top: -60px !important;
        font-family: 'Arial Black', sans-serif !important;
    }}

    /* Metrics: Semi-Transparent for readability */
    [data-testid="stMetric"] {{
        background-color: rgba(255, 255, 255, 0.95) !important;
        padding: 20px !important;
        border-radius: 15px !important;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.5) !important;
        border-left: 10px solid #800000 !important;
    }}
    
    [data-testid="stMetricValue"] {{
        color: #800000 !important;
        font-weight: bold !important;
    }}

    /* Data Table Visibility */
    .stDataFrame {{
        background-color: rgba(255, 255, 255, 0.9) !important;
        border-radius: 10px !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. Data File Logic ---
DATA_FILE = "tractor_data.csv"
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=["DATE", "TRACTOR", "DRIVER_NAME", "ROUND", "WEIGHT", "RATE", "KAMAI", "DIESEL", "DRIVER_EXP", "OTHER", "TOTAL_INV", "PROFIT"])

# --- 4. Sidebar Menu ---
with st.sidebar:
    st.header("🚜 JAVED RANGHAD")
    active_tractor = st.selectbox("Apna Tractor Chunein", ["FARMTRACK 60", "MAHINDRA NOVO 605"])
    st.divider()
    
    st.subheader("📝 Nayi Entry")
    date = st.date_input("Tarik")
    d_name = st.text_input("Driver Name")
    weight = st.number_input("Weight (KG)", min_value=0.0, step=100.0)
    rate = st.number_input("Rate", min_value=0.0, format="%.4f")
    
    st.markdown("---")
    st.markdown("**Kharche (Expenses)**")
    diesel = st.number_input("Diesel", min_value=0.0)
    d_pay = st.number_input("Driver Exp", min_value=0.0)
    other = st.number_input("Other", min_value=0.0)

    if st.button("💾 SAVE RECORD"):
        kamai_val = float(weight * rate)
        kharcha_val = float(diesel + d_pay + other)
        profit_val = float(kamai_val - kharcha_val)
        
        new_data = {
            "DATE": str(date), "TRACTOR": active_tractor, "DRIVER_NAME": d_name,
            "ROUND": 1, "WEIGHT": weight, "RATE": rate, "KAMAI": round(kamai_val, 2),
            "DIESEL": diesel, "DRIVER_EXP": d_pay, "OTHER": other,
            "TOTAL_INV": round(kharcha_val, 2), "PROFIT": round(profit_val, 2)
        }
        df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
