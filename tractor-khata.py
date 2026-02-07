import streamlit as st
import pandas as pd
import os

# --- 1. App Configuration ---
st.set_page_config(page_title="JAVED RANGHAD TRACTOR KHATA", layout="wide")

# --- 2. Custom Design (Bada Naam aur Watermark) ---
def apply_custom_design(tractor_name):
    # Watermark images
    img_url = "https://cdn.pixabay.com/photo/2014/07/06/17/20/tractor-385681_1280.jpg" # Default
    if "FARMTRACK" in tractor_name.upper():
        img_url = "https://th.bing.com/th/id/OIP.XG6nU7L2X_H0O7Q_y_XW_AHaE8?rs=1&pid=ImgDetMain"
    elif "NOVO" in tractor_name.upper() or "605" in tractor_name:
        img_url = "https://th.bing.com/th/id/OIP.7_z_Y-8Qk2P8Wf6y5A6Q-AHaE8?rs=1&pid=ImgDetMain"

    st.markdown(f"""
    <style>
    /* Background Watermark */
    .stApp {{
        background: linear-gradient(rgba(255,255,255,0.85), rgba(255,255,255,0.85)), url("{img_url}");
        background-repeat: no-repeat;
        background-size: cover;
        background-attachment: fixed;
    }}
    /* Tractor Name: DOUBLE SIZE (BIG) */
    .tractor-title {{
        font-size: 100px !important;
        font-weight: 900 !important;
        color: #CC0000 !important;
        text-align: center !important;
        margin-top: -30px !important;
        line-height: 1.2 !important;
        text-shadow: 4px 4px 10px rgba(0,0,0,0.3);
        font-family: 'Impact', sans-serif;
    }}
    /* Metrics Styling */
    [data-testid="stMetricValue"] {{
        font-size: 40px !important;
        color: #000080 !important;
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
    all_tractors = ["FARMTRACK 60", "MAHINDRA NOVO 605", "NAGISH 106"]
    if not df.empty:
        all_tractors = list(set(all_tractors + df["TRACTOR"].unique().tolist()))
    
    active_tractor = st.selectbox("Apna Tractor Chunein", all_tractors)
    st.divider()
    
    st.subheader("Nayi Entry Bharein")
    date = st.date_input("Tarik")
    d_name = st.text_input("Driver ka Naam")
    weight = st.number_input("Weight (KG)", min_value=0.0)
    rate = st.number_input("Rate", min_value=0.0, format="%.4f")
    diesel = st.number_input("Diesel Kharcha", min_value=0.0)
    d_pay = st.number_input("Driver Kharcha", min_value=0.0)
    other = st.number_input("Other Kharcha", min_value=0.0)

    if st.button("SAVE RECORD"):
        kamai = weight * rate
        total_inv = diesel + d_pay + other
        profit = kamai - total_inv
        new_row = {
            "DATE": str(date), "TRACTOR": active_tractor, "DRIVER_NAME": d_name,
            "ROUND": 1, "WEIGHT": weight, "RATE": rate, "KAMAI": round(kamai, 2),
            "DIESEL": diesel, "DRIVER_EXP": d_pay, "OTHER": other,
            "TOTAL_INV": round(total_inv, 2), "PROFIT": round(profit, 2)
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("Record Save Ho Gaya!")
        st.rerun()

# --- 5. Main Page Display ---
apply_custom_design(active_tractor)

# BIG TRACTOR NAME
st.markdown(f'<h1 class="tractor-title">{active_tractor}</h1>', unsafe_allow_html=True)

# Separate Data for Selected Tractor
t_df = df[df["TRACTOR"] == active_tractor]

# SEQUENCE (1. Weight, 2. Kamai, 3. Kharcha, 4. Profit)
col1, col2, col3, col4 = st.columns(4)
col1.metric("1. TOTAL WEIGHT", f"{t_df['WEIGHT'].sum():.2f} KG")
col2.metric("2. KUL KAMAI", f"₹{t_df['KAMAI'].sum():.2f}")
col3.metric("3. KUL KHARCHA", f"₹{t_df['TOTAL_INV'].sum():.2f}")
col4.metric("4. NET PROFIT", f"₹{t_df['PROFIT'].sum():.2f}")

st.divider()

# Records Table
st.subheader(f"Detailed Table: {active_tractor}")
st.dataframe(t_df, use_container_width=True)

# Delete Option
with st.expander("🗑️ Entry Delete Karein"):
    if not t_df.empty:
        row = st.selectbox("Kaun sa No. hatana hai?", t_df.index)
        if st.button("Confirm Delete"):
            df = df.drop(row)
            df.to_csv(DATA_FILE, index=False)
            st.warning("Entry Hata di gayi!")
            st.rerun()
