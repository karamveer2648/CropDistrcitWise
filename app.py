import streamlit as st
import pandas as pd
@st.cache

def loaddata()
    df = pd.read_csv("crop.csv")
    return df

data = loaddata()


st.sidebar.header("Filters")
st.sidebar.multiselect('Select a State', options=data.['State Name'].unique())
