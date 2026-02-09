import streamlit as st
import pandas as pd

# --- 1. App Configuration ---
st.set_page_config(page_title="JAVED RANGHAD TRACTOR KHATA", layout="wide")

# AAPKA ZOHO CSV LINK (Directly converted for Python)
# Maine aapke link ke aage ?mode=csv jod diya hai taaki data seedha uth sake
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
    </style>
    """, unsafe_allow_html=True)

# --- 3. Data Loading Logic ---
@st.cache_data(ttl=10) # 10 second refresh rate
def load_data():
    try:
        # Zoho se data read karna
        data = pd.read_csv(ZOHO_URL)
        # Columns ke naam saaf karna
        data.columns = data.columns.str.strip()
        
        # Numbers ko float mein badalna
        numeric_cols = ["WEIGHT", "RATE", "KAMAI", "DIESEL", "DRIVER_EXP", "OTHER", "TOTAL_INV", "PROFIT"]
        for col in numeric_cols:
            if col in data.columns:
                data[col] = pd.to_numeric(data[col], errors='coerce').fillna(0)
        
        # Tractor names ko upper case karna
        if "TRACTOR" in data.columns:
            data["TRACTOR"] = data["TRACTOR"].astype(str).str.strip().str.upper()
            
        return data
    except Exception as e:
        # Agar error aaye toh dashboard par dikhao
        st.error(f"⚠️ Zoho Connection Error: Link sahi nahi hai ya Sheet publish nahi hui.")
        return pd.DataFrame()

# --- 4. Page Layout ---
set_design()
df = load_data()

# Tractor ki list (Zoho mein jo naam likhenge wahi yahan dikhenge)
base_tractors = ["FARMTRACK 60", "MAHINDRA NOVO 605", "NAGISH 106"]

with st.sidebar:
    st.header("🚜 MENU")
    active_tractor = st.selectbox("Apna Tractor Chunein", base_tractors)
    st.divider()
    st.success("✅ Connected to Zoho Sheet")
    if st.button("🔄 REFRESH DATA"):
        st.cache_data.clear()
        st.rerun()

# Tractor Name Title
st.markdown(f'<p class="big-cherry-title">{active_tractor}</p>', unsafe_allow_html=True)

if not df.empty:
    if "TRACTOR" in df.columns:
        # Filter for selected tractor
        t_df = df[df["TRACTOR"] == active_tractor.upper()].copy()
        
        # Metrics Display
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("TOTAL WEIGHT", f"{t_df['WEIGHT'].sum():.2f} KG")
        c2.metric("KUL KAMAI", f"₹{t_df['KAMAI'].sum():.2f}")
        c3.metric("KUL KHARCHA", f"₹{t_df['TOTAL_INV'].sum():.2f}")
        c4.metric("NET PROFIT", f"₹{t_df['PROFIT'].sum():.2f}")

        st.divider()
        
        # Display Table
        show_cols = ["DATE", "DRIVER_NAME", "ROUND", "WEIGHT", "RATE", "KAMAI", "DIESEL", "DRIVER_EXP", "OTHER", "TOTAL_INV", "PROFIT"]
        actual_cols = [c for c in show_cols if c in t_df.columns]
        
        if not t_df.empty:
            st.dataframe(t_df[actual_cols], use_container_width=True, hide_index=True)
        else:
            st.info(f"Bhai, {active_tractor} ka abhi koi data Zoho mein nahi hai.")
    else:
        st.error("Error: Zoho Sheet mein 'TRACTOR' naam ka column nahi mila!")
else:
    st.warning("Zoho Sheet load nahi ho rahi. Check karein ki apne Sheet ko 'Publish' kiya hai ya nahi.")
