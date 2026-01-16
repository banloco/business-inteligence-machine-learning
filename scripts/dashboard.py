import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

st.title("Olist Data Dashboard")
engine = create_engine("postgresql://analyst:password123@localhost:5432/olist_ecommerce")

df = pd.read_sql("SELECT * FROM analytics.rfm_segmentation", engine)
st.write("### Répartition des segments", df['Segment'].value_counts())
st.bar_chart(df['Segment'].value_counts())