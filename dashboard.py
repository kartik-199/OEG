import streamlit as st 
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from predict_price import predict_price
st.title("Welcome to the Pricing Dashboard")

uploaded_file = st.file_uploader("Upload your historical sales data CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("Data Preview:", df.head())

    sku_filter = st.selectbox("Select SKU", options=df['SKU'].unique())
    sku_data = df[df['SKU'] == sku_filter]

    sku_data['Date'] = pd.to_datetime(sku_data['Date'])
    st.line_chart(sku_data.set_index('Date')['Units_Sold'])

    X = sku_data[['Price']]
    y = sku_data['Units_Sold']

    model = LinearRegression().fit(np.log(X), np.log(y))

    coef = model.coef_[0]
    intercept = model.intercept_

    avg_price = sku_data['Price'].mean()    
    avg_units = sku_data['Units_Sold'].mean()

    elasticity = coef * (avg_price / avg_units)
    st.write(f"Estimated price elasticity for SKU {sku_filter}: {elasticity:.2f}")
    cost = st.number_input("Enter cost for SKU", value=float(sku_data['Cost'].iloc[0]))

    sku_data = sku_data.sort_values(by='Date', ascending=False)
    most_recent_price = sku_data['Price'].iloc[0]
    current_price = most_recent_price
    st.write(f"Most recent price: ${current_price:.2f}")

    st.header("ML Modeling for Optimal Pricing")

    st.subheader("Random Forests Ensemble Model")
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    predict_price(X, y, rf, current_price, cost)

    st.subheader("Log Linear Regression Model")
    predict_price(X, y, LinearRegression(), current_price, cost)


else:
    st.info("Please upload a CSV file to proceed.")