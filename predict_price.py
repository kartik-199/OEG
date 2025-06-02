import streamlit as st 
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor

def predict_price(X, y, model, current_price, cost):
    model.fit(X, y)
    price_range = np.linspace(current_price * 0.9, current_price * 1.1, 25)
    predicted_units = model.predict(price_range.reshape(-1, 1))
    predicted_units = np.maximum(predicted_units, 0)
    profits = (price_range - cost) * predicted_units
    max_profit_idx = np.argmax(profits)
    optimal_price = price_range[max_profit_idx]
    optimal_profit = profits[max_profit_idx]

    st.write(f"Optimal price based on {model.__class__.__name__}: ${optimal_price:.2f}")
    st.write(f"Estimated profit at optimal price: ${optimal_profit:.2f}")

    fig, ax = plt.subplots()
    ax.plot(price_range, profits, label="Estimated Profit")
    ax.axvline(optimal_price, color='red', linestyle='--', label="Optimal Price: ${:.2f}".format(optimal_price))
    ax.set_xlabel("Price")
    ax.set_ylabel("Estimated Profit")
    ax.set_title(f"Profit vs Price Curve ({model.__class__.__name__})")
    ax.legend() 
    st.pyplot(fig)