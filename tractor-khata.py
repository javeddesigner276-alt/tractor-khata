import streamlit as st
import pandas as pd

# --- 1. App Configuration ---
st.set_page_config(page_title="JAVED RANGHAD TRACTOR KHATA", layout="wide")

# AAPKA ZOHO CSV LINK
# Note: Is link ke kaam karne ke liye Zoho mein Sheet select karke Publish karna zaroori hai
ZOHO_URL = "https://sheet.zohopublic.in/sheet/published/nkkiha1063d1e61dd48a49008ceb6396f1a1a?mode=csv"

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

@st.cache_data(ttl=5) # Sirf 5 second ka cache
def load_data():
    try:
        # Zoho se data uthana
        data = pd.read_csv(ZOHO_URL)
        data.columns = data.columns.str.strip() # Faltu space hatana
        return data
    except Exception as e:
        # Agar error aaye toh khali table dikhao aur error msg do
        st.sidebar.error("⚠️ Zoho se link nahi ban pa raha. Sheet check karein!")
        return pd.DataFrame()

set_design()
df = load_data()
base_tractors = ["FARMTRACK 60", "MAHINDRA NOVO 605", "NAGISH 106"]

with st.sidebar:
    st.header("🚜 MENU")
    active_tractor = st.selectbox("Apna Tractor Chunein", base_tractors)
    st.divider()
    if st.button("🔄 REFRESH DATA"):
        st.cache_data.clear()
        st.rerun()

st.markdown(f'<p class="big-cherry-title">{active_tractor}</p>', unsafe_allow_html=True)

if not df.empty:
    # Column check aur cleaning
    if "TRACTOR" in df.columns:
        # Case insensitive filtering
        t_df = df[df["TRACTOR"].astype(str).str.strip().str.upper() == active_tractor.upper()].copy()
        
        # Numbers ko sahi format mein laana
        numeric_cols = ["WEIGHT", "KAMAI", "TOTAL_INV", "PROFIT"]
        for col in numeric_cols:
            if col in t_df.columns:
                t_df[col] = pd.to_numeric(t_df[col], errors='coerce').fillna(0)

        # 4 Metrics Display
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("TOTAL WEIGHT", f"{t_df['WEIGHT'].sum():.2f} KG")
        c2.metric("KUL KAMAI", f"₹{t_df['KAMAI'].sum():.2f}")
        c3.metric("KUL KHARCHA", f"₹{t_df['TOTAL_INV'].sum():.2f}")
        c4.metric("NET PROFIT", f"₹{t_df['PROFIT'].sum():.2f}")

        st.divider()
        st.dataframe(t_df, use_container_width=True)
    else:
        st.warning("Zoho Sheet mein 'TRACTOR' column nahi mila. Check karein!")
else:
    st.info("Bhai, Zoho Sheet publish nahi hai ya khali hai. Upar diye gaye steps follow karein!")
