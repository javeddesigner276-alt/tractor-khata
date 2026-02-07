import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="JAVED TRACTOR KHATA", layout="wide")

# Aapka Sheet Link
SHEET_URL = "https://docs.google.com/spreadsheets/d/1K8Umx9q0IEka1O6IrIo1DrMcGgtxGbDW4raQybV_Ljg/edit?usp=sharing"

# Connection
conn = st.connection("gsheets", type=GSheetsConnection)

def load_data():
    try:
        return conn.read(spreadsheet=SHEET_URL, ttl=0)
    except:
        return pd.DataFrame(columns=["DATE", "TRACTOR", "DRIVER_NAME", "WEIGHT", "RATE", "KAMAI", "DIESEL", "DRIVER_EXP", "OTHER", "TOTAL_INV", "PROFIT"])

# --- 2. STYLE (WHITE & BOLD) ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(255,255,255,0.7), rgba(255,255,255,0.7)), 
                    url("https://images.pexels.com/photos/2933243/pexels-photo-2933243.jpeg?auto=compress&cs=tinysrgb&w=1260");
        background-size: cover; background-attachment: fixed;
    }
    .main-title { 
        font-size: 70px !important; font-weight: 950 !important; color: #800000 !important; 
        text-align: center; text-transform: uppercase; margin-top: -30px;
    }
    [data-testid="stSidebar"] { background-color: #800000 !important; }
    
    /* MENU & NAYI ENTRY - White & Bold */
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: white !important; font-weight: 900 !important; border-bottom: 2px solid white;
    }
    [data-testid="stSidebar"] label p { color: white !important; font-weight: 800 !important; font-size: 20px !important; }
    
    /* Input Boxes Text Black */
    [data-testid="stSidebar"] input { color: black !important; font-weight: bold; }
    
    /* Metrics */
    [data-testid="stMetricValue"] div { font-size: 40px !important; font-weight: 900 !important; color: #800000 !important; }
    
    /* Expander Box */
    [data-testid="stExpander"] { background-color: white !important; border-radius: 10px; border: 2px solid #800000; }
    [data-testid="stExpander"] p { color: black !important; font-weight: 900 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATA & LOGIC ---
df = load_data()
tractor_list = ["FARMTRACK 60", "MAHINDRA NOVO 605", "NAGISH 106"]

with st.sidebar:
    st.header("🚜 MENU")
    active_t = st.selectbox("Tractor Chunein", tractor_list)
    st.divider()
    
    st.subheader("📝 Nayi Entry")
    dt = st.date_input("Tarik")
    dr = st.text_input("Driver Name")
    wt = st.number_input("Weight (KG)", min_value=0.0)
    rt = st.number_input("Rate", min_value=0.0)
    ds = st.number_input("Diesel", min_value=0.0)
    dx = st.number_input("Driver Kharcha", min_value=0.0)
    ot = st.number_input("Other Kharcha", min_value=0.0)

    if st.button("💾 SAVE DATA"):
        total_kamai = wt * rt
        total_kharcha = ds + dx + ot
        net_profit = total_kamai - total_kharcha
        
        new_row = pd.DataFrame([{
            "DATE": str(dt), "TRACTOR": active_t, "DRIVER_NAME": dr,
            "WEIGHT": wt, "RATE": rt, "KAMAI": round(total_kamai, 2), 
            "DIESEL": ds, "DRIVER_EXP": dx, "OTHER": ot, 
            "TOTAL_INV": round(total_kharcha, 2), "PROFIT": round(net_profit, 2)
        }])
        
        updated_df = pd.concat([df, new_row], ignore_index=True)
        conn.update(spreadsheet=SHEET_URL, data=updated_df)
        st.success("Save Ho Gaya!")
        st.rerun()

# --- 4. DISPLAY ---
st.markdown(f'<p class="main-title">{active_t}</p>', unsafe_allow_html=True)

# Filtering data
t_df = df[df["TRACTOR"] == active_t] if not df.empty else pd.DataFrame()

# Dashboard Metrics
col1, col2, col3, col4 = st.columns(4)
if not t_df.empty:
    col1.metric("TOTAL WEIGHT", f"{t_df['WEIGHT'].sum():.2f}")
    col2.metric("KUL KAMAI", f"₹{t_df['KAMAI'].sum():.2f}")
    col3.metric("KUL KHARCHA", f"₹{t_df['TOTAL_INV'].sum():.2f}")
    col4.metric("NET PROFIT", f"₹{t_df['PROFIT'].sum():.2f}")
else:
    col1.metric("TOTAL WEIGHT", "0.00")
    col2.metric("KUL KAMAI", "₹0.00")
    col3.metric("KUL KHARCHA", "₹0.00")
    col4.metric("NET PROFIT", "₹0.00")

st.divider()
st.dataframe(t_df, use_container_width=True)

# Delete Option
with st.expander("🗑️ GALTI SUDHAREIN (DELETE)"):
    if not t_df.empty:
        row_id = st.selectbox("Kaunsa record hatana hai?", t_df.index)
        if st.button("Humesha ke liye hatayein"):
            final_df = df.drop(row_id)
            conn.update(spreadsheet=SHEET_URL, data=final_df)
            st.warning("Record Mita Diya Gaya!")
            st.rerun()
