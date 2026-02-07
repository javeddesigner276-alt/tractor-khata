import streamlit as st
import pandas as pd
import os

# --- 1. App Configuration ---
st.set_page_config(page_title="JAVED RANGHAD TRACTOR KHATA", layout="wide")

# --- 2. Custom Cherry Design (Full Visible Watermark) ---
def apply_custom_design(tractor_name):
    name_up = tractor_name.upper()
    
    # Asli Tractor Images
    if "FARMTRACK" in name_up:
        img_url = "https://th.bing.com/th/id/OIP.UeE_7mY6x89-f5v_F8Gj_AHaE8?rs=1&pid=ImgDetMain"
    elif "NOVO" in name_up or "605" in name_up:
        img_url = "https://th.bing.com/th/id/OIP.H_6E4-x2-x-S_0tS3n08RAHaFj?rs=1&pid=ImgDetMain"
    else:
        img_url = "https://images.pexels.com/photos/162637/tractor-agriculture-farm-drive-162637.jpeg"

    st.markdown(f"""
    <style>
    /* Full Visible Background with Cherry Tint */
    .stApp {{
        background: linear-gradient(rgba(100, 0, 0, 0.2), rgba(100, 0, 0, 0.2)), 
                    url("{img_url}") !important;
        background-repeat: no-repeat !important;
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
        background-color: #800000 !important; /* Cherry Red */
    }}

    /* Title: WHITE & HUGE */
    .tractor-title {{
        font-size: 100px !important;
        font-weight: 900 !important;
        color: #FFFFFF !important; 
        text-align: center !important;
        margin-top: -30px !important;
        text-shadow: 4px 4px 15px rgba(0,0,0,1) !important;
        font-family: 'Arial Black', sans-serif !important;
    }}

    /* Metrics Cards: White */
    [data-testid="stMetric"] {{
        background-color: rgba(255, 255, 255, 0.98) !important;
        padding: 20px !important;
        border-radius: 12px !important;
        box-shadow: 0px 8px 25px rgba(0,0,0,0.8) !important;
        border-top: 8px solid #D2143A !important;
    }}
    
    [data-testid="stMetricLabel"] {{
        color: #000000 !important;
        font-size: 20px !important;
        font-weight: bold !important;
    }}

    [data-testid="stMetricValue"] {{
        color: #8B0000 !important; 
        font-size: 45px !important;
        font-weight: 900 !important;
    }}

    /* Sidebar Dark Cherry */
    section[data-testid="stSidebar"] {{
        background-color: #300000 !important;
    }}
    
    .stDataFrame, div[data-testid="stExpander"] {{
        background-color: white !important;
        border-radius: 10px !important;
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
    st.header("🚜 JAVED RANGHAD")
    all_tractors = ["FARMTRACK 60", "MAHINDRA NOVO 605"]
    active_tractor = st.selectbox("Tractor Chunein", all_tractors)
    st.divider()
    
    st.subheader("📝 Nayi Entry")
    date = st.date_input("Tarik")
    d_name = st.text_input("Driver Name")
    weight = st.number_input("Weight (KG)", min_value=0.0)
    rate = st.number_input("Rate", min_value=0.0, format="%.4f")
    
    st.markdown("**Kharche**")
    diesel = st.number_input("Diesel", min_value=0.0)
    d_pay = st.number_input("Driver Exp", min_value=0.0)
    other = st.number_input("Other", min_value=0.0)

    if st.button("💾 SAVE"):
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
        st.success("Saved!")
        st.rerun()

# --- 5. Main Page ---
apply_custom_design(active_tractor)
st.markdown(f'<h1 class="tractor-title">{active_tractor}</h1>', unsafe_allow_html=True)

t_df = df[df["TRACTOR"] == active_tractor]

c1, c2, c3, c4 = st.columns(4)
c1.metric("1. TOTAL WEIGHT", f"{t_df['WEIGHT'].sum():.2f} KG")
c2.metric("2. KUL KAMAI", f"₹{t_df['KAMAI'].sum():.2f}")
c3.metric("3. KUL KHARCHA", f"₹{t_df['TOTAL_INV'].sum():.2f}")
c4.metric("4. NET PROFIT", f"₹{t_df['PROFIT'].sum():.2f}")

st.divider()
st.subheader("📊 Data Table")
st.dataframe(t_df, use_container_width=True)

with st.expander("🗑️ Delete"):
    if not t_df.empty:
        row = st.selectbox("Index Chunein", t_df.index)
        if st.button("Confirm"):
            df = df.drop(row)
            df.to_csv(DATA_FILE, index=False)
            st.rerun()
