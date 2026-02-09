import streamlit as st
import pandas as pd

# --- 1. App Configuration ---
st.set_page_config(page_title="JAVED RANGHAD TRACTOR KHATA", layout="wide")

# AAPKA ZOHO DIRECT CSV LINK (Updated with your new ID)
ZOHO_URL = "https://sheet.zohopublic.in/sheet/publishedsheet/36364df8cd3cbedb7cd796ab0817ed93a1dfe6252a3c6b612288121c8a80d211?type=csv"

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
    </style>
    """, unsafe_allow_html=True)

# --- 3. Data Loading Logic ---
@st.cache_data(ttl=5) # Har 5 second mein naya data check karega
def load_data():
    try:
        # Zoho se CSV format mein data uthana
        data = pd.read_csv(ZOHO_URL)
        
        # Columns ke naam saaf karna (Faltu space hatana)
        data.columns = data.columns.str.strip()
        
        # Numbers ko sahi karna (Weight, Kamai etc.)
        numeric_cols = ["WEIGHT", "RATE", "KAMAI", "DIESEL", "DRIVER_EXP", "OTHER", "TOTAL_INV", "PROFIT"]
        for col in numeric_cols:
            if col in data.columns:
                data[col] = pd.to_numeric(data[col], errors='coerce').fillna(0)
        
        # Tractor names ko clean karna
        if "TRACTOR" in data.columns:
            data["TRACTOR"] = data["TRACTOR"].astype(str).str.strip().str.upper()
            
        return data
    except Exception as e:
        # Agar Zoho link kaam na kare toh error dikhao
        st.sidebar.error("⚠️ Zoho Sheet se connect nahi ho raha. Check karein ki Sheet 'Published' hai ya nahi.")
        return pd.DataFrame()

# --- 4. Main Page Display ---
set_design()
df = load_data()

# Tractor List
base_tractors = ["FARMTRACK 60", "MAHINDRA NOVO 605", "NAGISH 106"]

with st.sidebar:
    st.header("🚜 MENU")
    active_tractor = st.selectbox("Apna Tractor Chunein", base_tractors)
    st.divider()
    st.success("✅ Live From Zoho")
    if st.button("🔄 REFRESH HISAB"):
        st.cache_data.clear()
        st.rerun()

st.markdown(f'<p class="big-cherry-title">{active_tractor}</p>', unsafe_allow_html=True)

if not df.empty:
    if "TRACTOR" in df.columns:
        # Selected tractor ka data filter karna
        t_df = df[df["TRACTOR"] == active_tractor.upper()].copy()
        
        # Metrics Display (4 Bade Dabbe)
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("TOTAL WEIGHT", f"{t_df['WEIGHT'].sum():.2f} KG")
        c2.metric("KUL KAMAI", f"₹{t_df['KAMAI'].sum():.2f}")
        c3.metric("KUL KHARCHA", f"₹{t_df['TOTAL_INV'].sum():.2f}")
        c4.metric("NET PROFIT", f"₹{t_df['PROFIT'].sum():.2f}")

        st.divider()
        
        # Table Display
        show_cols = ["DATE", "DRIVER_NAME", "ROUND", "WEIGHT", "RATE", "KAMAI", "DIESEL", "DRIVER_EXP", "OTHER", "TOTAL_INV", "PROFIT"]
        actual_cols = [c for c in show_cols if c in t_df.columns]
        
        if not t_df.empty:
            st.dataframe(t_df[actual_cols], use_container_width=True, hide_index=True)
        else:
            st.info(f"Bhai, Zoho Sheet mein {active_tractor} ka abhi koi data nahi hai.")
    else:
        st.error("Galti: Zoho Sheet ki pehli line mein 'TRACTOR' naam ka column nahi mila.")
else:
    st.warning("Zoho Sheet khali hai ya link kaam nahi kar raha. Zoho mein data bhar kar 'Publish' zaroor karein.")
