import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# --- 1. App Configuration ---
st.set_page_config(page_title="JAVED RANGHAD TRACTOR KHATA", layout="wide")

# Google Sheet Link
SHEET_URL = "https://docs.google.com/spreadsheets/d/1K8Umx9q0IEka1O6IrIo1DrMcGgtxGbDW4raQybV_Ljg/edit?usp=sharing"

# Connection Setup
conn = st.connection("gsheets", type=GSheetsConnection)

def load_data():
    try:
        # Sheet se data read karna
        return conn.read(spreadsheet=SHEET_URL)
    except:
        return pd.DataFrame(columns=["DATE", "TRACTOR", "DRIVER_NAME", "WEIGHT", "RATE", "KAMAI", "DIESEL", "DRIVER_EXP", "OTHER", "TOTAL_INV", "PROFIT"])

# Custom CSS for Design & Visibility
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
    [data-testid="stSidebar"] label {{ color: #FFFFFF !important; font-size: 22px !important; font-weight: 900 !important; }}
    [data-testid="stSidebar"] input {{ color: #000000 !important; font-weight: 900 !important; font-size: 18px !important; }}
    [data-testid="stMetricValue"] div {{ font-size: 50px !important; font-weight: 950 !important; color: #800000 !important; }}
    [data-testid="stExpander"] {{ background-color: #FFFFFF !important; border-radius: 10px !important; }}
    [data-testid="stExpander"] p {{ color: #000000 !important; font-weight: 900 !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. Data Processing ---
df = load_data()
base_tractors = ["FARMTRACK 60", "MAHINDRA NOVO 605", "NAGISH 106"]
if not df.empty and "TRACTOR" in df.columns:
    existing_tractors = df["TRACTOR"].unique().tolist()
    base_tractors = sorted(list(set(base_tractors + existing_tractors)))

# --- 3. Sidebar Setup ---
with st.sidebar:
    st.header("🚜 MENU")
    active_tractor = st.selectbox("Apna Tractor Chunein", base_tractors)
    st.divider()
    
    st.subheader("📝 Nayi Entry")
    date = st.date_input("Tarik")
    d_name = st.text_input("Driver ka Naam")
    weight = st.number_input("Weight (KG)", min_value=0.0)
    rate = st.number_input("Rate", min_value=0.0, format="%.4f")
    diesel = st.number_input("Diesel", min_value=0.0)
    d_pay = st.number_input("Driver Kharcha", min_value=0.0)
    other = st.number_input("Other Kharcha", min_value=0.0)

    if st.button("💾 SAVE TO GOOGLE SHEET"):
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
        st.success("Save Ho Gaya!")
        st.rerun()

# --- 4. Main Page Display ---
set_design()
st.markdown(f'<p class="big-cherry-title">{active_tractor}</p>', unsafe_allow_html=True)

if not df.empty and "TRACTOR" in df.columns:
    t_df = df[df["TRACTOR"] == active_tractor]
else:
    t_df = pd.DataFrame()

# Metrics
c1, c2, c3, c4 = st.columns(4)
if not t_df.empty:
    c1.metric("TOTAL WEIGHT", f"{t_df['WEIGHT'].sum():.2f} KG")
    c2.metric("KUL KAMAI", f"₹{t_df['KAMAI'].sum():.2f}")
    c3.metric("KUL KHARCHA", f"₹{t_df['TOTAL_INV'].sum():.2f}")
    c4.metric("NET PROFIT", f"₹{t_df['PROFIT'].sum():.2f}")
else:
    c1.metric("TOTAL WEIGHT", "0 KG")
    c2.metric("KUL KAMAI", "₹0")
    c3.metric("KUL KHARCHA", "₹0")
    c4.metric("NET PROFIT", "₹0")

st.divider()
st.dataframe(t_df, use_container_width=True)

# --- 5. DELETE BUTTON SECTION ---
with st.expander("🗑️ Galti Sudharein (Delete Entry)"):
    if not t_df.empty:
        # User ko index dikhana delete karne ke liye
        delete_row = st.selectbox("Kaunsa record hatana hai? (Row ID)", t_df.index)
        if st.button("Humesha ke liye hatayein"):
            # Original dataframe se row mita kar sheet update karna
            updated_df = df.drop(delete_row)
            conn.update(spreadsheet=SHEET_URL, data=updated_df)
            st.warning("Record Delete Ho Gaya!")
            st.rerun()
    else:
        st.info("Delete karne ke liye koi record nahi hai.")
