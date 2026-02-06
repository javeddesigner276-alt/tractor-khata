import streamlit as st
import pandas as pd
import os

# App Configuration
st.set_page_config(page_title="Tractor Management System", layout="wide")

# Data File
DATA_FILE = "tractor_data.csv"

# Load Data
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    # Saare columns alag-alag define kiye hain
    df = pd.DataFrame(columns=["DATE", "TRACTOR", "ROUND", "WEIGHT", "RATE", "KAMAI", "DIESEL", "DRIVER", "OTHER", "TOTAL_INV", "PROFIT"])

st.title("🚜 Multi-Tractor Detailed Khata")

# --- Sidebar: Entry Form ---
with st.sidebar:
    st.header("Nayi Entry")
    
    existing_tractors = ["Farmtrack 60", "NAGISH 106"]
    if not df.empty:
        existing_tractors = list(set(existing_tractors + df["TRACTOR"].unique().tolist()))
    
    selected_tractor = st.selectbox("Tractor Chunein", existing_tractors)
    new_tractor = st.text_input("Ya Naya Tractor Likhein")
    final_tractor = new_tractor if new_tractor else selected_tractor
    
    date = st.text_input("Date", "06/02/2026")
    round_no = st.number_input("Round No.", min_value=1, step=1)
    weight = st.number_input("Weight (KG)", min_value=0.0)
    rate = st.number_input("Rate", min_value=0.0, format="%.4f")
    
    st.markdown("---")
    st.subheader("Kharche (Investment)")
    diesel = st.number_input("Diesel", min_value=0.0)
    driver = st.number_input("Driver", min_value=0.0)
    other = st.number_input("Other", min_value=0.0)

    if st.button("Save Record"):
        kamai = weight * rate
        total_inv = diesel + driver + other
        profit = kamai - total_inv
        
        new_row = {
            "DATE": date, "TRACTOR": final_tractor.upper(), "ROUND": round_no, 
            "WEIGHT": weight, "RATE": rate, "KAMAI": round(kamai, 2),
            "DIESEL": diesel, "DRIVER": driver, "OTHER": other, 
            "TOTAL_INV": round(total_inv, 2), "PROFIT": round(profit, 2)
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("Entry Save Ho Gayi!")
        st.rerun()

# --- Main Screen ---
st.subheader("Records (Detailed Table)")
# Filter option
all_tractors = df["TRACTOR"].unique()
selected_filter = st.multiselect("Tractor Filter", all_tractors, default=all_tractors)

display_df = df[df["TRACTOR"].isin(selected_filter)]

# Table display
st.dataframe(display_df, use_container_width=True)

# --- Summary Boxes ---
st.divider()
st.subheader("Summary (Kul Hisab)")
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Total Weight", f"{display_df['WEIGHT'].sum():.2f} KG")
with c2:
    st.metric("Total Kamai", f"₹{display_df['KAMAI'].sum():.2f}")
with c3:
    st.metric("Total Kharcha", f"₹{display_df['TOTAL_INV'].sum():.2f}")
with c4:
    net = display_df['PROFIT'].sum()
    st.metric("Net Profit", f"₹{net:.2f}", delta=f"Bachat")

# Individual Expenses Breakdown
st.write(f"**Kharche ka Byora:** Diesel: ₹{display_df['DIESEL'].sum()} | Driver: ₹{display_df['DRIVER'].sum()} | Other: ₹{display_df['OTHER'].sum()}")

# Delete Feature
st.divider()
if st.checkbox("Galti Sudharein"):
    idx = st.number_input("Row No. (Index)", min_value=0, max_value=len(df)-1 if len(df)>0 else 0)
    if st.button("Delete"):
        df = df.drop(df.index[idx])
        df.to_csv(DATA_FILE, index=False)
        st.rerun()
