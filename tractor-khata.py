import streamlit as st
import pandas as pd
import os

# --- 1. App Configuration ---
st.set_page_config(page_title="JAVED RANGHAD TRACTOR KHATA", layout="wide")

# --- 2. Custom Design (Cherry Sidebar & High-Visibility Watermark) ---
def apply_custom_design(tractor_name):
    name_up = tractor_name.upper()
    
    # Asli Tractor Image Links (Watermark)
    if "FARMTRACK" in name_up:
        img_url = "https://th.bing.com/th/id/OIP.UeE_7mY6x89-f5v_F8Gj_AHaE8?rs=1&pid=ImgDetMain"
    elif "605" in name_up or "NOVO" in name_up:
        img_url = "https://th.bing.com/th/id/OIP.H_6E4-x2-x-S_0tS3n08RAHaFj?rs=1&pid=ImgDetMain"
    else:
        img_url = "https://images.pexels.com/photos/162637/tractor-agriculture-farm-drive-162637.jpeg"

    st.markdown(f"""
    <style>
    /* 1. Background: Full Clear Tractor Photo */
    .stApp {{
        background-image: url("{img_url}") !important;
        background-repeat: no-repeat !important;
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }}

    /* 2. Sidebar: Dark Cherry Color (Aapki marking ke hisaab se) */
    [data-testid="stSidebar"] {{
        background-color: #800000 !important;
    }}
    
    /* Sidebar text color white */
    [data-testid="stSidebar"] .stMarkdown, 
    [data-testid="stSidebar"] label, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h1 {{
        color: white !important;
        font-weight: bold !important;
    }}

    /* 3. Title Style: Big White with Black Shadow */
    .tractor-title {{
        font-size: 80px !important;
        font-weight: 950 !important;
        color: #FFFFFF !important; 
        text-align: center !important;
        margin-top: -50px !important;
        text-shadow: 4px 4px 15px rgba(0,0,0,1) !important;
        font-family: 'Arial Black', sans-serif !important;
        text-transform: uppercase;
    }}

    /* 4. Metrics Cards: Readable White Boxes */
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
    
    /* Table styling */
    .stDataFrame {{
        background-color: rgba(255, 255, 255, 0.9) !important;
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
    st.header("🚜 JAVED RANGHAD")
    base_tractors = ["FARMTRACK 60", "MAHINDRA NOVO 605"]
    active_tractor = st.selectbox("Tractor Chunein", base_tractors)
    st.divider()
    
    st.subheader("📝 Nayi Entry")
    date = st.date_input("Tarik")
    d_name = st.text_input("Driver Name")
    weight = st.number_input("Weight (KG)", min_value=0.0)
    rate = st.number_input("Rate", min_value=0.0, format="%.4f")
    
    st.markdown("---")
    st.markdown("**Kharche (Expenses)**")
    diesel = st.number_input("Diesel", min_value=0.0)
    d_pay = st.number_input("Driver Exp", min_value=0.0)
    other = st.number_input("Other Exp", min_value=0.0)

    if st.button("💾 SAVE RECORD"):
        kamai = weight * rate
        total_inv = diesel + d_pay + other
        new_entry = {
            "DATE": str(date), 
            "TRACTOR": active_tractor, 
            "DRIVER_NAME": d_name,
            "ROUND": 1, 
            "WEIGHT": weight, 
            "RATE": rate, 
            "KAMAI": round(kamai, 2),
            "DIESEL": diesel, 
            "DRIVER_EXP": d_pay, 
            "OTHER": other,
            "TOTAL_INV": round(total_inv, 2), 
            "PROFIT": round(kamai - total_inv, 2)
        }
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("Record Save Ho Gaya!")
        st.rerun()

# --- 5. Main Page Display ---
apply_custom_design(active_tractor)

# Bada Title
st.markdown(f'<h1 class="tractor-title">{active_tractor}</h1>', unsafe_allow_html=True)

# Filter Data
t_df = df[df["TRACTOR"] == active_tractor]

# Metrics Display
c1, c2, c3, c4 = st.columns(4)
c1.metric("1. TOTAL WEIGHT", f"{t_df['WEIGHT'].sum():.2f} KG")
c2.metric("2. TOTAL KAMAI", f"₹{t_df['KAMAI'].sum():.2f}")
c3.metric("3. TOTAL KHARCHA", f"₹{t_df['TOTAL_INV
