import streamlit as st
import pandas as pd
import os

# --- 1. App Configuration ---
st.set_page_config(page_title="JAVED RANGHAD TRACTOR KHATA", layout="wide")

# Custom CSS for Professional Background & Text Visibility
def set_design():
    # Naya Reliable HD Tractor Background Link
    img_url = "https://images.pexels.com/photos/2933243/pexels-photo-2933243.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"

    st.markdown(f"""
    <style>
    /* 1. Background setup with Blur & Overlay */
    .stApp {{
        background: linear-gradient(rgba(255,255,255,0.75), rgba(255,255,255,0.75)), 
                    url("{img_url}");
        background-size: cover;
        background-position: center center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    
    /* 2. CHERRY RED EXTRA BIG TITLE */
    .big-cherry-title {{ 
        font-size: 90px !important; 
        font-weight: 900 !important; 
        color: #800000 !important; 
        text-align: center !important; 
        margin-top: -50px !important;
        text-shadow: 3px 3px 8px rgba(0,0,0,0.3) !important;
        font-family: 'Arial Black', sans-serif !important;
        text-transform: uppercase;
        letter-spacing: 2px;
    }}

    /* 3. SIDEBAR CHERRY COLOUR */
    [data-testid="stSidebar"] {{
        background-color: #800000 !important;
    }}
    
    /* 4. SIDEBAR TEXT (Headings/Labels) - WHITE */
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] p, [data-testid="stSidebar"] .stMarkdown p {{
        color: #FFFFFF !important;
        font-weight: bold !important;
    }}

    /* 5. INPUT BOXES TEXT - PURE BLACK */
    [data-testid="stSidebar"] input, [data-testid="stSidebar"] select, 
    [data-testid="stSidebar"] .stSelectbox div, [data-testid="stSidebar"] .stButton button p {{
        color: #000000 !important; 
        font-weight: 900 !important;
    }}

    /* 6. Metrics Box Design */
    [data-testid="stMetric"] {{
        background-color: rgba(255, 255, 255, 0.95) !important;
        border-radius: 12px !important;
        border-left: 8px solid #800000 !important;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.1) !important;
        padding: 10px !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. Data Management ---
DATA_FILE = "tractor_data.csv"
TRACTOR_LIST_FILE = "tractors.txt"

if os.path.exists(TRACTOR_LIST_FILE):
    with open(TRACTOR_LIST_FILE, "r") as f:
        base_tractors = [line.strip() for line in f.readlines()]
else:
    base_tractors = ["FARMTRACK 60", "MAHINDRA NOVO 605", "NAGISH 106"]

if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    cols = ["DATE", "TRACTOR", "DRIVER_NAME", "ROUND", "WEIGHT", "RATE", "KAMAI", "DIESEL", "DRIVER_EXP", "OTHER", "TOTAL_INV", "PROFIT"]
    df = pd.DataFrame(columns=cols)

# --- 3. Sidebar Setup ---
with st.sidebar:
    st.header("🚜 MENU")
    
    with st.expander("➕ ADD NEW TRACTOR"):
        new_t_name = st.text_input("Tractor Name Likhein")
        if st.button("ADD TRACTOR"):
            if new_t_name and new_t_name.upper() not in base_tractors:
                base_tractors.append(new_t_name.upper())
                with open(TRACTOR_LIST_FILE, "w") as f:
                    for t in base_tractors: f.write(t + "\n")
                st.success("Add Ho Gaya!")
                st.rerun()

    active_tractor = st.selectbox("Apna Tractor Chunein", base_tractors)
    st.divider()
    
    st.subheader("📝 Nayi Entry")
    date = st.date_input("Tarik")
    d_name = st.text_input("Driver ka Naam")
    weight = st.number_input("Weight (KG)", min_value=0.0)
    rate = st.number_input("Rate", min_value=0.0, format="%.4f")
    diesel = st.number_input("Diesel", min_value=0.0)
    d_pay = st.number_input("Driver Kharcha", min_value=0.0)
    other = st.number_input("Other Kharcha", min_value=0.0)

    if st.button("💾 SAVE RECORD"):
        kamai = weight * rate
        total_inv = diesel + d_pay + other
        new_row = {
            "DATE": str(date), "TRACTOR": active_tractor, "DRIVER_NAME": d_name,
            "ROUND": 1, "WEIGHT": weight, "RATE": rate, "KAMAI": round(kamai, 2),
            "DIESEL": diesel, "DRIVER_EXP": d_pay, "OTHER": other,
            "TOTAL_INV": round(total_inv, 2), "PROFIT": round(kamai - total_inv, 2)
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("Save Ho Gaya!")
        st.rerun()

# --- 4. Main Page Display ---
set_design()

# Title Display
st.markdown(f'<p class="big-cherry-title">{active_tractor}</p>', unsafe_allow_html=True)

t_df = df[df["TRACTOR"] == active_tractor]

# Performance Metrics
c1, c2, c3, c4 = st.columns(4)
c1.metric("1. TOTAL WEIGHT", f"{t_df['WEIGHT'].sum():.2f} KG")
c2.metric("2. KUL KAMAI", f"₹{t_df['KAMAI'].sum():.2f}")
c3.metric("3. KUL KHARCHA", f"₹{t_df['TOTAL_INV'].sum():.2f}")
c4.metric("4. NET PROFIT", f"₹{t_df['PROFIT'].sum():.2f}")

st.divider()
st.dataframe(t_df, use_container_width=True)

# Delete Option
with st.expander("🗑️ Galti Sudharein (Delete)"):
    if not t_df.empty:
        row = st.selectbox("Hatane wala Number", t_df.index)
        if st.button("Humesha ke liye hatayein"):
            df = df.drop(row)
            df.to_csv(DATA_FILE, index=False)
            st.rerun()
