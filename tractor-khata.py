import streamlit as st
import pandas as pd
import os

# --- 1. App Configuration ---
st.set_page_config(page_title="JAVED RANGHAD TRACTOR KHATA", layout="wide")

# --- 2. Custom Cherry Design (High Visibility Watermark) ---
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
    /* Background Cherry Colour & Full Visibility Watermark */
    .stApp {{
        background: linear-gradient(rgba(139, 0, 0, 0.4), rgba(139, 0, 0, 0.4)), 
                    url("{img_url}") !important;
        background-repeat: no-repeat !important;
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
        background-color: #8B0000 !important; /* Cherry Red Background */
    }}

    /* Tractor Name: DOUBLE SIZE & WHITE for Cherry Contrast */
    .tractor-title {{
        font-size: 110px !important;
        font-weight: 950 !important;
        color: #FFFFFF !important; /* White text for better visibility on cherry */
        text-align: center !important;
        margin-top: -50px !important;
        margin-bottom: 20px !important;
        text-shadow: 5px 5px 15px rgba(0,0,0,0.7) !important;
        font-family: 'Arial Black', sans-serif !important;
        text-transform: uppercase;
    }}

    /* Metrics Row - White Boxes with Cherry Border */
    [data-testid="stMetric"] {{
        background-color: rgba(255, 255, 255, 0.95) !important;
        padding: 25px !important;
        border-radius: 15px !important;
        box-shadow: 0px 8px 20px rgba(0,0,0,0.6) !important;
        border-left: 10px solid #D2143A !important; /* Cherry border on cards */
    }}
    
    [data-testid="stMetricLabel"] {{
        color: #000000 !important;
        font-size: 22px !important;
        font-weight: bold !important;
    }}

    [data-testid="stMetricValue"] {{
        color: #8B0000 !important; /* Cherry color for numbers */
        font-size: 50px !important;
        font-weight: 900 !important;
    }}

    /* Sidebar Styling - Cherry Theme */
    section[data-testid="stSidebar"] {{
        background-color: #4A0404 !important; /* Deep Cherry Sidebar */
        color: white !important;
    }}

    /* Table & Sidebar text */
    .stDataFrame, .stMarkdown, p, h3 {{
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border-radius: 5px;
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
    st.header("🚜 JAVED RANGHAD DASHBOARD")
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
        st.success("Save Ho Gaya!")
        st.rerun()

# --- 5. Main Page Display ---
apply_custom_design(active_tractor)

# BIG WHITE TITLE
st.markdown(f'<h1 class="tractor-title">{active_tractor}</h1>', unsafe_allow_html=True)

t_df = df[df["TRACTOR"] == active_tractor]

# SEQUENCE (1. Weight, 2. Kamai, 3. Kharcha, 4. Profit)
col1, col2, col3, col4 = st.columns(4)
col1.metric("1. TOTAL WEIGHT", f"{t_df['WEIGHT'].sum():.2f} KG")
col2.metric("2. KUL KAMAI", f"₹{t_df['KAMAI'].sum():.2f}")
col3.metric("3. KUL KHARCHA", f"₹{t_df['TOTAL_INV'].sum():.2f}")
col4.metric("4. NET PROFIT", f"₹{t_df['PROFIT'].sum():.2f}")

st.divider()
st.subheader(f"📊 Detailed Table: {active_tractor}")
st.dataframe(t_df, use_container_width=True)

# Delete Option
with st.
