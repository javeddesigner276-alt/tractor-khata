import streamlit as st
import pandas as pd
import os

# --- 1. App Configuration ---
st.set_page_config(page_title="JAVED RANGHAD TRACTOR KHATA", layout="wide")

# Custom CSS for Big Title & Sequential Metrics
def set_design(tractor_name):
    img_url = ""
    if "FARMTRACK" in tractor_name.upper():
        img_url = "https://th.bing.com/th/id/OIP.XG6nU7L2X_H0O7Q_y_XW_AHaE8?rs=1&pid=ImgDetMain"
    elif "NOVO" in tractor_name.upper() or "605" in tractor_name:
        img_url = "https://th.bing.com/th/id/OIP.7_z_Y-8Qk2P8Wf6y5A6Q-AHaE8?rs=1&pid=ImgDetMain"
    else:
        img_url = "https://cdn.pixabay.com/photo/2014/07/06/17/20/tractor-385681_1280.jpg"

    st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(255,255,255,0.85), rgba(255,255,255,0.85)), 
                    url("{img_url}");
        background-repeat: no-repeat;
        background-size: cover;
        background-attachment: fixed;
    }}
    /* Tractor Name Double Size */
    .big-title {{ 
        font-size: 80px; 
        font-weight: 800; 
        color: #1E3A8A; 
        text-align: center; 
        margin-top: -50px;
        text-shadow: 3px 3px 6px #aaa;
        font-family: 'Arial Black', Gadget, sans-serif;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. Data Management ---
DATA_FILE = "tractor_data.csv"
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    cols = ["DATE", "TRACTOR", "DRIVER_NAME", "ROUND", "WEIGHT", "RATE", "KAMAI", "DIESEL", "DRIVER_EXP", "OTHER", "TOTAL_INV", "PROFIT"]
    df = pd.DataFrame(columns=cols)

# --- 3. Sidebar Setup ---
with st.sidebar:
    st.header("🚜 MENU")
    all_tractors = ["FARMTRACK 60", "MAHINDRA NOVO 605"]
    if not df.empty:
        all_tractors = list(set(all_tractors + df["TRACTOR"].unique().tolist()))
    
    active_tractor = st.selectbox("Apna Tractor Chunein", all_tractors)
    st.divider()
    
    st.subheader("Nayi Entry")
    date = st.date_input("Tarik")
    d_name = st.text_input("Driver ka Naam")
    weight = st.number_input("Weight (KG)", min_value=0.0)
    rate = st.number_input("Rate", min_value=0.0, format="%.4f")
    diesel = st.number_input("Diesel", min_value=0.0)
    d_pay = st.number_input("Driver Kharcha", min_value=0.0)
    other = st.number_input("Other", min_value=0.0)

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
        st.success("Save Ho Gaya!")
        st.rerun()

# --- 4. Main Page Display ---
set_design(active_tractor)
st.markdown(f'<p class="big-title">{active_tractor}</p>', unsafe_allow_html=True)

# Requirement 1: Separate Data
t_df = df[df["TRACTOR"] == active_tractor]

# Requirement 1 & 2: Sequence of Metrics (1. Weight, 2. Kamai, 3. Kharcha, 4. Profit)
c1, c2, c3, c4 = st.columns(4)
c1.metric("1. TOTAL WEIGHT", f"{t_df['WEIGHT'].sum():.2f} KG")
c2.metric("2. KUL KAMAI", f"₹{t_df['KAMAI'].sum():.2f}")
c3.metric("3. KUL KHARCHA", f"₹{t_df['TOTAL_INV'].sum():.2f}")
c4.metric("4. NET PROFIT", f"₹{t_df['PROFIT'].sum():.2f}")

st.divider()
st.dataframe(t_df, use_container_width=True)

# Delete Option
with st.expander("Galti Sudharein (Delete)"):
    if not t_df.empty:
        row = st.selectbox("Kaun sa No. hatana hai?", t_df.index)
        if st.button("Humesha ke liye hatayein"):
            df = df.drop(row)
            df.to_csv(DATA_FILE, index=False)
            st.rerun()
