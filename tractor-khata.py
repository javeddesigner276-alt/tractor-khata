import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- PAGE CONFIG ---
st.set_page_config(page_title="JAVED TRACTOR KHATA", layout="wide")

# Google Sheet URL
SHEET_URL = "https://docs.google.com/spreadsheets/d/1K8Umx9q0IEka1O6IrIo1DrMcGgtxGbDW4raQybV_Ljg/edit?usp=sharing"

# --- STYLE (WHITE & BOLD) ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(255,255,255,0.7), rgba(255,255,255,0.7)), 
                    url("https://images.pexels.com/photos/2933243/pexels-photo-2933243.jpeg?auto=compress&cs=tinysrgb&w=1260");
        background-size: cover; background-attachment: fixed;
    }
    .main-title { 
        font-size: 60px !important; font-weight: 950 !important; color: #800000 !important; 
        text-align: center; text-transform: uppercase;
    }
    [data-testid="stSidebar"] { background-color: #800000 !important; }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: white !important; font-weight: 900 !important; border-bottom: 2px solid white;
    }
    [data-testid="stSidebar"] label p { color: white !important; font-weight: 800 !important; font-size: 20px !important; }
    [data-testid="stSidebar"] input { color: black !important; font-weight: bold; }
    [data-testid="stMetricValue"] div { font-size: 40px !important; font-weight: 900 !important; color: #800000 !important; }
    </style>
    """, unsafe_allow_html=True)

# Data Load using Pandas (Public link)
def load_data():
    try:
        csv_url = SHEET_URL.replace('/edit?usp=sharing', '/export?format=csv')
        return pd.read_csv(csv_url)
    except:
        return pd.DataFrame(columns=["DATE", "TRACTOR", "DRIVER_NAME", "WEIGHT", "RATE", "KAMAI", "DIESEL", "DRIVER_EXP", "OTHER", "TOTAL_INV", "PROFIT"])

df = load_data()
tractors = ["FARMTRACK 60", "MAHINDRA NOVO 605", "NAGISH 106"]

with st.sidebar:
    st.header("🚜 MENU")
    active_t = st.selectbox("Tractor Chunein", tractors)
    st.divider()
    
    st.subheader("📝 Nayi Entry")
    dt = st.date_input("Tarik")
    dr = st.text_input("Driver Name")
    wt = st.number_input("Weight (KG)", min_value=0.0)
    rt = st.number_input("Rate", min_value=0.0)
    ds = st.number_input("Diesel", min_value=0.0)
    dx = st.number_input("Driver Kharcha", min_value=0.0)
    ot = st.number_input("Other Kharcha", min_value=0.0)

    if st.button("💾 SAVE DATA"):
        # Yahan hum simple link based save use kar rahe hain
        # Kyunaki connection error aa raha tha, ye method use karenge:
        st.info("Bhai, Streamlit Cloud mein 'Secrets' set karne honge. Tab tak ye button data nahi bhej payega.")
        st.write("Kya aapne Google Sheet ko 'Editor' banaya hai? Agar haan, toh mujhe screenshot dikhao.")

# --- DISPLAY ---
st.markdown(f'<p class="main-title">{active_t}</p>', unsafe_allow_html=True)
t_df = df[df["TRACTOR"] == active_t] if not df.empty else pd.DataFrame()

c1, c2, c3, c4 = st.columns(4)
if not t_df.empty:
    c1.metric("TOTAL WEIGHT", f"{t_df['WEIGHT'].sum():.2f}")
    c2.metric("KUL KAMAI", f"₹{t_df['KAMAI'].sum():.2f}")
    c3.metric("KUL KHARCHA", f"₹{t_df['TOTAL_INV'].sum():.2f}")
    c4.metric("NET PROFIT", f"₹{t_df['PROFIT'].sum():.2f}")

st.divider()
st.dataframe(t_df, use_container_width=True)
