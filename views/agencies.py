import streamlit as st
import pandas as pd
import os
import plotly.express as px

def budget_agencies(df, name_agency):
    if st.button("⬅️ Back to Agencies"):
        st.session_state['selected_agency'] = None
        st.rerun()
        
    st.title(f"📊 Budget Analysis: {name_agency}")
    
    df_agency = df[df['Space_Agency'] == name_agency].copy()
    
    tech_col = 'Technology Used' if 'Technology Used' in df_agency.columns else ('Technology Used' if 'Technology Used' in df_agency.columns else None)
    
    if 'Year' in df_agency.columns and 'Budget' in df_agency.columns:
        df_agency['Year'] = pd.to_numeric(df_agency['Year'], errors='coerce')
        if df_agency['Budget'].dtype == 'object':
            df_agency['Budget'] = df_agency['Budget'].astype(str).str.replace('$', '', regex=False).str.replace(',', '', regex=False).str.strip()
        df_agency['Budget'] = pd.to_numeric(df_agency['Budget'], errors='coerce')
        
        df_agency = df_agency.dropna(subset=['Year', 'Budget'])
        
        if not df_agency.empty:
            fig_decade = px.histogram(
                df_agency, 
                x='Year', 
                y='Budget',
                histfunc='sum',
                title=f"Total Budget Distribution per Decades - {name_agency}",
                color_discrete_sequence=["#7CCE5C"],
                labels={'Year': 'Decade', 'Budget': 'Total Budget ($)'}
            )
            
            fig_decade.update_traces(
                xbins=dict(
                    start=df_agency['Year'].min(),
                    end=df_agency['Year'].max(),
                    size=10
                ),
                marker_line_width=1, 
                marker_line_color="white"
            )
            
            fig_decade.update_layout(
                margin=dict(l=20, r=20, t=50, b=20),
                height=380,
                xaxis=dict(tickmode='linear', dtick=10),
                template="plotly_dark",
                hovermode="x unified"
            )
            
            col_graphic, col_table = st.columns([2, 1])
            
            with col_graphic:
                st.plotly_chart(fig_decade, use_container_width=True)
                
            with col_table:
                st.markdown("### Data")
                df_agency['Decade'] = (df_agency['Year'] // 10).astype(int) * 10
                df_budget = df_agency.groupby('Decade')['Budget'].sum().reset_index().sort_values('Decade')
                st.dataframe(df_budget, use_container_width=True, hide_index=True)
            
            st.markdown("---")
            
            if tech_col:
                df_tech = df_agency.dropna(subset=[tech_col])
                if not df_tech.empty:
                    fig_tech = px.histogram(
                        df_tech,
                        x=tech_col,
                        y='Budget',
                        histfunc='sum',
                        title=f"Budget Allocation by Technology Used - {name_agency}",
                        color=tech_col,
                        color_discrete_sequence=px.colors.qualitative.Safe,
                        labels={tech_col: 'Technology Used', 'Budget': 'Total Budget ($)'}
                    )
                    
                    fig_tech.update_layout(
                        margin=dict(l=20, r=20, t=50, b=40),
                        height=400,
                        template="plotly_dark",
                        xaxis={'categoryorder':'total descending'},
                        showlegend=False
                    )
                    
                    col_tech_graph, col_tech_table = st.columns([2, 1])
                    
                    with col_tech_graph:
                        st.plotly_chart(fig_tech, use_container_width=True)
                        
                    with col_tech_table:
                        st.markdown("### Data")
                        df_tech_summary = df_tech.groupby(tech_col)['Budget'].sum().reset_index().sort_values('Budget', ascending=False)
                        st.dataframe(df_tech_summary, use_container_width=True, hide_index=True)
                else:
                    st.warning("No technology data available to display the chart.")
            else:
                st.warning("Technology column not found in the dataset.")
                
        else:
            st.warning(f"No budget data found for {name_agency}.")
    else:
        st.error("Columns 'Year' or 'Budget' not found in the dataset.")
        st.write("Available columns:", df_agency.columns.tolist())

def agencies_card(df):
    st.write("Select or explore the space agencies included in the global dataset.")

    lists = df['Space_Agency'].unique()
    
    cards_per_row = 4
    cols = st.columns(cards_per_row)
    
    for idx, current_agency in enumerate(lists):
        target_col = cols[idx % cards_per_row]
        
        with target_col:
            with st.container(border=True):
                
                name_img = f"{current_agency}.png"
                route_img = f"./img/agencies/{name_img}"
                
                if os.path.exists(route_img):
                    st.image(route_img, use_container_width=True)
                else:
                    st.image("https://images.unsplash.com/photo-1614728894747-a83421e2b9c9?w=400", use_container_width=True)
                
                st.markdown(f"### **{current_agency}**")
                
                total_missions = len(df[df['Space_Agency'] == current_agency])
                st.caption(f"🚀 Missions: **{total_missions}**")
                
                if st.button(f"View analysis", key=f"btn_{current_agency}"):
                    st.session_state['selected_agency'] = current_agency
                    st.rerun()

def agencies_page(df):
    if 'selected_agency' not in st.session_state:
        st.session_state['selected_agency'] = None

    if st.session_state['selected_agency'] is not None:
        budget_agencies(df, st.session_state['selected_agency'])
    else:
        agencies_card(df)