import streamlit as st
import pandas as pd

# --- App Config ---
st.set_page_config(page_title="JAVED TRACTOR KHATA", layout="wide")

# SAHI ZOHO LINK (CSV FORMAT)
# Agar ye kaam na kare, toh niche Step 2 dekhein
ZOHO_URL = "https://sheet.zohopublic.in/sheet/publishedsheet/36364df8cd3cbedb7cd796ab0817ed93a1dfe6252a3c6b612288121c8a80d211?type=csv"

st.markdown("<h1 style='text-align: center; color: #800000;'>🚜 JAVED RANGHAD TRACTOR KHATA</h1>", unsafe_allow_html=True)

@st.cache_data(ttl=5)
def load_data():
    try:
        # header=1 ka matlab pehli row (Mahindra wali) ko chhod do, dusri row ko header maano
        df = pd.read_csv(ZOHO_URL, header=1)
        # Faltu space hatana
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except Exception as e:
        return pd.DataFrame()

df = load_data()

if not df.empty:
    # Metrics
    c1, c2, c3, c4 = st.columns(4)
    
    # Aapki sheet ke columns ke hisab se calculations
    w = pd.to_numeric(df['WEIGHT(KG)'], errors='coerce').sum() if 'WEIGHT(KG)' in df.columns else 0
    k = pd.to_numeric(df['TOTAL'], errors='coerce').sum() if 'TOTAL' in df.columns else 0
    kh = pd.to_numeric(df['TOTAL.1'], errors='coerce').sum() if 'TOTAL.1' in df.columns else 0
    p = pd.to_numeric(df['LOSS & PROFIT'], errors='coerce').sum() if 'LOSS & PROFIT' in df.columns else 0

    c1.metric("KUL WEIGHT", f"{w:,.0f} KG")
    c2.metric("KUL KAMAI", f"₹{k:,.0f}")
    c3.metric("KUL KHARCHA", f"₹{kh:,.0f}")
    c4.metric("NET PROFIT", f"₹{p:,.0f}")

    st.divider()
    st.write("### 📝 RECENT ENTRIES (Zoho Sheet)")
    st.dataframe(df, use_container_width=True)
else:
    st.error("❌ Data Nahi Mila!")
    st.info("Bhai, Zoho Sheet mein 'Publish' wala link sahi se set nahi hai. Niche Step 2 dekhein.")

if st.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.rerun()
