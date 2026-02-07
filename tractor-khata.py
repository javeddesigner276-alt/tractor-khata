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
        return conn.read(spreadsheet=SHEET_URL, ttl=0)
    except:
        return pd.DataFrame(columns=["DATE", "TRACTOR", "DRIVER_NAME", "WEIGHT", "RATE", "KAMAI", "DIESEL", "DRIVER_EXP", "OTHER", "TOTAL_INV", "PROFIT"])

# Custom Design
def set_design():
    img_url = "https://images.pexels.com/photos/2933243/pexels-photo-2933243.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
    st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(255,255,255,0.75), rgba(255,255,255,0.75)), url("{img_url}");
        background-size: cover; background-position: center; background-attachment: fixed;
    }}
    .big-cherry-title {{ 
        font-size: 100px !important; font-weight: 950 !important; color: #800000 !important; 
        text-align: center !important; margin-top: -50px !important; text-transform: uppercase;
        text-shadow: 2px 2px 5px rgba(0,0,0,0.2);
    }}
    
    /* SIDEBAR BACKGROUND */
    [data-testid="stSidebar"] {{ background-color: #800000 !important; }}
    
    /* MENU & NAYI ENTRY (Headings) - White & Extra Bold */
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {{
        color: #FFFFFF !important;
        font-size: 32px !important;
        font-weight: 900 !important;
        text-transform: uppercase;
        border-bottom: 3px solid #FFFFFF;
        padding-bottom: 5px;
        margin-bottom: 20px !important;
    }}

    /* SIDEBAR LABELS (Tarik, Driver Name etc.) - White & Bold */
    [data-testid="stSidebar"] label p {{
        color: #FFFFFF !important;
        font-size: 22px !important;
        font-weight: 800 !important;
    }}

    /* INPUT BOXES - Text Black & Bold */
    [data-testid="stSidebar"] input, [data-testid="stSidebar"] select {{
        color: #000000 !important;
        font-weight: 900 !important;
        font-size: 18px !important;
    }}

    /* METRICS SECTION */
    [data-testid="stMetricLabel"] p {{ font-size: 24px !important; font-weight: 900 !important; color: #333 !important; }}
    [data-testid="stMetricValue"] div {{ font-size: 50px !important; font-weight: 950 !important; color: #800000 !important; }}
    
    /* White box for Expander */
    [data-testid="stExpander"] {{ background-color: white !important; border-radius: 10px; border: 2px solid #800000; }}
    [data-testid="stExpander"] p {{ color: black !important; font-weight: 900 !important; font-size: 18px !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. Data Load ---
df = load_data()
base_tractors = ["FARMTRACK 60", "MAHINDRA NOVO 605", "NAGISH 106"]
if not df.empty and "TRACTOR" in df.columns:
    existing = [t for t in df["TRACTOR"].unique().tolist() if pd.notna(t)]
    base_tractors = sorted(list(set(base_tractors + existing)))

# --- 3. Sidebar ---
with st.sidebar:
    st.header("🚜 MENU") # Ab ye White aur Bold dikhega
    active_tractor = st.selectbox("Tractor Chunein", base_tractors)
    st.divider()
    
    st.subheader("📝 Nayi Entry") # Ab ye White aur Bold dikhega
    date = st.date_input("Tarik")
    d_name = st.text_input("Driver ka Naam")
    weight = st.number_input("Weight (KG)", min_value=0.0)
    rate = st.number_input("Rate", min_value=0.0, format="%.4f")
    diesel = st.number_input("Diesel", min_value=0.0)
    d_pay = st.number_input("Driver Kharcha", min_value=0.0)
    other = st.number_input("Other Kharcha", min_value=0.0)

    if st.button("💾 SAVE TO SHEET"):
        kamai = weight * rate
        total_inv = diesel + d_pay + other
        new_row = pd.DataFrame([{
            "DATE": str(date), "TRACTOR": active_tractor, "DRIVER_NAME": d_name,
            "WEIGHT": weight, "RATE": rate, "KAMAI": round(kamai, 2), 
            "DIESEL": diesel, "DRIVER_EXP": d_pay, "OTHER": other, 
            "TOTAL_INV": round(total_inv, 2), "PROFIT": round(kamai - total_inv, 2)
        }])
        updated_df = pd.concat([df, new_row], ignore_index=True)
        conn.update(spreadsheet=SHEET_URL, data=updated_df)
        st.success("Entry Save Ho Gayi!")
        st.rerun()

# --- 4. Main Display ---
set_design()
st.markdown(f'<p class="big-cherry-title">{active_tractor}</p>', unsafe_allow_html=True)

t_df = df[df["TRACTOR"] == active_tractor] if not df.empty else pd.DataFrame()

c1, c2, c3, c4 = st.columns(4)
c1.metric("TOTAL
