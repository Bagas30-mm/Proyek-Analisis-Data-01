import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt

# Load data
day = pd.read_csv('./Dashboard/day.csv')
hour = pd.read_csv('./Dashboard/hour.csv') 

df = day.merge(hour, on='dteday', how='inner', suffixes=('_daily', '_hourly'))

# Streamlit App Title
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")
st.title("🚲 Dashboard of Analyzing Bike Sharing Culture")
st.write("### By Bagas Rizky Ramadhan")

# Sidebar Filters
st.sidebar.header("🔍 Filter Data")

# Filter by Date Range
df['dteday'] = pd.to_datetime(df['dteday'])
date_range = st.sidebar.date_input("Pilih Rentang Tanggal:", [df['dteday'].min(), df['dteday'].max()])
df_filtered = df[(df['dteday'] >= pd.to_datetime(date_range[0])) & (df['dteday'] <= pd.to_datetime(date_range[1]))]

# Filter by Season
season_options = {1: 'Spring 🌸', 2: 'Summer ☀️', 3: 'Fall 🍂', 4: 'Winter ❄️'}
selected_season = st.sidebar.radio("Pilih Musim:", options=list(season_options.keys()), format_func=lambda x: season_options[x])
df_filtered = df_filtered[df_filtered['season_daily'] == selected_season]

# Filter by Weather Condition
weather_options = {1: 'Clear ☀️', 2: 'Cloudy ☁️', 3: 'Light Rain 🌧️', 4: 'Heavy Rain ⛈️'}
selected_weather = st.sidebar.radio("Pilih Kondisi Cuaca:", options=list(weather_options.keys()), format_func=lambda x: weather_options[x])
df_filtered = df_filtered[df_filtered['weathersit_daily'] == selected_weather]

# Filter by Hour Range
hour_range = st.sidebar.slider("Pilih Rentang Jam:", 0, 23, (0, 23))
df_filtered = df_filtered[(df_filtered['hr'] >= hour_range[0]) & (df_filtered['hr'] <= hour_range[1])]

# Layout
col1, col2 = st.columns(2)

# Visualisasi penyewaan berdasarkan musim untuk casual dan registered users
st.subheader(f"📊 Pengaruh {season_options[selected_season]}, {weather_options[selected_weather]}, dan jam {hour_range[0]}-{hour_range[1]} terhadap Penyewaan Sepeda")

seasonal_data_casual = df_filtered.groupby(['season_daily'])['casual_daily'].mean().reset_index()
seasonal_data_registered = df_filtered.groupby(['season_daily'])['registered_daily'].mean().reset_index()

fig_casual = px.bar(seasonal_data_casual, x='season_daily', y='casual_daily',
                    title=f'🚴‍♂️ Casual Users - {season_options[selected_season]} ({weather_options[selected_weather]})',
                    labels={'casual_daily': 'Rata-rata Jumlah Sewa Harian', 'season_daily': 'Musim'},
                    color='casual_daily', color_continuous_scale='reds', template='plotly_white')

fig_registered = px.bar(seasonal_data_registered, x='season_daily', y='registered_daily',
                        title=f'👥 Registered Users - {season_options[selected_season]} ({weather_options[selected_weather]})',
                        labels={'registered_daily': 'Rata-rata Jumlah Sewa Harian', 'season_daily': 'Musim'},
                        color='registered_daily', color_continuous_scale='blues', template='plotly_white')

col1.plotly_chart(fig_casual, use_container_width=True)
col2.plotly_chart(fig_registered, use_container_width=True)

# Footer
st.markdown("---")
st.write("💡 **Tip:** Gunakan sidebar untuk mengeksplorasi data berdasarkan tanggal, musim, cuaca, dan jam!")
