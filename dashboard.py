import pandas as pd
import seaborn as sns
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

#load Covid data
@st.cache_data
def load_data():
    df = pd.read_csv('data_without_region_agg.csv')
    return df

df = load_data()  

#page configuration
st.set_page_config(
    layout="wide",
    page_icon=":bar_chart:",
    page_title="COVID-19 Data Explorer")

#page title
st.title("COVID-19 Data Explorer Dashboard")

#sidebar for filters
st.sidebar.header("Filter Here:")


#dropdown selector for country
country = st.sidebar.selectbox(
    "Select the Country for Case Breakdown and Bar Graph:",
    options=df['Country/Region'].unique(),
)


# Number of Deaths slider filter 
min_deaths = int(df['Deaths'].min())
max_deaths = int(df['Deaths'].max())
deaths_range = st.sidebar.slider(
    "Select the range of Deaths for Scatter Plot:",
    min_value=min_deaths,
    max_value=max_deaths,
    value=(min_deaths, max_deaths),
    step=1000
)

# Display country stats
st.header(f"Stats for {country}")
country_data = df[df['Country/Region'] == country].iloc[0]

col1, col2, col3 = st.columns(3)
col1.metric("Confirmed", f"{country_data['Confirmed']:,}")
col2.metric("Deaths", f"{country_data['Deaths']:,}")
col3.metric("Recovered", f"{country_data['Recovered']:,}")

# Chart 1: Country breakdown
st.subheader("Cases Breakdown")
fig1 = px.bar(
    x=['Confirmed', 'Deaths', 'Recovered', 'Active'],
    y=[country_data['Confirmed'], country_data['Deaths'], 
       country_data['Recovered'], country_data['Active']],
    labels={'x': 'Metric', 'y': 'Count'}
)
st.plotly_chart(fig1, use_container_width=True)

# Chart 2: Scatter with filter
st.subheader(f"Countries with Deaths between {deaths_range[0]:,} and {deaths_range[1]:,}")
filtered = df[(df['Deaths'] >= deaths_range[0]) & (df['Deaths'] <= deaths_range[1])]

st.info(f"{len(filtered)} countries | CFR range: {filtered['Case_Fatality_Rate'].min():.2f}% to {filtered['Case_Fatality_Rate'].max():.2f}%")

fig2 = px.scatter(
    filtered,
    size='Case_Fatality_Rate',
    x='Confirmed',
    y='Deaths',
    color='WHO Region',
    hover_name='Country/Region',
    hover_data={'Confirmed': ':,', 'Deaths': ':,', 'Case_Fatality_Rate': ':.2f'},
    title='Confirmed Cases vs Deaths',
    size_max=30 ,  
    opacity=0.7
)

st.plotly_chart(fig2, use_container_width=True)

