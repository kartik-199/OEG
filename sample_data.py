import streamlit as st
import pandas as pd

sample_csv_path = 'data.csv'

df = pd.read_csv(sample_csv_path)
st.title("Sample Data Generation")
st.write("This page generates synthetic sales data for two SKUs over a period of time.")

st.dataframe(df.head(10))

csv_bytes = df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download Sample Data CSV",
    data=csv_bytes,
    file_name='sample_data.csv',
    mime='text/csv'
)
