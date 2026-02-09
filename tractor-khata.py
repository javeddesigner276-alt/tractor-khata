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
        font-size: 60px !important; font-weight: 950 !important; color: #800000 !important; 
        text-align: center !important; margin-top: -30px !important; text-transform: uppercase;
        text-shadow: 2px 2px 10px rgba(0,0,0,0.3);
    }}
    [data-testid="stSidebar"] {{ background-color: #800000 !important; }}
    [data-testid="stSidebar"] label p {{ color: #FFFFFF !important; font-size: 20px !important; font-weight: 900 !important; }}
    [data-testid="stMetricValue"] div {{ font-size: 35px !important; font-weight: 950 !important; color: #800000 !important; }}
    </style>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=5)
def load_data():
    try:
        # Step 1: Seedha pandas se read karna (Sabse best tarika)
        # skiprows=1 isliye taaki 'MAHINDRA NOVO 605' wali line hat jaye
        df = pd.read_csv(ZOHO_URL, skiprows=1)
        
        # Step 2: Headers clean karna
        df.columns = [str(c).strip().upper() for c in df.columns]
        
        # Step 3: Numeric data ko fix karna
        # Note: Agar Zoho mein do TOTAL hain, toh pandas doosre ko TOTAL.1 bana dega
        cols_to_fix = ['WEIGHT(KG)', 'TOTAL', 'TOTAL.1', 'LOSS & PROFIT']
        for col in cols_to_fix:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        return df
    except Exception as e:
        st.error(f"⚠️ Connection Error: {e}")
        return pd.DataFrame()

# --- Page Layout ---
set_design()
df = load_data()
base_tractors = ["MAHINDRA NOVO 605", "FARMTRACK 60", "NAGISH 106"]

with st.sidebar:
    st.header("🚜 MENU")
    active_tractor = st.selectbox("Apna Tractor Chunein", base_tractors)
    st.divider()
    if st.button("🔄 REFRESH DATA"):
        st.cache_data.clear()
        st.rerun()

st.markdown(f'<p class="big-cherry-title">{active_tractor}</p>', unsafe_allow_html=True)

if not df.empty:
    # Metrics columns dhoondna
    w_col = 'WEIGHT(KG)' if 'WEIGHT(KG)' in df.columns else None
    k_col = 'TOTAL' if 'TOTAL' in df.columns else None
    kh_col = 'TOTAL.1' if 'TOTAL.1' in df.columns else None
    p_col = 'LOSS & PROFIT' if 'LOSS & PROFIT' in df.columns else None

    # Top Metrics
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("KUL WEIGHT", f"{df[w_col].sum() if w_col else 0:,.0f} KG")
    c2.metric("KUL KAMAI", f"₹{df[k_col].sum() if k_col else 0:,.2f}")
    c3.metric("KUL KHARCHA", f"₹{df[kh_col].sum() if kh_col else 0:,.2f}")
    c4.metric("NET PROFIT", f"₹{df[p_col].sum() if p_col else 0:,.2f}")

    st.divider()
    
    # Table Display
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("Bhai, Zoho Sheet load nahi ho rahi. Check karein ki Row 2 mein 'DATE' likha hai ya nahi.")
