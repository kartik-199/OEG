import pandas as pd
from openai import OpenAI
import sys
from dotenv import load_dotenv
import os
import streamlit as st

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
api_key = os.getenv('OPENAI_API_KEY')

if not api_key:
    raise ValueError("Error: No OpenAI API key found. Please set the OPENAI_API_KEY environment variable.")

client = OpenAI(api_key=api_key)

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

