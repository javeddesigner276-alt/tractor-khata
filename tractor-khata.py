import streamlit as st
import pandas as pd
import os

# --- 1. App Configuration ---
st.set_page_config(page_title="JAVED RANGHAD TRACTOR KHATA", layout="wide")

# --- 2. Custom Design (Bada Naam aur Watermark) ---
def apply_custom_design(tractor_name):
    # Naye aur High-Quality Image Links jo load honge
    name_up = tractor_name.upper()
    
    # Default Image
    img_url = "https://images.unsplash.com/photo-1530268578403-df6e89da0d30?q=80&w=2070&auto=format&fit=crop"
    
    if "FARMTRACK" in name_up:
        # Blue Tractor / Farmtrack Style
        img_url = "https://images.unsplash.com/photo-1594411126605-7208f237f37e?q=80&w=2072&auto=format&fit=crop"
    elif "NOVO" in name_up or "605" in name_up:
        # Red/Modern Tractor / Novo Style
        img_url = "https://images.unsplash.com/photo-1622329606883-9b0f69a5015b?q=80&w=1974&auto=format&fit=crop"
    elif "NAGISH" in name_up:
        # Heavy Duty / Nagish Style
        img_url = "https://images.unsplash.com/photo-1535249416175-df0567ef294f?q=80&w=2070&auto=format&fit=crop"

    st.markdown(f"""
    <style>
    /* Background Watermark Settings */
    .stApp {{
        background: linear-gradient(rgba(255,255,255,0.88), rgba(255,255,255,0.88)), url("{img_url}");
        background-repeat: no-repeat;
        background-size: cover;
        background-attachment: fixed;
    }}
    /* Tractor Name: DOUBLE SIZE (BIG) - RED COLOR */
    .tractor-title {{
        font-size: 100px !important;
        font-weight: 900 !important;
        color: #B22222 !important;
        text-align: center !important;
        margin-top: -40px !important;
        margin-bottom: 10px !important;
        text-shadow: 3px 3px 8px rgba(0,0,0,0.2);
        font-family: 'Impact', sans-serif;
        letter-spacing: 2px;
    }}
    /* Metrics Styling - DARK BLUE */
    [data-testid="stMetricValue"] {{
        font-size: 45px !important;
        color: #000080 !important;
        font-weight: bold !important;
    }}
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {{
        background-color: #f0f2f6;
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
    
    # Default list
    base_tractors = ["FARMTRACK 60", "MAHINDRA NOVO 605", "NAGISH 106"]
    
    # Add any new tractors found in the data
    if not df.empty:
        existing_tractors = df["TRACTOR"].unique().tolist()
        all_tractors = sorted(list(set(base_tractors + existing_tractors)))
    else:
        all_tractors = base_tractors
    
    active_tractor = st.selectbox("Apna Tractor Chunein", all_tractors)
    st.divider()
    
    st.subheader("📝 Nayi Entry Bharein")
    date = st.date_input("Tarik")
    d_name = st.text_input("Driver ka Naam")
    weight = st.number_input("Weight (KG)", min_value=0.0, step=100.0)
    rate = st.number_input("Rate", min_value=0.0, format="%.4f", step=0.001)
    
    st.markdown("---")
    st.markdown("**Kharche (Investment)**")
    diesel = st.number_input("Diesel Kharcha", min_value=0.0, step=50.0)
    d_pay = st.number_input("Driver Kharcha", min_value=0.0, step=50.0)
    other = st.number_input("Other Kharcha", min_value=0.0, step=10.0)

    if st.button("💾 SAVE RECORD"):
        kamai = weight * rate
        total_inv = diesel + d_pay + other
        profit = kamai - total_inv
        
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
            "PROFIT": round(profit, 2)
        }
        
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success(f"Record Saved for {active_tractor}!")
        st.rerun()

# --- 5. Main Page Display ---
apply_custom_design(active_tractor)

# BIG TRACTOR NAME (Top Center)
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
st.subheader(f"📊 Detailed Table: {active_tractor}")
st.dataframe(t_df, use_container_width=True)

# Delete Option
st.divider()
with st.expander("🗑️ Entry Delete Karein (Galti Sudharein)"):
    if not t_df.empty:
        # Selection using the original index for accurate deletion
        row_to_del = st.selectbox("Kaun sa Index hatana hai?", t_df.index)
        if st.button("Confirm Delete"):
            df = df.drop(row_to_del)
            df.to_csv(DATA_FILE, index=False)
            st.warning("Entry Hata di gayi!")
            st.rerun()
    else:
        st.info("Abhi koi data nahi hai delete karne ke liye.")
