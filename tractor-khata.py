import streamlit as st
import pandas as pd

# --- 1. App Configuration ---
st.set_page_config(page_title="JAVED RANGHAD TRACTOR KHATA", layout="wide")

# AAPKA ZOHO LINK
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
        font-size: 70px !important; font-weight: 950 !important; color: #800000 !important; 
        text-align: center !important; margin-top: -40px !important; text-transform: uppercase;
        text-shadow: 2px 2px 10px rgba(0,0,0,0.3);
    }}
    [data-testid="stSidebar"] {{ background-color: #800000 !important; }}
    [data-testid="stSidebar"] label p {{ color: #FFFFFF !important; font-size: 20px !important; font-weight: 900 !important; }}
    [data-testid="stMetricValue"] div {{ font-size: 35px !important; font-weight: 950 !important; color: #800000 !important; }}
    </style>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=2)
def load_data():
    try:
        # Pura data load karna bina skip kiye taaki hum headers khud dhoond sakein
        raw_data = pd.read_csv(ZOHO_URL, header=None)
        
        # 1. Pehli aisi row dhoondna jisme "DATE" likha ho (Ye hamara asli header hoga)
        header_row_index = 0
        for i, row in raw_data.iterrows():
            if "DATE" in [str(val).strip().upper() for val in row.values]:
                header_row_index = i
                break
        
        # 2. Data ko us row se dobara load karna
        df = pd.read_csv(ZOHO_URL, skiprows=header_row_index)
        
        # 3. Headers clean karna
        df.columns = [str(c).strip().upper() for c in df.columns]
        
        # 4. Numeric columns fix karna (Aapki sheet ke hisab se)
        fix_map = {
            'WEIGHT(KG)': 'WEIGHT(KG)', 
            'TOTAL': 'KAMAI', 
            'TOTAL.1': 'KHARCHA', 
            'LOSS & PROFIT': 'PROFIT'
        }
        
        for old, new in fix_map.items():
            if old in df.columns:
                df[old] = pd.to_numeric(df[old], errors='coerce').fillna(0)
                
        return df, list(df.columns)
    except Exception as e:
        return pd.DataFrame(), [str(e)]

# --- UI Layout ---
set_design()
df, cols_found = load_data()
base_tractors = ["MAHINDRA NOVO 605", "FARMTRACK 60", "NAGISH 106"]

with st.sidebar:
    st.header("🚜 MENU")
    active_tractor = st.selectbox("Apna Tractor Chunein", base_tractors)
    if st.button("🔄 REFRESH DATA"):
        st.cache_data.clear()
        st.rerun()

st.markdown(f'<p class="big-cherry-title">{active_tractor}</p>', unsafe_allow_html=True)

if not df.empty:
    # Saara data dikhana (Abhi filter nahi kar rahe taaki check kar sakein)
    # Metrics calculation
    c1, c2, c3, c4 = st.columns(4)
    
    # Aapki sheet ke columns ke exact naam check karna
    w_col = 'WEIGHT(KG)' if 'WEIGHT(KG)' in df.columns else None
    k_col = 'TOTAL' if 'TOTAL' in df.columns else None
    kh_col = 'TOTAL.1' if 'TOTAL.1' in df.columns else None
    p_col = 'LOSS & PROFIT' if 'LOSS & PROFIT' in df.columns else None

    c1.metric("KUL WEIGHT", f"{df[w_col].sum() if w_col else 0:,.0f} KG")
    c2.metric("KUL KAMAI", f"₹{df[k_col].sum() if k_col else 0:,.2f}")
    c3.metric("KUL KHARCHA", f"₹{df[kh_col].sum() if kh_col else 0:,.2f}")
    c4.metric("NET PROFIT", f"₹{df[p_col].sum() if p_col else 0:,.2f}")

    st.divider()
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.error("⚠️ Data connect nahi ho raha!")
    st.write("Dikaat ye ho sakti hai:")
    st.write("1. Zoho Sheet mein 'DATE' naam ka column sahi spelling mein nahi hai.")
    st.write("2. Link access nahi de raha.")
