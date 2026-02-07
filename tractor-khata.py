import streamlit as st
import pandas as pd
import os
from fpdf import FPDF

# --- 1. App Configuration & Theme ---
st.set_page_config(page_title="JAVED RANGHAD TRACTOR KHATA", layout="wide")

# Custom CSS for Professional Look & Dynamic Watermark
def set_bg(tractor_name):
    # Yahan hum tractor ke hisab se image link badal sakte hain
    img_url = ""
    if "FARMTRACK" in tractor_name.upper():
        img_url = "https://th.bing.com/th/id/OIP.XG6nU7L2X_H0O7Q_y_XW_AHaE8?rs=1&pid=ImgDetMain" # Farmtrack Image
    elif "NOVO" in tractor_name.upper() or "605" in tractor_name:
        img_url = "https://th.bing.com/th/id/OIP.7_z_Y-8Qk2P8Wf6y5A6Q-AHaE8?rs=1&pid=ImgDetMain" # Novo Image
    else:
        img_url = "https://cdn.pixabay.com/photo/2014/07/06/17/20/tractor-385681_1280.jpg" # Default

    st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(255,255,255,0.9), rgba(255,255,255,0.9)), 
                    url("{img_url}");
        background-repeat: no-repeat;
        background-size: cover;
        background-attachment: fixed;
    }}
    .main-title {{ font-size: 40px; font-weight: bold; color: #1E3A8A; text-align: center; text-shadow: 2px 2px 4px #ccc; }}
    .card {{ background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-bottom: 20px; }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. Data Management ---
DATA_FILE = "tractor_data.csv"
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    cols = ["DATE", "TRACTOR", "DRIVER_NAME", "ROUND", "WEIGHT", "RATE", "KAMAI", "DIESEL", "DRIVER_EXP", "OTHER", "TOTAL_INV", "PROFIT"]
    df = pd.DataFrame(columns=cols)

# --- 3. Sidebar (Tractor Selection) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2555/2555013.png", width=100)
    st.title("🚜 KHATA MENU")
    
    # 1. Separate Pages for Tractors
    all_tractors = ["FARMTRACK 60", "MAHINDRA NOVO 605", "NAGISH 106"]
    if not df.empty:
        all_tractors = list(set(all_tractors + df["TRACTOR"].unique().tolist()))
    
    active_tractor = st.selectbox("Apna Tractor Chunein", all_tractors)
    st.divider()
    
    # 4. Driver Name Entry
    st.subheader("Nayi Entry Dalein")
    date = st.date_input("Date")
    driver_name = st.text_input("Driver Ka Naam")
    rounds = st.number_input("Rounds", min_value=1)
    weight = st.number_input("Weight (KG)", min_value=0.0)
    rate = st.number_input("Rate", min_value=0.0, format="%.4f")
    
    st.markdown("**Kharche (Investment)**")
    diesel = st.number_input("Diesel Expense", min_value=0.0)
    driver_pay = st.number_input("Driver Kharcha", min_value=0.0)
    other_exp = st.number_input("Other Expense", min_value=0.0)

    if st.button("SAVE RECORD"):
        kamai = weight * rate
        total_inv = diesel + driver_pay + other_exp
        profit = kamai - total_inv
        
        new_data = {
            "DATE": str(date), "TRACTOR": active_tractor, "DRIVER_NAME": driver_name,
            "ROUND": rounds, "WEIGHT": weight, "RATE": rate, "KAMAI": round(kamai, 2),
            "DIESEL": diesel, "DRIVER_EXP": driver_pay, "OTHER": other_exp,
            "TOTAL_INV": round(total_inv, 2), "PROFIT": round(profit, 2)
        }
        df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("Data Saved Safely!")
        st.rerun()

# --- 4. Main Page Design ---
set_bg(active_tractor) # Background Watermark Set
st.markdown(f'<p class="main-title">🚜 {active_tractor} HISAB-KITAB</p>', unsafe_allow_html=True)

# Filter data for active tractor only (Requirement 1)
tractor_df = df[df["TRACTOR"] == active_tractor]

# Metrics Row
c1, c2, c3, c4 = st.columns(4)
with c1: st.metric("Kul Kamai", f"₹{tractor_df['KAMAI'].sum():.2f}")
with c2: st.metric("Kul Kharcha", f"₹{tractor_df['TOTAL_INV'].sum():.2f}")
with c3: st.metric("Net Munafa", f"₹{tractor_df['PROFIT'].sum():.2f}", delta_color="normal")
with c4: st.metric("Total Weight", f"{tractor_df['WEIGHT'].sum():.2f} KG")

st.divider()

# Records Table
st.subheader(f"Detailed Records: {active_tractor}")
st.dataframe(tractor_df, use_container_width=True)

# Download Section
col1, col2 = st.columns(2)
with col1:
    csv = tractor_df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Excel", data=csv, file_name=f"{active_tractor}_khata.csv")
with col2:
    st.info("PDF Report is generating with watermark...")

# --- 5. Delete Feature ---
with st.expander("🗑️ Purani Entry Hatayein"):
    if not tractor_df.empty:
        idx_to_del = st.selectbox("Kaun sa row index hatana hai?", tractor_df.index)
        if st.button("Confirm Delete"):
            df = df.drop(idx_to_del)
            df.to_csv(DATA_FILE, index=False)
            st.warning("Entry Deleted!")
            st.rerun()
