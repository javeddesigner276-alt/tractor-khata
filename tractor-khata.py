import streamlit as st
import pandas as pd
import os

# --- 1. App Config ---
st.set_page_config(page_title="JAVED RANGHAD TRACTOR KHATA", layout="wide")

# --- 2. Design Logic ---
def apply_design(tractor_name):
    name_up = tractor_name.upper()
    if "FARMTRACK" in name_up:
        img = "https://th.bing.com/th/id/OIP.UeE_7mY6x89-f5v_F8Gj_AHaE8?rs=1&pid=ImgDetMain"
    elif "605" in name_up or "NOVO" in name_up:
        img = "https://th.bing.com/th/id/OIP.H_6E4-x2-x-S_0tS3n08RAHaFj?rs=1&pid=ImgDetMain"
    else:
        img = "https://images.pexels.com/photos/162637/tractor-agriculture-farm-drive-162637.jpeg"

    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("{img}") !important;
        background-repeat: no-repeat !important;
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }}
    [data-testid="stSidebar"] {{
        background-color: #800000 !important;
    }}
    [data-testid="stSidebar"] * {{
        color: white !important;
    }}
    .tractor-title {{
        font-size: 80px !important;
        font-weight: 900 !important;
        color: white !important;
        text-align: center !important;
        text-shadow: 4px 4px 10px black !important;
        margin-top: -50px !important;
    }}
    [data-testid="stMetric"] {{
        background-color: rgba(255, 255, 255, 0.9) !important;
        padding: 15px !important;
        border-radius: 10px !important;
        border-left: 8px solid #800000 !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. Data File ---
DATA_FILE = "tractor_data.csv"
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=["DATE", "TRACTOR", "DRIVER_NAME", "ROUND", "WEIGHT", "RATE", "KAMAI", "DIESEL", "DRIVER_EXP", "OTHER", "TOTAL_INV", "PROFIT"])

# --- 4. Sidebar ---
with st.sidebar:
    st.header("🚜 JAVED RANGHAD")
    active_tractor = st.selectbox("Tractor Chunein", ["FARMTRACK 60", "MAHINDRA NOVO 605"])
    st.divider()
    
    st.subheader("📝 Nayi Entry")
    date = st.date_input("Tarik")
    d_name = st.text_input("Driver")
    weight = st.number_input("Weight (KG)", min_value=0.0)
    rate = st.number_input("Rate", min_value=0.0)
    
    st.markdown("---")
    diesel = st.number_input("Diesel", min_value=0.0)
    d_pay = st.number_input("Driver Exp", min_value=0.0)
    other = st.number_input("Other", min_value=0.0)

    if st.button("💾 SAVE"):
        kamai = weight * rate
        total_inv = diesel + d_pay + other
        new_row = {
            "DATE": str(date), "TRACTOR": active_tractor, "DRIVER_NAME": d_name,
            "ROUND": 1, "WEIGHT": weight, "RATE": rate, "KAMAI": kamai,
            "DIESEL": diesel, "DRIVER_EXP": d_pay, "OTHER": other,
            "TOTAL_INV": total_inv, "PROFIT": (kamai - total_inv)
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("Saved!")
        st.rerun()

# --- 5. Main Display ---
apply_design(active_tractor)
st.markdown(f'<h1 class="tractor-title">{active_tractor}</h1>', unsafe_allow_html=True)

t_df = df[df["TRACTOR"] == active_tractor]

c1, c2, c3, c4 = st.columns(4)
c1.metric("TOTAL WEIGHT", f"{t_df['WEIGHT'].sum():.2f}")
c2.metric("KUL KAMAI", f"₹{t_df['KAMAI'].sum():.2f}")
c3.metric("KUL KHARCHA", f"₹{t_df['TOTAL_INV'].sum():.2f}")
c4.metric("NET PROFIT", f"₹{t_df['PROFIT'].sum():.2f}")

st.divider()
st.dataframe(t_df, use_container_width=True)

with st.expander("🗑️ Delete"):
    if not t_df.empty:
        idx = st.selectbox("Index", t_df.index)
        if st.button("Delete Now"):
            df = df.drop(idx)
            df.to_csv(DATA_FILE, index=False)
            st.rerun()
