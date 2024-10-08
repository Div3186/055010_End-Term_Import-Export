# Import libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt

# Load data
df = pd.read_csv('Divyank End Term Final Project Import Export.csv')
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# Page configuration
st.set_page_config(
    page_title="Import-Export Dashboard",
    page_icon="📦",
    layout="wide"
)

# Sidebar Styling and Options
st.sidebar.title('📦 Import-Export Dashboard')
st.sidebar.write("Choose your preferences below:")

# Theme selector
theme = st.sidebar.selectbox('Choose a Theme', ['Light', 'Dark'])
if theme == 'Dark':
    st.markdown("<style>body {background-color: #121212; color: white;}</style>", unsafe_allow_html=True)

# Year and Country Filters
year_list = sorted(df['Date'].dt.year.dropna().unique(), reverse=True)
selected_year = st.sidebar.selectbox('Select Year', year_list)

country_list = df['Country'].dropna().unique()
selected_countries = st.sidebar.multiselect('Select Countries', country_list, default=country_list[:5])

df_filtered = df[(df['Date'].dt.year == selected_year) & (df['Country'].isin(selected_countries))]

# Metrics
st.title(f"Import-Export Analysis for {selected_year}")
col1, col2 = st.columns(2)

with col1:
    highest_value = df_filtered['Value'].max()
    highest_country = df_filtered[df_filtered['Value'] == highest_value]['Country'].values[0]
    st.metric(label="Top Country by Value", value=highest_country, delta=highest_value)

with col2:
    lowest_value = df_filtered['Value'].min()
    lowest_country = df_filtered[df_filtered['Value'] == lowest_value]['Country'].values[0]
    st.metric(label="Lowest Country by Value", value=lowest_country, delta=lowest_value)

# Tab layout
tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Scatter Plot", "Box Plot", "Donut & Treemap"])

# Tab 1 - Overview: Line Chart
with tab1:
    st.subheader('Transactions Over Time')
    line_chart = alt.Chart(df_filtered).mark_line().encode(
        x='Date:T',
        y='Value:Q',
        color='Category:N',
        tooltip=['Date:T', 'Value:Q', 'Category:N']
    ).interactive()
    st.altair_chart(line_chart, use_container_width=True)

# Tab 2 - Scatter Plot
with tab2:
    st.subheader('Country-wise Transaction Value')
    scatter_plot = px.scatter(
        df_filtered, x='Country', y='Value', color='Category',
        size='Value', hover_name='Country', title="Scatter Plot of Transaction Value by Country"
    )
    st.plotly_chart(scatter_plot, use_container_width=True)

# Tab 3 - Box Plot
with tab3:
    st.subheader('Transaction Value Distribution by Category')
    box_plot = px.box(
        df_filtered, x='Category', y='Value', color='Category',
        title="Box Plot of Transaction Value by Category"
    )
    st.plotly_chart(box_plot, use_container_width=True)

# Tab 4 - Donut Chart & Treemap
with tab4:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Value Distribution by Category')
        donut_chart = px.pie(
            df_filtered, values='Value', names='Category', hole=0.3,
            title="Donut Chart for Value Distribution by Category"
        )
        st.plotly_chart(donut_chart, use_container_width=True)
    with col2:
        st.subheader('Category and Country Breakdown')
        treemap_chart = px.treemap(
            df_filtered, path=['Category', 'Country'], values='Value',
            title="Treemap: Category and Country Breakdown"
        )
        st.plotly_chart(treemap_chart, use_container_width=True)

# Footer with download options
st.sidebar.markdown("---")
st.sidebar.subheader("Download Options")
download_button = st.sidebar.button("Download Filtered Data as CSV")
if download_button:
    csv = df_filtered.to_csv(index=False).encode()
    st.sidebar.download_button(
        label="Download CSV",
        data=csv,
        file_name='filtered_data.csv',
        mime='text/csv'
    )

st.sidebar.write("Created by Divyank Harjani | © 2024")
