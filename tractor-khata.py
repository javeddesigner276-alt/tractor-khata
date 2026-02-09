import streamlit as st
import pandas as pd

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
        font-size: 80px !important; font-weight: 950 !important; color: #800000 !important; 
        text-align: center !important; margin-top: -50px !important; text-transform: uppercase;
        text-shadow: 2px 2px 10px rgba(0,0,0,0.3);
    }}
    [data-testid="stSidebar"] {{ background-color: #800000 !important; }}
    [data-testid="stSidebar"] label p {{ color: #FFFFFF !important; font-size: 20px !important; font-weight: 900 !important; }}
    [data-testid="stMetricValue"] div {{ font-size: 40px !important; font-weight: 950 !important; color: #800000 !important; }}
    </style>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=2)
def load_data():
    try:
        # skiprows=1 ka matlab pehli heading wali row ko chhod do
        data = pd.read_csv(ZOHO_URL, skiprows=1)
        # Headers se faltu space hatana
        data.columns = [str(c).strip() for c in data.columns]
        return data
    except Exception as e:
        return pd.DataFrame()

set_design()
df = load_data()

# Tractor Selection (Aapki heading ke hisab se default set hai)
base_tractors = ["MAHINDRA NOVO 605", "FARMTRACK 60", "NAGISH 106"]

with st.sidebar:
    st.header("🚜 MENU")
    active_tractor = st.selectbox("Apna Tractor Chunein", base_tractors)
    if st.button("🔄 REFRESH DATA"):
        st.cache_data.clear()
        st.rerun()

st.markdown(f'<p class="big-cherry-title">{active_tractor}</p>', unsafe_allow_html=True)

if not df.empty:
    # Aapki sheet ke columns ko numeric mein badalna
    # Note: Agar Zoho mein do column ka naam same ho (TOTAL), toh pandas doosre ko TOTAL.1 bana deta hai
    cols_to_fix = {
        'WEIGHT(KG)': 'WEIGHT(KG)',
        'TOTAL': 'TOTAL (KAMAI)',
        'TOTAL.1': 'TOTAL (KHARCHA)',
        'LOSS & PROFIT': 'LOSS & PROFIT'
    }
    
    for old_col in cols_to_fix.keys():
        if old_col in df.columns:
            df[old_col] = pd.to_numeric(df[old_col], errors='coerce').fillna(0)

    # Metrics Display
    c1, c2, c3, c4 = st.columns(4)
    
    weight_val = df['WEIGHT(KG)'].sum() if 'WEIGHT(KG)' in df.columns else 0
    kamai_val = df['TOTAL'].sum() if 'TOTAL' in df.columns else 0
    kharcha_val = df['TOTAL.1'].sum() if 'TOTAL.1' in df.columns else 0
    profit_val = df['LOSS & PROFIT'].sum() if 'LOSS & PROFIT' in df.columns else 0

    c1.metric("KUL WEIGHT", f"{weight_val:,.0f} KG")
    c2.metric("KUL KAMAI", f"₹{kamai_val:,.2f}")
    c3.metric("KUL KHARCHA", f"₹{kharcha_val:,.2f}")
    c4.metric("NET PROFIT", f"₹{profit_val:,.2f}")

    st.divider()
    
    # Table Display
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.error("⚠️ Data nahi dikh raha! Check karein ki Zoho Sheet mein Row 2 mein headers hain ya nahi.")
    st.info("💡 Hint: Row 1 mein 'MAHINDRA NOVO 605' rakhein aur Row 2 mein 'DATE', 'WEIGHT(KG)' etc.")
