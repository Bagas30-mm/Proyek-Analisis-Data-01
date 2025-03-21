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
st.title("Dashboard of Analyzing Bike Sharing Culture")
st.write("Bagas Rizky Ramadhan")

# Interactive Filter
season_options = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
selected_season = st.selectbox("Pilih Musim:", options=list(season_options.keys()), format_func=lambda x: season_options[x])

# Filter data based on selected season
df_filtered = df[df['season_daily'] == selected_season]

# Visualisasi penyewaan berdasarkan musim untuk casual dan registered users
st.subheader("Pengaruh Musim terhadap Penyewaan Sepeda")
seasonal_data_casual = df_filtered.groupby(['season_daily'])['casual_daily'].mean().reset_index()
seasonal_data_registered = df_filtered.groupby(['season_daily'])['registered_daily'].mean().reset_index()

fig_casual = px.bar(seasonal_data_casual, x='season_daily', y='casual_daily',
                    title=f'Rata-rata Sewa Harian (Casual Users) - {season_options[selected_season]}',
                    labels={'casual_daily': 'Rata-rata Jumlah Sewa Harian', 'season_daily': 'Musim'},
                    color='casual_daily', color_continuous_scale='reds', template='plotly_dark')

fig_registered = px.bar(seasonal_data_registered, x='season_daily', y='registered_daily',
                        title=f'Rata-rata Sewa Harian (Registered Users) - {season_options[selected_season]}',
                        labels={'registered_daily': 'Rata-rata Jumlah Sewa Harian', 'season_daily': 'Musim'},
                        color='registered_daily', color_continuous_scale='blues', template='plotly_dark')

st.plotly_chart(fig_casual)
st.plotly_chart(fig_registered)
