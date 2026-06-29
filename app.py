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
    st.subheader("Global Dataset")
    st.dataframe(df, use_container_width=True)
    
with tab_agencies:
    st.subheader("Spaces Agency Analysis")
    agencies_page(df)

with tab_comparatives:
    st.subheader("Comparatives")
    comparatives_page(df)
