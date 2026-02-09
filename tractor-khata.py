import streamlit as st
import pandas as pd
import requests
from io import StringIO

# --- 1. App Configuration ---
st.set_page_config(page_title="JAVED RANGHAD TRACTOR KHATA", layout="wide")

# AAPKA ZOHO DIRECT CSV LINK
ZOHO_URL = "https://sheet.zohopublic.in/sheet/publishedsheet/36364df8cd3cbedb7cd796ab0817ed93a1dfe6252a3c6b612288121c8a80d211?type=csv"

def set_design():
    img_url = "https://images.pexels.com/photos/2933243/pexels-photo-2933243.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
    st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(255,255,255,0.75), rgba(255,255,255,0.75)), url("{img_url}");
        background-size: cover; background-position: center; background-attachment: fixed;
    }}
    .big-cherry-title {{ 
        font-size: 60px !important; font-weight: 950 !important; color: #800000 !important; 
        text-align: center !important; margin-top: -30px !important; text-transform: uppercase;
    }}
    [data-testid="stSidebar"] {{ background-color: #800000 !important; }}
    [data-testid="stSidebar"] label p {{ color: #FFFFFF !important; font-size: 20px !important; font-weight: 900 !important; }}
    [data-testid="stMetricValue"] div {{ font-size: 35px !important; font-weight: 950 !important; color: #800000 !important; }}
    </style>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=2)
def load_data():
    try:
        # Step A: Data download karna
        response = requests.get(ZOHO_URL)
        if response.status_code != 200:
            return pd.DataFrame(), "Link Error"
        
        # Step B: Raw data read karna
        raw_csv = StringIO(response.text)
        all_data = pd.read_csv(raw_csv, header=None)
        
        # Step C: 'DATE' dhoondna headers ke liye
        header_idx = 0
        for i, row in all_data.iterrows():
            if "DATE" in [str(x).strip().upper() for x in row.values]:
                header_idx = i
                break
        
        # Step D: Sahi data frame banana
        df = pd.read_csv(StringIO(response.text), skiprows=header_idx)
        df.columns = [str(c).strip().upper() for c in df.columns]
        
        # Step E: Numbers fix karna (Aapki sheet ke names ke hisab se)
        # Zoho mein do bar 'TOTAL' hai, pandas use 'TOTAL' aur 'TOTAL.1' bana dega
        cols_map = {'WEIGHT(KG)': 'W', 'TOTAL': 'K', 'TOTAL.1': 'KH', 'LOSS & PROFIT': 'P'}
        for old in cols_map.keys():
            if old in df.columns:
                df[old] = pd.to_numeric(df[old], errors='coerce').fillna(0)
        
        return df, "Success"
    except Exception as e:
        return pd.DataFrame(), str(e)

# --- Layout ---
set_design()
df, status = load_data()
base_tractors = ["MAHINDRA NOVO 605", "FARMTRACK 60", "NAGISH 106"]

with st.sidebar:
    st.header("🚜 MENU")
    active_tractor = st.selectbox("Apna Tractor Chunein", base_tractors)
    if st.button("🔄 REFRESH DATA"):
        st.cache_data.clear()
        st.rerun()

st.markdown(f'<p class="big-cherry-title">{active_tractor}</p>', unsafe_allow_html=True)

if not df.empty:
    # Metrics columns check
    w_col = 'WEIGHT(KG)' if 'WEIGHT(KG)' in df.columns else None
    k_col = 'TOTAL' if 'TOTAL' in df.columns else None
    kh_col = 'TOTAL.1' if 'TOTAL.1' in df.columns else None
    p_col = 'LOSS & PROFIT' if 'LOSS & PROFIT' in df.columns else None

    # 4 metrics
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("KUL WEIGHT", f"{df[w_col].sum() if w_col else 0:,.0f} KG")
    c2.metric("KUL KAMAI", f"₹{df[k_col].sum() if k_col else 0:,.2f}")
    c3.metric("KUL KHARCHA", f"₹{df[kh_col].sum() if kh_col else 0:,.2f}")
    c4.metric("NET PROFIT", f"{df[p_col].sum() if p_col else 0:,.2f}")

    st.divider()
    # Puri table dikhana
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.error(f"⚠️ Dikaat: {status}")
    st.info("Bhai, Zoho Sheet mein check karein ki Row 2 mein 'DATE' likha hai ya nahi.")
