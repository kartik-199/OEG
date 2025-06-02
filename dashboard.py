import streamlit as st 
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

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

    st.subheader("Linear Regression Model")

    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X, y)


    price_range = np.linspace(current_price * 0.9, current_price * 1.1, 25)
    predicted_units = rf.predict(price_range.reshape(-1, 1))
    predicted_units = np.maximum(predicted_units, 0)
    profits = (price_range - cost) * predicted_units
    max_profit_idx = np.argmax(profits)
    optimal_price = price_range[max_profit_idx]
    optimal_profit = profits[max_profit_idx]

    st.write(f"Optimal price based on RF model: ${optimal_price:.2f}")
    st.write(f"Estimated profit at optimal price: ${optimal_profit:.2f}")

    fig, ax = plt.subplots()
    ax.plot(price_range, profits, label="Estimated Profit")
    ax.axvline(optimal_price, color='red', linestyle='--', label=f"Optimal Price: ${optimal_price:.2f}")
    ax.set_xlabel("Price")
    ax.set_ylabel("Estimated Profit")
    ax.set_title("Profit vs Price Curve (Random Forest Regressor)")
    ax.legend()
    st.pyplot(fig)

    st.subheader("Log Linear Regression Model")

    predicted_units = model.predict(np.log(price_range.reshape(-1, 1)))
    predicted_units = np.exp(predicted_units) 
    predicted_units = np.maximum(predicted_units, 0)

    profits = (price_range - cost) * predicted_units
    max_profit_idx = np.argmax(profits)
    optimal_price = price_range[max_profit_idx]
    optimal_profit = profits[max_profit_idx]

    st.write(f"Optimal price based on LR model: ${optimal_price:.2f}")
    st.write(f"Estimated profit at optimal price: ${optimal_profit:.2f}")

    fig, ax = plt.subplots()
    ax.plot(price_range, profits, label="Estimated Profit")
    ax.axvline(optimal_price, color='red', linestyle='--', label=f"Optimal Price: ${optimal_price:.2f}")
    ax.set_xlabel("Price")
    ax.set_ylabel("Estimated Profit")
    ax.set_title("Profit vs Price Curve (Linear Regression Model)")
    ax.legend()
    st.pyplot(fig)


else:
    st.info("Please upload a CSV file to proceed.")