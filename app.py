import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
from views.agencies import agencies_page
from views.comparatives import comparatives_page

st.set_page_config('Global Space Exploration Dataset', page_icon='🚀🌌', layout='wide')
st.image("./img/photo1.png", use_container_width=True)
st.title('Global Space Exploration Dataset', text_alignment='center')

@st.cache_data
def data_loading():
    return pd.read_csv(Path(__file__).parent/'data/exploration_cleaned.csv')

df = data_loading()
df.columns = df.columns.str.strip()

tab_main, tab_agencies, tab_comparatives = st.tabs(["📊 OVERVIEW", "🚀 SPACES AGENCIES", "↔️ COMPARATIVES"])

with tab_main:
    min_year = int(df['Year'].min())
    max_year = int(df['Year'].max())
    year_range = st.slider("Filter by year range", min_year, max_year, (min_year, max_year))
    
    df_filtered = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])]
    
    col1, col2, col3 = st.columns(3)
    
    avg_success = df_filtered['Rate'].mean()
    total_budget = df_filtered['Budget'].sum()
    num_agencies = df_filtered['Space_Agency'].nunique()
    
    col1.metric("Average Success Rate", f"{avg_success:.2f}%")
    col2.metric("Total Budget", f"{total_budget:,.2f}")
    col3.metric("Space Agencies", num_agencies)
    
    st.markdown("---")

    st.subheader("📈 Evolution of Space Investment")
    
    budget_trend = df_filtered.groupby('Year')['Budget'].sum().reset_index()
  
    st.area_chart(
        data=budget_trend, 
        x='Year', 
        y='Budget', 
        use_container_width=True,
        color="#005088" 
    )
    
    st.caption("Interactive chart: X axis shows the selected years and Y axis shows the total accumulated budget.")

    st.subheader("🏆 Top 5 Agencies by Investment")
    
    top_agencies = df_filtered.groupby('Space_Agency')['Budget'].sum().sort_values(ascending=False).head(5)
    
    top_agencies_df = top_agencies.reset_index()
    
    st.bar_chart(
        data=top_agencies_df,
        x='Space_Agency',
        y='Budget',
        horizontal=True,
        color="#11caa0" 
    )
    
    st.markdown("---")
    
    st.subheader(f"Data from {year_range[0]} to {year_range[1]}")
    st.dataframe(df_filtered, use_container_width=True)

with tab_agencies:
    st.subheader("Space Agency Analysis")
    agencies_page(df)

with tab_comparatives:
    st.subheader("Comparatives")
    comparatives_page(df)
