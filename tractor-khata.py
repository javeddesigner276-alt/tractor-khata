import streamlit as st
import pandas as pd

# --- 1. App Configuration ---
st.set_page_config(page_title="JAVED RANGHAD TRACTOR KHATA", layout="wide")

# AAPKA ZOHO LINK
ZOHO_URL = "https://sheet.zohopublic.in/sheet/publishedsheet/36364df8cd3cbedb7cd796ab0817ed93a1dfe6252a3c6b612288121c8a80d211?type=csv"

def set_design():
    st.markdown(f"""
    <style>
    .stApp {{ background-color: #f0f2f6; }}
    .big-title {{ 
        font-size: 50px !important; font-weight: 900 !important; color: #800000 !important; 
        text-align: center !important;
    }}
    [data-testid="stMetricValue"] div {{ color: #800000 !important; font-weight: bold; }}
    </style>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=2)
def load_data():
    try:
        # Zoho se data load karna - Hum yahan header=1 use kar rahe hain 
        # Kyunki aapki pehli line mein Tractor ka naam hai
        df = pd.read_csv(ZOHO_URL, header=1)
        
        # Column names ke aage piche se space hatana
        df.columns = [str(c).strip() for c in df.columns]
        
        # Numbers ko sahi format mein lana
        for col in ['WEIGHT(KG)', 'TOTAL', 'TOTAL.1', 'LOSS & PROFIT']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        return df
    except Exception as e:
        return pd.DataFrame()

set_design()
df = load_data()

st.markdown('<p class="big-title">🚜 JAVED RANGHAD TRACTOR KHATA</p>', unsafe_allow_html=True)

if not df.empty:
    # 4 metrics
    c1, c2, c3, c4 = st.columns(4)
    
    # Aapki sheet ke columns: WEIGHT(KG), TOTAL (Kamai), TOTAL.1 (Kharcha), LOSS & PROFIT
    w = df['WEIGHT(KG)'].sum() if 'WEIGHT(KG)' in df.columns else 0
    k = df['TOTAL'].sum() if 'TOTAL' in df.columns else 0
    kh = df['TOTAL.1'].sum() if 'TOTAL.1' in df.columns else 0
    p = df['LOSS & PROFIT'].sum() if 'LOSS & PROFIT' in df.columns else 0

    c1.metric("KUL WEIGHT", f"{w:,.0f} KG")
    c2.metric("KUL KAMAI", f"₹{k:,.0f}")
    c3.metric("KUL KHARCHA", f"₹{kh:,.0f}")
    c4.metric("NET PROFIT", f"₹{p:,.0f}")

    st.divider()
    
    # Table dikhana
    st.write("### LIVE DATA FROM ZOHO SHEET")
    st.dataframe(df, use_container_width=True)
else:
    st.error("Bhai, Zoho Sheet se data nahi aa raha hai.")
    st.write("Ek baar ye check karein:")
    st.write("1. Zoho Sheet mein 'File' -> 'Publish' -> 'External Link' chalu hai?")
    st.write("2. Kya aapne Zoho Sheet mein kuch likha hua hai?")
    
    # Backup Button
    if st.button("Koshish karein (Force Refresh)"):
        st.cache_data.clear()
        st.rerun()
