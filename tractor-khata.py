import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# --- 1. App Configuration ---
st.set_page_config(page_title="JAVED RANGHAD TRACTOR KHATA", layout="wide")

# Aapka Google Sheet Link
SHEET_URL = "https://docs.google.com/spreadsheets/d/1K8Umx9q0IEka1O6IrIo1DrMcGgtxGbDW4raQybV_Ljg/edit?usp=sharing"

# Connection Setup
conn = st.connection("gsheets", type=GSheetsConnection)

def load_data():
    try:
        # ttl=0 matlab turant naya data dikhega
        return conn.read(spreadsheet=SHEET_URL, ttl=0)
    except Exception as e:
        return pd.DataFrame(columns=["DATE", "TRACTOR", "DRIVER_NAME", "WEIGHT", "RATE", "KAMAI", "DIESEL", "DRIVER_EXP", "OTHER", "TOTAL_INV", "PROFIT"])

# Custom Design (White Headings & Bold Text)
def set_design():
    img_url = "https://images.pexels.com/photos/2933243/pexels-photo-2933243.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
    st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(255,255,255,0.75), rgba(255,255,255,0.75)), url("{img_url}");
        background-size: cover; background-position: center; background-attachment: fixed;
    }}
    .big-cherry-title {{ 
        font-size: 80px !important; font-weight: 950 !important; color: #800000 !important; 
        text-align: center !important; margin-top: -50px !important; text-transform: uppercase;
        text-shadow: 2px 2px 5px rgba(0,0,0,0.2);
    }}
    
    /* SIDEBAR */
    [data-testid="stSidebar"] {{ background-color: #800000 !important; }}
    
    /* MENU & NAYI ENTRY - White & Bold */
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {{
        color: #FFFFFF !important; font-size: 30px !important; font-weight: 900 !important;
        text-transform: uppercase; border-bottom: 3px solid white; padding-bottom: 5px;
    }}

    /* LABELS - White & Bold */
    [data-testid="stSidebar"] label p {{
        color: #FFFFFF !important; font-size: 20px !important; font-weight: 800 !important;
    }}

    /* INPUT BOXES - Black Text */
    [data-testid="stSidebar"] input, [data-testid="stSidebar"] select {{
        color: #000000 !important; font-weight: 900 !important; font-size: 16px !important;
    }}

    /* METRICS */
    [data-testid="stMetricValue"] div {{ font-size: 45px !important; font-weight: 950 !important; color: #800000 !important; }}
    
    /* White box for Delete section */
    [data-testid="stExpander"] {{ background-color: white !important; border-radius: 10px; border: 2px solid #800000; }}
    [data-testid="stExpander"] p {{ color: black !important; font-weight: 900 !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. Main Logic ---
df = load_data()
base_tractors = ["FARMTRACK 60", "MAHINDRA NOVO 605", "NAGISH 106"]
if not df.empty and "TRACTOR" in df.columns:
    existing = [t for t in df["TRACTOR"].unique().tolist() if pd.notna(t)]
    base_tractors = sorted(list(set(base_tractors + existing)))

# Sidebar
with st.sidebar:
    st.header("🚜 MENU")
    active_tractor = st.selectbox("Tractor Chunein", base_tractors)
    st.divider()
    
    st.subheader("📝 Nayi
