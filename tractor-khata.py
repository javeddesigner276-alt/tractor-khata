import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# --- 1. App Configuration ---
st.set_page_config(page_title="JAVED RANGHAD TRACTOR KHATA", layout="wide")

# Aapka Google Sheet Link
SHEET_URL = "https://docs.google.com/spreadsheets/d/1K8Umx9q0IEka1O6IrIo1DrMcGgtxGbDW4raQybV_Ljg/edit?usp=sharing"

# Connection Setup
conn = st.connection("gsheets", type=GSheetsConnection)

def load_data():
    try:
        # ttl=0 isliye taaki refresh karne par naya data turant dikhe
        return conn.read(spreadsheet=SHEET_URL, ttl=0)
    except:
        return pd.DataFrame(columns=["DATE", "TRACTOR", "DRIVER_NAME", "WEIGHT", "RATE", "KAMAI", "DIESEL", "DRIVER_EXP", "OTHER", "TOTAL_INV", "PROFIT"])

# Custom Design
def set_design():
    img_url = "https://images.pexels.com/photos/2933243/pexels-photo-2933243.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
    st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(255,255,255,0.75), rgba(255,255,255,0.75)), url("{img_url}");
        background-size: cover; background-position: center; background-attachment: fixed;
    }}
    .big-cherry-title {{ 
        font-size: 100px !important; font-weight: 900 !important; color: #800000 !important; 
        text-align: center !important; margin-top: -50px !important; text-transform: uppercase;
    }}
    [data-testid="stSidebar"] {{ background-color: #800000 !important; }}
    [data-testid="stSidebar"] label {{ color: #FFFFFF !important; font-size: 20px !important; font-weight: 900 !important; }}
    [data-testid="stMetricValue"] div {{ font-size: 45px !important; font-weight: 950 !important; color: #800000 !important; }}
    /* Expander box styling */
    [data-testid="stExpander"] {{ background-color: white !important; border-radius: 10px; }}
    [data-testid="stExpander"] p {{ color: black !important; font-weight: bold; }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. Data Load ---
df = load_data()
base_tractors = ["FARMTRACK 60", "MAHINDRA NOVO 605", "NAGISH 106"]
if not df.empty and "TRACTOR" in df.columns:
    existing = [t for t in df["TRACTOR"].unique().tolist() if pd.notna(t)]
    base_tractors = sorted(list(set(base_tractors + existing)))

# --- 3. Sidebar ---
with st.sidebar:
    st.header("🚜 MENU")
    active_tractor = st.selectbox("Tractor Chunein", base_tractors)
    st.divider()
    
    st.subheader("📝 Nayi Entry")
    date = st.date_input("Tarik")
    d_name = st.text_input("Driver ka Naam")
    weight = st.number_input("Weight (KG)", min_value=0.0)
    rate = st.number_input("Rate", min_value=0.0, format="%.4f")
    diesel = st.number_input("Diesel", min_value=0.0)
    d_pay = st.number_input("Driver Kharcha", min_value=0.0)
    other = st.number_input("Other Kharcha", min_value=0.0)

    if st.button("💾 SAVE TO SHEET"):
        kamai = weight * rate
        total_inv = diesel + d_pay + other
        new_row = pd.DataFrame([{
            "DATE": str(date), "TRACTOR": active_tractor, "DRIVER_NAME": d_name,
            "WEIGHT": weight, "RATE": rate, "KAMAI": round(kamai, 2), 
            "DIESEL": diesel, "DRIVER_EXP": d_pay, "OTHER": other, 
            "TOTAL_INV": round(total_inv, 2), "PROFIT": round(kamai - total_inv, 2)
        }])
        updated_df = pd.concat([df, new_row], ignore_index=True)
        conn.update(spreadsheet=SHEET_URL, data=updated_df)
        st.success("Entry Save Ho Gayi!")
        st.rerun()

# --- 4. Main Display ---
set_design()
st.markdown(f'<p class="big-cherry-title">{active_tractor}</p>', unsafe_allow_html=True)

t_df = df[df["TRACTOR"] == active_tractor] if not df.empty else pd.DataFrame()

c1, c2, c3, c4 = st.columns(4)
c1.metric("TOTAL WEIGHT", f"{t_df['WEIGHT'].sum() if not t_df.empty else 0:.2f} KG")
c2.metric("KUL KAMAI", f"₹{t_df['KAMAI'].sum() if not t_df.empty else 0:.2f}")
c3.metric("KUL KHARCHA", f"₹{t_df['TOTAL_INV'].sum() if not t_df.empty else 0:.2f}")
c4.metric("NET PROFIT", f"₹{t_df['PROFIT'].sum() if not t_df.empty else 0:.2f}")

st.divider()
st.dataframe(t_df, use_container_width=True)

# --- 5. Delete Section ---
with st.expander("🗑️ Galti Sudharein (Delete)"):
    if not t_df.empty:
        # Hum index list dikhayenge taaki sahi record delete ho
        options = t_df.index.tolist()
        to_delete = st.selectbox("Hatane ke liye Row chunein", options)
        if st.button("Confirm Delete"):
            new_df = df.drop(to_delete)
            conn.update(spreadsheet=SHEET_URL, data=new_df)
            st.warning("Record Delete Ho Gaya!")
            st.rerun()
    else:
        st.write("Delete karne ke liye koi data nahi hai.")
