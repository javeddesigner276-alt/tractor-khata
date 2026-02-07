import streamlit as st
import pandas as pd
import os

# --- 1. App Configuration ---
st.set_page_config(page_title="JAVED RANGHAD TRACTOR KHATA", layout="wide")

# Custom CSS for Design & Fixing Visibility
def set_design(tractor_name):
    img_url = ""
    name_up = tractor_name.upper()
    
    # Background logic
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
    /* Background setup */
    .stApp {{
        background: linear-gradient(rgba(255,255,255,0.85), rgba(255,255,255,0.85)), 
                    url("{img_url}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    
    /* CHERRY RED BIG TITLE */
    .big-cherry-title {{ 
        font-size: 100px !important; 
        font-weight: 950 !important; 
        color: #800000 !important; 
        text-align: center !important; 
        margin-top: -60px !important;
        text-shadow: 4px 4px 10px rgba(0,0,0,0.2) !important;
        font-family: 'Arial Black', sans-serif !important;
        text-transform: uppercase;
    }}

    /* SIDEBAR CHERRY COLOUR */
    [data-testid="stSidebar"] {{
        background-color: #800000 !important;
    }}
    
    /* SIDEBAR HEADINGS & LABELS - WHITE */
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] .stMarkdown p {{
        color: #FFFFFF !important;
        font-weight: bold !important;
    }}

    /* INPUT BOX TEXT - PURE BLACK */
    [data-testid="stSidebar"] input, 
    [data-testid="stSidebar"] select, 
    [data-testid="stSidebar"] .stSelectbox div,
    [data-testid="stSidebar"] .stButton button p {{
        color: #000000 !important; 
        font-weight: 900 !important;
    }}

    /* FIX FOR ADD TRACTOR BUTTON TEXT */
    div.stButton > button {{
        color: #000000 !important;
        background-color: #FFFFFF !important;
        border-radius: 5px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. Data Management ---
DATA_FILE = "tractor_data.csv"
TRACTOR_LIST_FILE = "tractors.txt"

# Load Tractor List
if os.path.exists(TRACTOR_LIST_FILE):
    with open(TRACTOR_LIST_FILE, "r") as f:
        base_tractors = [line.strip() for line in f.readlines()]
else:
    base_tractors = ["FARMTRACK 60", "MAHINDRA NOVO 605", "NAGISH 106"]

# Load Records
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    cols = ["DATE", "TRACTOR", "DRIVER_NAME", "ROUND", "WEIGHT", "RATE", "KAMAI", "DIESEL", "DRIVER_EXP", "OTHER", "TOTAL_INV", "PROFIT"]
    df = pd.DataFrame(columns=cols)

# --- 3. Sidebar Setup ---
with st.sidebar:
    st.header("🚜 MENU")
    
    # ➕ ADD NEW TRACTOR
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
    
    st.markdown("---")
    st.markdown("**Kharche (Expenses)**")
    diesel = st.number_input("Diesel", min_value=0.0)
    d_pay = st.number_input("Driver Kharcha", min_value=0.0)
    other = st.number_input("Other", min_value=0.0)

    if st.button("💾 SAVE RECORD"):
        kamai = weight * rate
        total_inv = diesel + d_pay + other
        new_row = {
            "DATE": str(date), 
            "TRACTOR": active_tractor, 
            "DRIVER_NAME": d_name,
            "ROUND": 1, 
            "WEIGHT": weight, 
            "RATE": rate, 
            "KAMAI": round(kamai, 2),
            "DIESEL": diesel, 
            "DRIVER_EXP": d_pay, 
            "OTHER": other,
            "TOTAL_INV": round(total_inv, 2), 
            "PROFIT": round(kamai - total_inv, 2)
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("Save Ho Gaya!")
        st.rerun()

# --- 4. Main Page Display ---
set_design(active_tractor)

# Huge Cherry Title
st.markdown(f'<p class="big-cherry-title">{active_tractor}</p>', unsafe_allow_html=True)

# Data for Active Tractor
t_df = df[df["TRACTOR"] == active_tractor]

# Sequence of Metrics
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
        row = st.selectbox("Kaun sa No. hatana hai?", t_df.index)
        if st.button("Humesha ke liye hatayein"):
            df = df.drop(row)
            df.to_csv(DATA_FILE, index=False)
            st.rerun()
