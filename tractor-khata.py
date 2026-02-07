import streamlit as st
import pandas as pd
import os

# --- 1. App Configuration ---
st.set_page_config(page_title="JAVED RANGHAD TRACTOR KHATA", layout="wide")

# --- 2. Custom Design (Sidebar Cherry & Clear Main Screen) ---
def apply_custom_design(tractor_name):
    name_up = tractor_name.upper()
    
    # Asli Tractor Images (Full Clear)
    if "FARMTRACK" in name_up:
        img_url = "https://th.bing.com/th/id/OIP.UeE_7mY6x89-f5v_F8Gj_AHaE8?rs=1&pid=ImgDetMain"
    elif "NOVO" in name_up or "605" in name_up:
        img_url = "https://th.bing.com/th/id/OIP.H_6E4-x2-x-S_0tS3n08RAHaFj?rs=1&pid=ImgDetMain"
    else:
        img_url = "https://images.pexels.com/photos/162637/tractor-agriculture-farm-drive-162637.jpeg"

    st.markdown(f"""
    <style>
    /* 1. Main Background: NO COLOUR, ONLY CLEAR WATERMARK */
    .stApp {{
        background: url("{img_url}") !important;
        background-repeat: no-repeat !important;
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }}

    /* 2. Sidebar: CHERRY COLOUR APPLIED HERE */
    section[data-testid="stSidebar"] {{
        background-color: #8B0000 !important; /* Cherry Red */
    }}
    
    /* Sidebar text to White */
    section[data-testid="stSidebar"] .stMarkdown, 
    section[data-testid="stSidebar"] label, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h1 {{
        color: white !important;
    }}

    /* 3. Tractor Title (Dark Red with White Shadow for clarity) */
    .tractor-title {{
        font-size: 100px !important;
        font-weight: 950 !important;
        color: #D32F2F !important; 
        text-align: center !important;
        margin-top: -50px !important;
        text-shadow: 2px 2px 10px rgba(255,255,255,0.8) !important;
        font-family: 'Arial Black', sans-serif !important;
    }}

    /* 4. Metrics: Transparent White Boxes */
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

# --- 4. Sidebar Menu (NOW CHERRY) ---
with st.sidebar:
    st.header("🚜 DASHBOARD MENU")
    base_tractors = ["FARMTRACK 60", "MAHINDRA NOVO 605"]
    active_tractor = st.selectbox("Tractor Chunein", base_tractors)
    st.divider()
    
    st.subheader("📝 Nayi Entry")
    date = st.date_input("Tarik")
    d_name = st.text_input("Driver Name")
    weight = st.number_input("Weight (KG)", min_value=0.0)
    rate = st.number_input("Rate", min_value=0.0, format="%.4f")
    
    st.markdown("**Kharche (Investment)**")
    diesel = st.number_input("Diesel", min_value=0.0)
    d_pay = st.number_input("Driver Exp", min_value=0.0)
    other = st.number_input("Other", min_value=0.0)

    if st.button("💾 SAVE RECORD"):
        kamai = weight * rate
        total_inv = diesel + d_pay + other
        # FIXED SYNTAX HERE:
        new_row = {
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
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("Saved!")
        st.rerun()

# --- 5. Main Page ---
apply_custom_design(active_tractor)

st.markdown(f'<h1 class="tractor-title">{active_tractor}</h1>', unsafe_allow_html=True)

t_df = df[df["TRACTOR"] == active_tractor]

# FIXED METRICS SYNTAX HERE:
col1, col2, col3, col4 = st.columns(4)
col1.metric("1. TOTAL WEIGHT", f"{t_df['WEIGHT'].sum():.2f} KG")
col2.metric("2. KUL KAMAI", f"₹{t_df['KAMAI'].sum():.2f}")
col3.metric("3. KUL KHARCHA", f"₹{t_df['TOTAL_INV'].sum():.2f}")
col4.metric("4. NET PROFIT", f"₹{t_df['PROFIT'].sum():.2f}")

st.divider()
st.subheader(f"📊 Table: {active_tractor}")
st.dataframe(t_df, use_container_width=True)

with st.expander("🗑️ Entry Delete"):
    if not t_df.empty:
        row_to_del = st.selectbox("Index chunein", t_df.index)
        if st.button("Confirm Delete"):
            df = df.drop(row_to_del)
            df.to_csv(DATA_FILE, index=False)
            st.rerun()
