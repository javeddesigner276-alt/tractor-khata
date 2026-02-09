import streamlit as st
import pandas as pd

# --- 1. App Configuration ---
st.set_page_config(page_title="JAVED RANGHAD TRACTOR KHATA", layout="wide")

# AAPKA ZOHO CSV LINK
ZOHO_URL = "https://sheet.zohopublic.in/sheet/published/nkkiha1063d1e61dd48a49008ceb6396f1a1a?mode=csv"

# --- 2. Custom Design ---
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
        text-shadow: 2px 2px 8px rgba(0,0,0,0.2);
    }}
    [data-testid="stSidebar"] {{ background-color: #800000 !important; }}
    [data-testid="stSidebar"] label p {{ color: #FFFFFF !important; font-size: 22px !important; font-weight: 900 !important; }}
    [data-testid="stMetricValue"] div {{ font-size: 45px !important; font-weight: 950 !important; color: #800000 !important; }}
    [data-testid="stSidebar"] h1 {{ color: #FFFFFF !important; border-bottom: 2px solid white; }}
    .stDataFrame {{ background-color: white; border-radius: 10px; }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. Data Loading Logic ---
@st.cache_data(ttl=10) # 10 second refresh rate
def load_data():
    try:
        # Zoho CSV se data load karna
        data = pd.read_csv(ZOHO_URL)
        
        # 1. Columns ke aage-piche se faltu space hatana
        data.columns = data.columns.str.strip()
        
        # 2. Saare numeric columns ko sahi karna (agar Zoho mein text ho toh 0 kar dega)
        numeric_cols = ["WEIGHT", "RATE", "KAMAI", "DIESEL", "DRIVER_EXP", "OTHER", "TOTAL_INV", "PROFIT"]
        for col in numeric_cols:
            if col in data.columns:
                data[col] = pd.to_numeric(data[col], errors='coerce').fillna(0)
        
        # 3. Tractor column ke naam bhi saaf karna
        if "TRACTOR" in data.columns:
            data["TRACTOR"] = data["TRACTOR"].astype(str).str.strip().str.upper()
            
        return data
    except Exception as e:
        st.error(f"Zoho Connection Error: {e}")
        return pd.DataFrame()

# --- 4. Main App Logic ---
set_design()
df = load_data()

# Tractor ki list (Zoho mein jo naam hain wahi yahan likhein)
base_tractors = ["FARMTRACK 60", "MAHINDRA NOVO 605", "NAGISH 106"]

with st.sidebar:
    st.header("🚜 MENU")
    active_tractor = st.selectbox("Apna Tractor Chunein", base_tractors)
    st.divider()
    st.write("✅ Status: Live from Zoho")
    if st.button("🔄 REFRESH HISAB"):
        st.cache_data.clear()
        st.rerun()

# Title Display
st.markdown(f'<p class="big-cherry-title">{active_tractor}</p>', unsafe_allow_html=True)

if not df.empty:
    if "TRACTOR" in df.columns:
        # Data Filter karna
        t_df = df[df["TRACTOR"] == active_tractor.upper()].copy()
        
        # Metrics Display (4 Bade Dabbe)
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("TOTAL WEIGHT", f"{t_df['WEIGHT'].sum():.2f} KG")
        c2.metric("KUL KAMAI", f"₹{t_df['KAMAI'].sum():.2f}")
        c3.metric("KUL KHARCHA", f"₹{t_df['TOTAL_INV'].sum():.2f}")
        c4.metric("NET PROFIT", f"₹{t_df['PROFIT'].sum():.2f}")

        st.divider()
        
        # Table Display
        # Sirf wahi columns dikhana jo zaroori hain (Order set kar diya hai)
        order_cols = ["DATE", "DRIVER_NAME", "ROUND", "WEIGHT", "RATE", "KAMAI", "DIESEL", "DRIVER_EXP", "OTHER", "TOTAL_INV", "PROFIT"]
        available_cols = [c for c in order_cols if c in t_df.columns]
        
        if not t_df.empty:
            st.dataframe(t_df[available_cols], use_container_width=True, hide_index=True)
        else:
            st.warning(f"Bhai, {active_tractor} ka koi record Zoho Sheet mein nahi mila.")
    else:
        st.error("Galti: Zoho Sheet mein 'TRACTOR' naam ka column nahi mila!")
else:
    st.info("Zoho Sheet load ho rahi hai ya khali hai. Refresh karke dekhein.")
