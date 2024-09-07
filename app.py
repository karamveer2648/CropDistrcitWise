import streamlit as st
import pandas as pd
@st.cache

def loaddata():
    df = pd.read_csv("crop.csv")
    return df

data = loaddata()


st.sidebar.header("Filters")
states = st.sidebar.multiselect('Select States', options=data['State Name'].unique(), default=data['State Name'].unique())