import streamlit as st
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(page_title="JAVED TRACTOR KHATA", layout="wide")

# Google Sheet CSV Link (Direct Read)
# Maine link ko change kiya hai taaki ye hamesha update rahe
SHEET_ID = "1K8Umx9q0IEka1O6IrIo1DrMcGgtxGbDW4raQybV_Ljg"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

def load_data():
    try:
        # Har baar fresh data uthayega
        return pd.read_csv(CSV_URL)
    except:
        return pd.DataFrame(columns=["DATE", "TRACTOR", "DRIVER_NAME", "WEIGHT", "RATE", "KAMAI", "DIESEL", "DRIVER_EXP", "OTHER", "TOTAL_INV", "PROFIT"])

# --- STYLE ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(255,255,255,0.7), rgba(255,255,255,0.7)), 
                    url("https://images.pexels.com/photos/2933243/pexels-photo-2933243.jpeg?auto=compress&cs=tinysrgb&w=1260");
        background-size: cover; background-attachment: fixed;
    }
    .main-title { 
        font-size: 60px !important; font-weight: 950 !important; color: #800000 !important; 
        text-align: center; text-transform: uppercase;
    }
    [data-testid="stSidebar"] { background-color: #800000 !important; }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: white !important; font-weight: 900 !important; border-bottom: 2px solid white;
    }
    [data-testid="stSidebar"] label p { color: white !important; font-weight: 800 !important; font-size: 20px !important; }
    [data-testid="stMetricValue"] div { font-size: 40px !important; font-weight: 900 !important; color: #800000 !important; }
    .save-btn { background-color: #ffffff; color: #800000; padding: 10px; border-radius: 5px; text-decoration: none; font-weight: bold; display: block; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- DISPLAY ---
df = load_data()
tractors = ["FARMTRACK 60", "MAHINDRA NOVO 605", "NAGISH 106"]

with st.sidebar:
    st.header("🚜 MENU")
    active_t = st.selectbox("Tractor Chunein", tractors)
    st.divider()
    
    st.subheader("📝 Nayi Entry")
    st.write("Bhai, data save karne ke liye niche button pe click karein:")
    # Yahan aap apna Google Form link daal sakte hain
    st.markdown('<a href="https://docs.google.com/spreadsheets/d/1K8Umx9q0IEka1O6IrIo1DrMcGgtxGbDW4raQybV_Ljg/edit" class="save-btn">📥 OPEN SHEET TO ADD DATA</a>', unsafe_allow_html=True)
    st.info("Sheet mein entry karke wapas aaiye, dashboard apne aap update ho jayega!")

st.markdown(f'<p class="main-title">{active_t}</p>', unsafe_allow_html=True)

# Filtering data
t_df = df[df["TRACTOR"] == active_t] if not df.empty and "TRACTOR" in df.columns else pd.DataFrame()

c1, c2, c3, c4 = st.columns(4)
if not t_df.empty:
    c1.metric("TOTAL WEIGHT", f"{t_df['WEIGHT'].sum():.2f}")
    c2.metric("KUL KAMAI", f"₹{t_df['KAMAI'].sum():.2f}")
    c3.metric("KUL KHARCHA", f"₹{t_df['TOTAL_INV'].sum():.2f}")
    c4.metric("NET PROFIT", f"₹{t_df['PROFIT'].sum():.2f}")
else:
    c1.metric("TOTAL WEIGHT", "0.00")
    c2.metric("KUL KAMAI", "₹0.00")
    c3.metric("KUL KHARCHA", "₹0.00")
    c4.metric("NET PROFIT", "₹0.00")

st.divider()
st.dataframe(t_df, use_container_width=True)

if st.button("🔄 REFRESH DATA"):
    st.rerun()
