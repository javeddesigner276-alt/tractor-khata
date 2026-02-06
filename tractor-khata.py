import streamlit as st
import pandas as pd
import os

# App ka Title aur Layout
st.set_page_config(page_title="Farmtrack 60 Khata", layout="wide")
st.title("🚜 Farmtrack 60 - Hisab Kitab")

# Data Save karne ke liye file
DATA_FILE = "tractor_data.csv"

# Purana data load karna
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=["DATE", "ROUND", "WEIGHT", "RATE", "TOTAL_KAMAI", "DIESEL", "DRIVER", "OTHER", "PROFIT"])

# --- Nayi Entry Ka Form ---
with st.sidebar:
    st.header("Nayi Entry Dalein")
    date = st.text_input("Date", "06/02/2026")
    round_no = st.number_input("Round Sr. No.", min_value=1, step=1)
    weight = st.number_input("Weight (KG)", min_value=0.0)
    rate = st.number_input("Rate", min_value=0.0, format="%.4f")
    diesel = st.number_input("Diesel Amount", min_value=0.0)
    driver = st.number_input("Driver Amount", min_value=0.0)
    other = st.number_input("Other Kharcha", min_value=0.0)

    if st.button("Save Record"):
        total_kamai = weight * rate
        total_kharcha = diesel + driver + other
        profit = total_kamai - total_kharcha
        
        new_row = {
            "DATE": date, "ROUND": round_no, "WEIGHT": weight, 
            "RATE": rate, "TOTAL_KAMAI": round(total_kamai, 2),
            "DIESEL": diesel, "DRIVER": driver, "OTHER": other, 
            "PROFIT": round(profit, 2)
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("Entry Save Ho Gayi!")

# --- Table Display (Excel Jaisa) ---
st.subheader("Records (Detailed Table)")
st.dataframe(df, use_container_width=True)

# --- Summary (Niche Wala Lal Hisaba) ---
st.divider()
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Kul Weight", f"{df['WEIGHT'].sum()} KG")
with col2:
    st.metric("Total Kamai", f"₹{df['TOTAL_KAMAI'].sum():.2f}")
with col3:
    st.metric("Net Profit", f"₹{df['PROFIT'].sum():.2f}", delta_color="normal")