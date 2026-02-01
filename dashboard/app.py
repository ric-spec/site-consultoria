import streamlit as st
import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
st.set_page_config(page_title="BI Consultoria Oliver", layout="wide")

def get_data():
    conn = psycopg2.connect(os.getenv("DATABASE_URL"), sslmode='require')
    df = pd.read_sql("SELECT * FROM leads_consultoria", conn)
    conn.close()
    return df

st.title("📊 Dashboard de Governanca")
try:
    df = get_data()
    st.dataframe(df)
except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")