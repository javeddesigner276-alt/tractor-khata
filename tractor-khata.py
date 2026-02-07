import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# --- PAGE CONFIG ---
st.set_page_config(page_title="JAVED TRACTOR KHATA", layout="wide")

# Google Sheet Link
url = "https://docs.google.com/spreadsheets/d/1K8Umx9q0IEka1O6IrIo1DrMcGgtxGbDW4raQybV_Ljg/edit?usp=sharing"

# Connection Setup
conn = st.connection("gsheets", type=GSheetsConnection)

def load_data():
    try:
        # ttl=0 matlab har baar naya data uthayega
        return conn.read(spreadsheet=url, ttl=0)
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
    [data-testid="stSidebar"] input { color: black !important; font-weight: bold; }
    [data-testid="stMetricValue"] div { font-size: 40px !important; font-weight: 900 !important; color: #800000 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIC ---
df = load_data()
tractors = ["FARMTRACK 60", "MAHINDRA NOVO 605", "NAGISH 106"]

with st.sidebar:
    st.header("🚜 MENU")
    active_t = st.selectbox("Tractor Chunein", tractors)
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
        km = wt * rt
        inv = ds + dx + ot
        new_row = pd.DataFrame([{
            "DATE": str(dt), "TRACTOR": active_t, "DRIVER_NAME": dr,
            "WEIGHT": wt, "RATE": rt, "KAMAI": round(km, 2), 
            "DIESEL": ds, "DRIVER_EXP": dx, "OTHER": ot, 
            "TOTAL_INV": round(inv, 2), "PROFIT": round(km - inv, 2)
        }])
        
        # Naya Data purane ke niche jodna
        updated_df = pd.concat([df, new_row], ignore_index=True)
        # Sheet Update
        conn.update(spreadsheet=url, data=updated_df)
        st.success("Badhai ho! Data Sheet mein save ho gaya.")
        st.rerun()

# --- DISPLAY ---
st.markdown(f'<p class="main-title">{active_t}</p>', unsafe_allow_html=True)
t_df = df[df["TRACTOR"] == active_t] if not df.empty else pd.DataFrame()

c1, c2, c3, c4 = st.columns(4)
c1.metric("TOTAL WEIGHT", f"{t_df['WEIGHT'].sum() if not t_df.empty else 0:.2f}")
c2.metric("KUL KAMAI", f"₹{t_df['KAMAI'].sum() if not t_df.empty else 0:.2f}")
c3.metric("KUL KHARCHA", f"₹{t_df['TOTAL_INV'].sum() if not t_df.empty else 0:.2f}")
c4.metric("NET PROFIT", f"₹{t_df['PROFIT'].sum() if not t_df.empty else 0:.2f}")

st.divider()
st.dataframe(t_df, use_container_width=True)

with st.expander("🗑️ GALTI SUDHAREIN (DELETE)"):
    if not t_df.empty:
        row_id = st.selectbox("Delete karne ke liye Row chunein", t_df.index)
        if st.button("Humesha ke liye hatayein"):
            final_df = df.drop(row_id)
            conn.update(spreadsheet=url, data=final_df)
            st.warning("Data Mita Diya Gaya!")
            st.rerun()
