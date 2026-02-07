import streamlit as st
import pandas as pd
import os

# --- 1. App Configuration ---
st.set_page_config(page_title="JAVED RANGHAD TRACTOR KHATA", layout="wide")

# --- 2. Custom CSS (Sidebar Cherry & Design) ---
st.markdown("""
<style>
    /* Sidebar: Pakka Cherry Red */
    [data-testid="stSidebar"] {
        background-color: #800000 !important;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Main Page: Clean Look */
    .stApp {
        background-color: #f5f5f5 !important;
    }

    /* Title: Big and Bold */
    .main-title {
        font-size: 60px !important;
        font-weight: 900 !important;
        color: #800000 !important;
        text-align: center !important;
        margin-top: -20px !important;
        font-family: 'Arial Black', sans-serif !important;
    }

    /* Metrics: White Cards with Red Border */
    [data-testid="stMetric"] {
        background-color: white !important;
        padding: 20px !important;
        border-radius: 12px !important;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.1) !important;
        border-top: 5px solid #800000 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. Data Loading ---
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
    weight = st.number_input("Weight (KG)", min_value=0.0)
    rate = st.number_input("Rate", min_value=0.0, format="%.4f")
    
    st.markdown("---")
    st.markdown("**Kharche (Expenses)**")
    diesel = st.number_input("Diesel", min_value=0.0)
    d_pay = st.number_input("Driver Exp", min_value=0.0)
    other = st.number_input("Other", min_value=0.0)

    if st.button("💾 SAVE RECORD"):
        kamai = weight * rate
        total_inv = diesel + d_pay + other
        new_data = pd.DataFrame([{
            "DATE": str(date), "TRACTOR": active_tractor, "DRIVER_NAME": d_name,
            "ROUND": 1, "WEIGHT": weight, "RATE": rate, "KAMAI": round(kamai, 2),
            "DIESEL": diesel, "DRIVER_EXP": d_pay, "OTHER": other,
            "TOTAL_INV": round(total_inv, 2), "PROFIT": round(kamai - total_inv, 2)
        }])
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("Save Ho Gaya!")
        st.rerun()

# --- 5. Main Dashboard ---
# Tractor Image and Title
if "FARMTRACK" in active_tractor:
    st.image("https://th.bing.com/th/id/OIP.UeE_7mY6x89-f5v_F8Gj_AHaE8?rs=1&pid=ImgDetMain", width=400)
else:
    st.image("https://th.bing.com/th/id/OIP.H_6E4-x2-x-S_0tS3n08RAHaFj?rs=1&pid=ImgDetMain", width=400)

st.markdown(f'<h1 class="main-title">{active_tractor}</h1>', unsafe_allow_html=True)

# Data Filter
t_df = df[df["TRACTOR"] == active_tractor]

# Metrics
c1, c2, c3, c4 = st.columns(4)
c1.metric("1. TOTAL WEIGHT", f"{t_df['WEIGHT'].sum():.2f} KG")
c2.metric("2. KUL KAMAI", f"₹{t_df['KAMAI'].sum():.2f}")
c3.metric("3. KUL KHARCHA", f"₹{t_df['TOTAL_INV'].sum():.2f}")
c4.metric("4. NET PROFIT", f"₹{t_df['PROFIT'].sum():.2f}")

st.divider()
st.subheader("📊 Detailed Table")
st.dataframe(t_df, use_container_width=True)

# Delete Row
with st.expander("🗑️ Entry Delete"):
    if not t_df.empty:
        idx = st.selectbox("Hataane ke liye chunein", t_df.index)
        if st.button("Confirm Delete"):
            df = df.drop(idx)
            df.to_csv(DATA_FILE, index=False)
            st.rerun()
