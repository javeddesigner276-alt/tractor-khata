import streamlit as st
import pandas as pd
import os

# --- 1. App Configuration ---
st.set_page_config(page_title="JAVED RANGHAD TRACTOR KHATA", layout="wide")

# --- 2. Custom Design (Bada Naam aur Asli Tractor Watermark) ---
def apply_custom_design(tractor_name):
    name_up = tractor_name.upper()
    
    # Direct links to real tractor images
    if "FARMTRACK" in name_up:
        # Farmtrack Blue Tractor
        img_url = "https://raw.githubusercontent.com/javeddesigner276-alt/tractor-khata/main/farmtrack_bg.jpg" 
        # Note: Agar ye link kaam na kare toh ye backup use karein:
        img_url = "https://th.bing.com/th/id/OIP.UeE_7mY6x89-f5v_F8Gj_AHaE8?rs=1&pid=ImgDetMain"
    elif "NOVO" in name_up or "605" in name_up:
        # Mahindra Novo Red Tractor
        img_url = "https://th.bing.com/th/id/OIP.H_6E4-x2-x-S_0tS3n08RAHaFj?rs=1&pid=ImgDetMain"
    else:
        # Default Tractor Image
        img_url = "https://th.bing.com/th/id/OIP.XG6nU7L2X_H0O7Q_y_XW_AHaE8?rs=1&pid=ImgDetMain"

    st.markdown(f"""
    <style>
    /* Background setup - Opacity 0.7 for clarity */
    .stApp {{
        background: linear-gradient(rgba(255,255,255,0.7), rgba(255,255,255,0.7)), 
                    url("{img_url}") !important;
        background-repeat: no-repeat !important;
        background-size: contain !important; /* Isse tractor pura dikhega bina kate */
        background-position: center !important;
        background-attachment: fixed !important;
    }}
    /* Tractor Name: BIG & RED */
    .tractor-title {{
        font-size: 110px !important;
        font-weight: 950 !important;
        color: #D32F2F !important;
        text-align: center !important;
        margin-top: -50px !important;
        margin-bottom: 20px !important;
        text-shadow: 4px 4px 12px rgba(0,0,0,0.4) !important;
        font-family: 'Arial Black', Gadget, sans-serif !important;
    }}
    /* Metrics sequence */
    [data-testid="stMetricValue"] {{
        font-size: 48px !important;
        color: #1A237E !important;
        font-weight: 900 !important;
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

# --- 4. Sidebar Menu (Nagish Removed) ---
with st.sidebar:
    st.header("🚜 DASHBOARD MENU")
    
    # Sirf Farmtrack aur Novo rakha hai
    base_tractors = ["FARMTRACK 60", "MAHINDRA NOVO 605"]
    
    if not df.empty:
        existing_tractors = df["TRACTOR"].unique().tolist()
        all_tractors = sorted(list(set(base_tractors + existing_tractors)))
        # Nagish ko filter se nikalne ke liye
        if "NAGISH 106" in all_tractors: all_tractors.remove("NAGISH 106")
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
            "DATE": str(date), "TRACTOR": active_tractor, "DRIVER_NAME": d_name,
            "ROUND": 1, "WEIGHT": weight, "RATE": rate, "KAMAI": round(kamai, 2),
            "DIESEL": diesel, "DRIVER_EXP": d_pay, "OTHER": other,
            "TOTAL_INV": round(total_inv, 2), "PROFIT": round(profit, 2)
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success(f"Saved for {active_tractor}!")
        st.rerun()

# --- 5. Main Page Display ---
apply_custom_design(active_tractor)

# BIG TRACTOR NAME
st.markdown(f'<h1 class="tractor-title">{active_tractor}</h1>', unsafe_allow_html=True)

t_df = df[df["TRACTOR"] == active_tractor]

# SEQUENCE (1. Weight, 2. Kamai, 3. Kharcha, 4. Profit)
col1, col2, col3, col4 = st.columns(4)
col1.metric("1. TOTAL WEIGHT", f"{t_df['WEIGHT'].sum():.2f} KG")
col2.metric("2. KUL KAMAI", f"₹{t_df['KAMAI'].sum():.2f}")
col3.metric("3. KUL KHARCHA", f"₹{t_df['TOTAL_INV'].sum():.2f}")
col4.metric("4. NET PROFIT", f"₹{t_df['PROFIT'].sum():.2f}")

st.divider()
st.subheader(f"📊 Detailed Table: {active_tractor}")
st.dataframe(t_df, use_container_width=True)

# Delete Option
st.divider()
with st.expander("🗑️ Entry Delete Karein (Galti Sudharein)"):
    if not t_df.empty:
        row_to_del = st.selectbox("Kaun sa Index hatana hai?", t_df.index)
        if st.button("Confirm Delete"):
            df = df.drop(row_to_del)
            df.to_csv(DATA_FILE, index=False)
            st.warning("Entry Hata di gayi!")
            st.rerun()
