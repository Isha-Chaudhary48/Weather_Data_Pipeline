import streamlit as st
import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv
import psycopg2
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import datetime

load_dotenv()

DB_URI = os.getenv("DB_URI")

@st.cache_data(ttl=43200)
def get_data():
    conn = psycopg2.connect(DB_URI)
    query = "SELECT * FROM weather_data"
    df = pd.read_sql(query,conn)
    conn.close()
    fetch_time = datetime.now()
    return df,fetch_time


st.set_page_config(
    page_title="Weather Dashboard",
    layout = "wide"
)
df, fetch_time = get_data()


st.markdown(
    "<h1 style='color:lightblue; font-size:2.5rem; text-align:center'>Weather Data Analysis </h1>",
    unsafe_allow_html=True
)
st.markdown("Analyze temperature, humidity, and trends across cities")

st.sidebar.title("Filters")

selected_cities=st.sidebar.multiselect("Select Cities",
                       options=df['city'].unique(),
                       default=df['city'].unique()[:5])

df['date'] = pd.to_datetime(df['recorded_at']).dt.date
min_date = df['date'].min()
max_date= df['date'].max()

selected_dates = st.sidebar.date_input(
    "Selected Date Range",
    [min_date,max_date]
)


filtered_df = df[(df['city'].isin(selected_cities)) 
                 & (df['date'] >= selected_dates[0])
                 & (df['date'] <=selected_dates[1])]





max_temp = filtered_df['temperature'].max()
avg_temp = filtered_df['temperature'].mean()

max_humidity = filtered_df['humidity'].max()
avg_humidity = filtered_df['humidity'].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric("🌡️ Max Temp", f"{max_temp:.1f} °C")
col2.metric("🌡️ Avg Temp", f"{avg_temp:.1f} °C")

col3.metric("💧 Max Humidity", f"{max_humidity:.1f} %")
col4.metric("💧 Avg Humidity", f"{avg_humidity:.1f} %")


col1,col2 = st.columns(2)
col3,col4 = st.columns(2)

with col1:
    st.markdown("Top cities By temprature")
    city_avg = filtered_df.groupby('city')['temperature'].mean().sort_values(ascending = False).reset_index()
    fig = px.bar(city_avg,x='city',y='temperature',color='city',  
    color_discrete_sequence=px.colors.qualitative.Set3)
    st.plotly_chart(fig)

with col2:
    st.markdown("Temprature Trend")
    temp_trend = filtered_df.groupby('date')['temperature'].mean()
    st.line_chart(temp_trend)
with col3:
    st.markdown("Temp vs feels like")
    compare_df = filtered_df.groupby('date')[['temperature','feels_like']].mean()
    st.line_chart(compare_df)
    
with col4:
    st.markdown("Weather Distribution")
    weather_count = filtered_df['weather'].value_counts().reset_index()
    weather_count.columns = ['weather', 'count']

    fig = px.bar(weather_count,x='weather',y='count',color='weather',  
    color_discrete_sequence=px.colors.qualitative.Set2)
    st.plotly_chart(fig)


st.write(filtered_df.head())

st.sidebar.caption(f"Data fetched at: {fetch_time.strftime('%Y-%m-%d %H:%M:%S')}")







