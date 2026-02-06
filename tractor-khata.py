import streamlit as st
import pandas as pd
import os
from fpdf import FPDF # PDF banane ke liye

# 1. App Configuration - Name Update
st.set_page_config(page_title="JAVED RANGHAD TRACTOR KHATA", layout="wide")

# Data File
DATA_FILE = "tractor_data.csv"

# Load Data
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=["DATE", "TRACTOR", "ROUND", "WEIGHT", "RATE", "KAMAI", "DIESEL", "DRIVER", "OTHER", "TOTAL_INV", "PROFIT"])

# 2. App Title - Name Update
st.title("🚜 JAVED RANGHAD TRACTOR KHATA")

# --- Sidebar: Entry Form ---
with st.sidebar:
    st.header("Nayi Entry Dalein")
    
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
all_tractors = df["TRACTOR"].unique()
selected_filter = st.multiselect("Tractor Filter", all_tractors, default=all_tractors)

display_df = df[df["TRACTOR"].isin(selected_filter)]
st.dataframe(display_df, use_container_width=True)

# --- 3. PDF Generation Function ---
def create_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="JAVED RANGHAD TRACTOR KHATA REPORT", ln=True, align='C')
    pdf.set_font("Arial", size=10)
    pdf.ln(10)
    
    # Table Header
    cols = ["DATE", "TRACTOR", "WEIGHT", "KAMAI", "TOTAL_INV", "PROFIT"]
    for col in cols:
        pdf.cell(32, 10, col, 1)
    pdf.ln()
    
    # Table Rows
    for i, row in data.iterrows():
        pdf.cell(32, 10, str(row['DATE']), 1)
        pdf.cell(32, 10, str(row['TRACTOR']), 1)
        pdf.cell(32, 10, str(row['WEIGHT']), 1)
        pdf.cell(32, 10, str(row['KAMAI']), 1)
        pdf.cell(32, 10, str(row['TOTAL_INV']), 1)
        pdf.cell(32, 10, str(row['PROFIT']), 1)
        pdf.ln()
    
    return pdf.output(dest='S').encode('latin-1')

# --- Download Buttons ---
if not display_df.empty:
    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        csv = display_df.to_csv(index=False).encode('utf-8')
        st.download_button(label="📥 Download Excel (CSV)", data=csv, file_name='tractor_khata.csv')
    with col_dl2:
        pdf_bytes = create_pdf(display_df)
        st.download_button(label="📄 Download PDF Report", data=pdf_bytes, file_name="tractor_report.pdf", mime="application/pdf")

# --- Summary Boxes ---
st.divider()
st.subheader("Summary (Kul Hisab)")
c1, c2, c3, c4 = st.columns(4)
with c1: st.metric("Total Weight", f"{display_df['WEIGHT'].sum():.2f} KG")
with c2: st.metric("Total Kamai", f"₹{display_df['KAMAI'].sum():.2f}")
with c3: st.metric("Total Kharcha", f"₹{display_df['TOTAL_INV'].sum():.2f}")
with c4: st.metric("Net Profit", f"₹{display_df['PROFIT'].sum():.2f}")# --- Delete Feature (Ab Table ke niche dikhega) ---
st.divider()
st.subheader("🗑️ Record Hatayein (Delete)")
delete_check = st.checkbox("Galti Sudharne ke liye yahan click karein")

if delete_check:
    if not df.empty:
        row_to_delete = st.number_input("Kaun sa Row No. hatana hai?", min_value=0, max_value=len(df)-1, step=1)
        if st.button("Hamesha ke liye Delete karein"):
            df = df.drop(df.index[row_to_delete])
            df.to_csv(DATA_FILE, index=False)
            st.success(f"Row {row_to_delete} delete ho gayi!")
            st.rerun()
    else:
        st.warning("Abhi koi data nahi hai delete karne ke liye.")

