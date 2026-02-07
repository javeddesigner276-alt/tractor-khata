import streamlit as st
import pandas as pd
import os

# --- 1. App Configuration ---
st.set_page_config(page_title="JAVED RANGHAD TRACTOR KHATA", layout="wide")

# --- 2. Custom Professional Design (Dark Dashboard Style) ---
def apply_custom_design(tractor_name):
    name_up = tractor_name.upper()
    
    # Asli Tractor Images (High Visibility)
    if "FARMTRACK" in name_up:
        img_url = "https://th.bing.com/th/id/OIP.UeE_7mY6x89-f5v_F8Gj_AHaE8?rs=1&pid=ImgDetMain"
    elif "NOVO" in name_up or "605" in name_up:
        img_url = "https://th.bing.com/th/id/OIP.H_6E4-x2-x-S_0tS3n08RAHaFj?rs=1&pid=ImgDetMain"
    else:
        img_url = "https://images.pexels.com/photos/162637/tractor-agriculture-farm-drive-162637.jpeg"

    st.markdown(f"""
    <style>
    /* Background Watermark - Visibility Increased (0.5 opacity for darker look) */
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), 
                    url("{img_url}") !important;
        background-repeat: no-repeat !important;
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
        color: white !important;
    }}

    /* Main Title: BIG & SHADOWED */
    .tractor-title {{
        font-size: 85px !important;
        font-weight: 900 !important;
        color: #FF3131 !important; /* Bright Red */
        text-align: center !important;
        margin-top: -30px !important;
        text-shadow: 3px 3px 10px rgba(0,0,0,0.8) !important;
        font-family: 'Arial Black', sans-serif !important;
        text-transform: uppercase;
    }}

    /* Metrics Row - White Boxes like Sample */
    [data-testid="stMetric"] {{
        background-color: rgba(255, 255, 255, 0.9) !important;
        padding: 20px !important;
        border-radius: 10px !important;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.5) !important;
        border-left: 8px solid #FF3131 !important;
    }}
    
    [data-testid="stMetricLabel"] {{
        color: #333 !important;
        font-size: 20px !important;
        font-weight: bold !important;
    }}

    [data-testid="stMetricValue"] {{
        color: #1A237E !important;
        font-size: 45px !important;
        font-weight: 800 !important;
    }}

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {{
        background-color: #1E1E1E !important;
        color: white !important;
    }}
    
    /* Table Styling */
    .stDataFrame {{
        background-color: white !important;
        border-radius: 10px !important;
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

# --- 4. Sidebar Menu ---
with st.sidebar:
    st.header("🚜 DASHBOARD MENU")
    base_tractors = ["FARMTRACK 60", "MAHINDRA NOVO 605"]
    
    if not df.empty:
        all_tractors = sorted(list(set(base_tractors + df["TRACTOR"].unique().tolist())))
        if "NAGISH 106" in all_tractors: all_tractors.remove("NAGISH 106")
    else:
        all_tractors = base_tractors
    
    active_tractor = st.selectbox("Apna Tractor Chunein", all_tractors)
    st.divider()
    
    st.subheader("📝 Nayi Entry")
    date = st.date_input("Tarik")
    d_name = st.text_input("Driver ka Naam")
    weight = st.number_input("Weight (KG)", min_value=0.0, step=100.0)
    rate = st.number_input("Rate", min_value=0.0, format="%.4f")
    
    st.markdown("**Kharche**")
    diesel = st.number_input("Diesel", min_value=0.0)
    d_pay = st.number_input("Driver Exp", min_value=0.0)
    other = st.number_input("Other", min_value=0.0)

    if st.button("💾 SAVE RECORD"):
        kamai = weight * rate
        total_inv = diesel + d_pay + other
        new_row = {
            "DATE": str(date), "TRACTOR": active_tractor, "DRIVER_NAME": d_name,
            "ROUND": 1, "WEIGHT": weight, "RATE": rate, "KAMAI": round(kamai, 2),
            "DIESEL": diesel, "DRIVER_EXP": d_pay, "OTHER": other,
            "TOTAL_INV": round(total_inv, 2), "PROFIT": round(kamai - total_inv, 2)
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("Saved!")
        st.rerun()

# --- 5. Main Page Display ---
apply_custom_design(active_tractor)

# BIG TITLE
st.markdown(f'<h1 class="tractor-title">{active_tractor}</h1>', unsafe_allow_html=True)

t_df = df[df["TRACTOR"] == active_tractor]

# SEQUENCE (1. Weight, 2. Kamai, 3. Kharcha, 4. Profit)
col
