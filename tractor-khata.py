import streamlit as st
import pandas as pd
import os

# --- 1. App Configuration ---
st.set_page_config(page_title="JAVED RANGHAD TRACTOR KHATA", layout="wide")

# Custom CSS for Big Cherry Title & Nagish-style Watermark
def set_design(tractor_name):
    img_url = ""
    name_up = tractor_name.upper()
    
    # Nagish wala logic ab sabke liye (Background/Watermark)
    if "FARMTRACK" in name_up:
        img_url = "https://th.bing.com/th/id/OIP.UeE_7mY6x89-f5v_F8Gj_AHaE8?rs=1&pid=ImgDetMain"
    elif "NOVO" in name_up or "605" in name_up:
        img_url = "https://th.bing.com/th/id/OIP.H_6E4-x2-x-S_0tS3n08RAHaFj?rs=1&pid=ImgDetMain"
    elif "NAGISH" in name_up:
        img_url = "https://th.bing.com/th/id/OIP.XG6nU7L2X_H0O7Q_y_XW_AHaE8?rs=1&pid=ImgDetMain"
    else:
        img_url = "https://cdn.pixabay.com/photo/2014/07/06/17/20/tractor-385681_1280.jpg"

    st.markdown(f"""
    <style>
    /* Background setup jaisa Nagish me tha */
    .stApp {{
        background: linear-gradient(rgba(255,255,255,0.85), rgba(255,255,255,0.85)), 
                    url("{img_url}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    
    /* Tractor Name: CHERRY COLOUR & EXTRA BIG (Double Size) */
    .big-cherry-title {{ 
        font-size: 100px !important; /* Size aur badi kar di */
        font-weight: 900 !important; 
        color: #800000 !important; /* Cherry Red Colour */
        text-align: center !important; 
        margin-top: -60px !important;
        text-shadow: 4px 4px 8px rgba(0,0,0,0.2) !important;
        font-family: 'Arial Black', Gadget, sans-serif !important;
        text-transform: uppercase;
    }}

    /* Sidebar: Cherry Red */
    [data-testid="stSidebar"] {{
        background-color: #800000 !important;
    }}
    [data-testid="stSidebar"] * {{
        color: white !important;
    }}
    
    /* Metrics box design */
    [data-testid="stMetric"] {{
        background-color: white !important;
        border-radius: 10px !important;
        border-left: 8px solid #800000 !important;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1) !important;
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
    all_tractors = ["FARMTRACK 60", "MAHINDRA NOVO 605", "NAGISH 106"]
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
set_design(active_tractor)

# Yahan Cherry color aur Bada Title apply ho raha hai
st.markdown(f'<p class="big-cherry-title">{active_tractor}</p>', unsafe_allow_html=True)

t_df = df[df["TRACTOR"] == active_tractor]

# Sequence of Metrics (1. Weight, 2. Kamai, 3. Kharcha, 4. Profit)
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
