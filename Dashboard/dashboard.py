import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# Load data
day_data = pd.read_csv('./dashboard/day.csv')
hour_data = pd.read_csv('./dashboard/hour.csv')

data = day_data.merge(hour_data, on='dteday', how='inner', suffixes=('_daily', '_hourly'))

# Dashboard Title
st.title(" Bike Sharing Trends Analysis")
st.write("**By: Bagas Rizky Ramadhan**")

# pertanyaan 1
st.header(" Bagaimana Pola Penyewaan Berdasarkan Cuaca?")

season_avg = data.groupby('season_daily')[['casual_daily', 'registered_daily']].mean().reset_index()
season_avg['season_name'] = ['Spring', 'Summer', 'Fall', 'Winter']

fig_season = px.bar(
    season_avg, x='season_name', y=['casual_daily', 'registered_daily'],
    labels={'value': 'Jumlah Rata-rata Penyewaan', 'season_name': 'Musim'},
    title="Rata-rata Penyewaan Sepeda Berdasarkan Musim",
    barmode='group', color_discrete_sequence=['#1f77b4', '#ff7f0e']
)
st.plotly_chart(fig_season)

st.write("Dari analisis, terlihat bahwa penyewaan sepeda oleh pengguna casual meningkat di musim gugur, kemungkinan karena cuaca yang nyaman. Sebaliknya, pengguna terdaftar lebih stabil sepanjang musim. Musim dingin memiliki jumlah penyewaan paling sedikit karena kondisi cuaca ekstrem.")

# Pertanyaan 2
st.header(" Bagaimana Perubahan Penyewaan Sepeda dalam Sehari?")

hour_avg = data.groupby('hr')[['casual_hourly', 'registered_hourly']].mean().reset_index()

fig_hourly = px.line(
    hour_avg, x='hr', y=['casual_hourly', 'registered_hourly'],
    labels={'value': 'Jumlah Penyewaan', 'hr': 'Jam'},
    title="Pola Penyewaan Sepeda dalam 24 Jam",
    markers=True, color_discrete_sequence=['#2ca02c', '#d62728']
)
st.plotly_chart(fig_hourly)

st.write("Penyewaan sepeda mencapai puncak pada sore hari sekitar pukul 17-18, yang menunjukkan banyaknya pengguna yang memakai sepeda setelah jam kerja atau sekolah. Pengguna terdaftar cenderung menyewa lebih banyak pada pagi hari untuk keperluan komuter.")

# Business Question 3
st.header(" Perbedaan Penyewaan pada Hari Kerja dan Libur")

workingday_avg = data.groupby('workingday_daily')['cnt_daily'].mean().reset_index()
workingday_avg['day_type'] = ['Hari Libur', 'Hari Kerja']

fig_workingday = px.bar(
    workingday_avg, x='day_type', y='cnt_daily',
    labels={'cnt_daily': 'Rata-rata Penyewaan', 'day_type': 'Jenis Hari'},
    title="Perbandingan Penyewaan Sepeda pada Hari Kerja dan Hari Libur",
    color='day_type', color_discrete_map={'Hari Libur': '#e377c2', 'Hari Kerja': '#17becf'}
)
st.plotly_chart(fig_workingday)

st.write("Jumlah penyewaan sepeda lebih tinggi pada hari kerja karena aktivitas rutin masyarakat. Namun, pada akhir pekan, penyewaan oleh pengguna casual meningkat karena banyak orang bersepeda untuk rekreasi.")

# Kesimpulan
st.header(" Kesimpulan")
st.markdown('''
- **Musim gugur memiliki penyewaan tertinggi**, terutama untuk pengguna casual yang menikmati cuaca sejuk.
- **Jam sibuk penyewaan terjadi sore hari** sekitar pukul 17-18, menunjukkan tingginya penggunaan setelah jam kerja.
- **Hari kerja memiliki lebih banyak penyewaan** oleh pengguna terdaftar, sedangkan akhir pekan menarik lebih banyak pengguna casual.
''')

st.caption("© 2025 - Bagas Rizky Ramadhan")
