import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Load data
@st.cache
def load_data():
    df = pd.read_csv('crop.csv')
    return df

data = load_data()

# Sidebar Filters
st.sidebar.header("Filters")
states = st.sidebar.multiselect('Select States', options=data['State Name'].unique(), default=data['State Name'].unique())
years = st.sidebar.slider('Select Year Range', int(data['Year'].min()), int(data['Year'].max()), (int(data['Year'].min()), int(data['Year'].max())))

# Filter data based on selection
filtered_data = data[(data['State Name'].isin(states)) & (data['Year'].between(years[0], years[1]))]

# Title
st.title("Agricultural Data Analysis Dashboard")

# Tab-based Layout
tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Trends", "Comparisons", "Geospatial Analysis"])

# Tab 1: Overview
with tab1:
    st.header("Overview of Agricultural Production")
    
    # Display total area, production, yield for crops
    crops = [col for col in data.columns if 'AREA' in col or 'PRODUCTION' in col or 'YIELD' in col]
    crop_summary = filtered_data[crops].sum().reset_index()
    crop_summary.columns = ['Crop Metric', 'Total Value']
    
    st.dataframe(crop_summary)

# Tab 2: Trends Over Time
with tab2:
    st.header("Yearly Trends in Production, Area, and Yield")
    
    crop_choice = st.selectbox("Select Crop", options=[col.split()[0] for col in crops if 'AREA' in col])
    
    fig, ax = plt.subplots(3, 1, figsize=(10, 15))
    
    # Area Trend
    area_col = f'{crop_choice} AREA (1000 ha)'
    production_col = f'{crop_choice} PRODUCTION (1000 tons)'
    yield_col = f'{crop_choice} YIELD (Kg per ha)'
    
    sns.lineplot(data=filtered_data, x='Year', y=area_col, ax=ax[0])
    ax[0].set_title(f'{crop_choice} Area Over Time')
    
    # Production Trend
    sns.lineplot(data=filtered_data, x='Year', y=production_col, ax=ax[1])
    ax[1].set_title(f'{crop_choice} Production Over Time')
    
    # Yield Trend
    sns.lineplot(data=filtered_data, x='Year', y=yield_col, ax=ax[2])
    ax[2].set_title(f'{crop_choice} Yield Over Time')
    
    st.pyplot(fig)

# Tab 3: Comparisons
with tab3:
    st.header("Crop Comparisons")
    
    comparison_type = st.selectbox("Compare By", ['States', 'Districts'])
    
    if comparison_type == 'States':
        group_col = 'State Name'
    else:
        group_col = 'Dist Name'
    
    crop_metric = st.selectbox("Select Metric", ['Area', 'Production', 'Yield'])
    
    if crop_metric == 'Area':
        metric_col = f'{crop_choice} AREA (1000 ha)'
    elif crop_metric == 'Production':
        metric_col = f'{crop_choice} PRODUCTION (1000 tons)'
    else:
        metric_col = f'{crop_choice} YIELD (Kg per ha)'
    
    comparison_df = filtered_data.groupby(group_col)[metric_col].sum().reset_index()
    
    fig = px.bar(comparison_df, x=group_col, y=metric_col, title=f'{crop_choice} {crop_metric} by {comparison_type}')
    
    st.plotly_chart(fig)

# Tab 4: Geospatial Analysis
with tab4:
    st.header("Geospatial Visualization of Crop Data")
    
    map_metric = st.selectbox("Select Map Metric", ['Area', 'Production', 'Yield'])
    
    if map_metric == 'Area':
        metric_col = f'{crop_choice} AREA (1000 ha)'
    elif map_metric == 'Production':
        metric_col = f'{crop_choice} PRODUCTION (1000 tons)'
    else:
        metric_col = f'{crop_choice} YIELD (Kg per ha)'
    
    state_data = filtered_data.groupby('State Name')[metric_col].sum().reset_index()
    
    fig = px.choropleth(state_data, 
                        locations='State Name', 
                        locationmode='country names', 
                        color=metric_col, 
                        title=f'{crop_choice} {map_metric} by State', 
                        color_continuous_scale='Viridis')
    
    st.plotly_chart(fig)

# Footer
st.sidebar.markdown("Developed with ❤️ by [Your Name]")
