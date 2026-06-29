import streamlit as st
import pandas as pd
import plotly.express as px

def comparatives_page(df):
    st.markdown("Select multiple agencies to compare their budget and mission performance side by side.")

    all_agencies = df['Space_Agency'].unique().tolist()
    selected_agencies = st.multiselect("Select agencies to compare:", all_agencies, default=all_agencies[:2])

    if selected_agencies:
        df_comp = df[df['Space_Agency'].isin(selected_agencies)].copy()

        df_comp['Budget'] = pd.to_numeric(df_comp['Budget'].astype(str).str.replace(r'[$,]', '', regex=True), errors='coerce')
        df_comp = df_comp.dropna(subset=['Budget', 'Year'])

        st.subheader("Budget Trend by Agency")
        df_comp['Decade'] = (df_comp['Year'] // 10).astype(int) * 10
        df_summary = df_comp.groupby(['Decade', 'Space_Agency'])['Budget'].sum().reset_index()

        fig = px.line(
            df_summary, 
            x='Decade', 
            y='Budget', 
            color='Space_Agency',
            markers=True,
            template="plotly_dark",
            title="Budget Evolution over Decades"
        )
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Raw Data Comparison")
        
        tabs = st.tabs([f"{a}" for a in selected_agencies] + ["Combined Summary"])
        
        for i, agency in enumerate(selected_agencies):
            with tabs[i]:
                st.dataframe(df_comp[df_comp['Space_Agency'] == agency], use_container_width=True)
        
        with tabs[-1]:
            st.dataframe(df_summary.pivot(index='Decade', columns='Space_Agency', values='Budget'), use_container_width=True)
        
        col_pie_left, col_pie_right = st.columns([1, 1])

        df_total = df_comp.groupby('Space_Agency')['Budget'].sum().reset_index()
        
        with col_pie_left:
            st.markdown("### Budget by Agency")
            st.dataframe(df_total.sort_values('Budget', ascending=False), use_container_width=True, hide_index=True)

        with col_pie_right:
            fig_pie = px.pie(
                df_total, 
                values='Budget', 
                names='Space_Agency', 
                hole=0.4,
                template="plotly_dark"
            )
            fig_pie.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=300)
            st.plotly_chart(fig_pie, use_container_width=True)

    else:
        st.info("Please select at least one agency from the dropdown menu to start the comparison.")