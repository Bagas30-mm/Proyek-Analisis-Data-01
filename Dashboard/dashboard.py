import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# Load data
day = pd.read_csv('./Dashboard/day.csv')
hour = pd.read_csv('./Dashboard/hour.csv')

df = day.merge(hour, on='dteday', how='inner', suffixes=('_daily', '_hourly'))

# Mengatur judul dan deskripsi aplikasi
st.title("Dashboard of Analyzing Bike Sharing Culture")
st.write("Bagas Rizky Ramadhan")

# Filter interaktif
selected_season = st.multiselect('Pilih Musim:', ['Spring', 'Summer', 'Fall', 'Winter'], default=['Spring', 'Summer', 'Fall', 'Winter'])
selected_workingday = st.multiselect('Pilih Hari:', ['Hari Kerja', 'Hari Libur'], default=['Hari Kerja', 'Hari Libur'])

# Mapping nama musim dan hari
season_map = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
df['season_name'] = df['season_daily'].map(season_map)
df['workingday_name'] = df['workingday_daily'].replace({0: 'Hari Libur', 1: 'Hari Kerja'})

# Filter data
filtered_df = df[(df['season_name'].isin(selected_season)) & (df['workingday_name'].isin(selected_workingday))]

# Pertanyaan 1: Bagaimana musim memengaruhi penyewaan sepeda oleh pengguna casual dan registered?
st.subheader("1. Bagaimana musim memengaruhi penyewaan sepeda oleh pengguna casual dan registered?")
# Group by daily season and calculate the mean for casual and registered users
seasonal_data_casual = df.groupby(['season_daily'])['casual_daily'].mean().reset_index()
seasonal_data_registered = df.groupby(['season_daily'])['registered_daily'].mean().reset_index()
seasonal_data_casual['season_name'] = ['Spring', 'Summer', 'Fall', 'Winter']
seasonal_data_registered['season_name'] = ['Spring', 'Summer', 'Fall', 'Winter']
seasonal_data_casual = seasonal_data_casual.sort_values(by='casual_daily', ascending=False)
seasonal_data_registered = seasonal_data_registered.sort_values(by='registered_daily', ascending=False)

casual_fig = px.bar(seasonal_data_casual, x='season_name', y='casual_daily',
                    title='Rata-rata Penyewaan Casual Berdasarkan Musim',
                    labels={'casual_daily': 'Rata-rata Jumlah Sewa Harian', 'season_name': 'Musim'},
                    color='casual_daily', color_continuous_scale='reds', template='plotly_dark')
st.plotly_chart(casual_fig)

registered_fig = px.bar(seasonal_data_registered, x='season_name', y='registered_daily',
                        title='Rata-rata Penyewaan Registered Berdasarkan Musim',
                        labels={'registered_daily': 'Rata-rata Jumlah Sewa Harian', 'season_name': 'Musim'},
                        color='registered_daily', color_continuous_scale='blues', template='plotly_dark')
st.plotly_chart(registered_fig)

# Pertanyaan 2: Seperti apa perubahan pola aktivitas penyewaan sepeda sepanjang hari?
st.subheader("2. Seperti apa perubahan pola aktivitas penyewaan sepeda sepanjang hari?")
hourly_counts_total = filtered_df.groupby('hr')['cnt_hourly'].mean().reset_index()
hourly_fig = px.bar(hourly_counts_total, x='hr', y='cnt_hourly',
                    title='Distribusi Penyewaan Sepeda Sepanjang Hari',
                    labels={'hr': 'Jam', 'cnt_hourly': 'Jumlah Penyewaan'},
                    color='cnt_hourly', color_continuous_scale='Burg', template='plotly_dark')
st.plotly_chart(hourly_fig)

# Pertanyaan 3: Berapa besar selisih penggunaan sepeda antara hari kerja dan hari libur?
st.subheader("3. Berapa besar selisih penggunaan sepeda antara hari kerja dan hari libur?")
fig_workingday = px.bar(filtered_df, x="workingday_name", y="cnt_daily", color="workingday_name",
                        labels={'workingday_name': 'Hari'},
                        title='Perbedaan Penggunaan Sepeda Harian Antara Hari Kerja dan Hari Libur.',
                        color_discrete_map={'Hari Libur': 'skyblue', 'Hari Kerja': 'salmon'})
st.plotly_chart(fig_workingday)

# Kesimpulan
st.header("Kesimpulan")
st.write("Dari semua hasil analisis berikut adalah kesimpulan keseluruhan dari semua data tersebut")
st.text('''1. Pengaruh Cuaca Terhadap Aktivitas Penyewaan:
- Aktivitas penyewaan mencapai puncaknya pada musim gugur, diduga dipengaruhi oleh kondisi cuaca yang menyenangkan dan pemandangan yang memikat.
- Walaupun terdapat penurunan, musim panas tetap menjadi salah satu periode dengan jumlah penyewaan yang tinggi.
- Musim dingin mengalami penurunan drastis dalam aktivitas penyewaan, yang kemungkinan disebabkan oleh cuaca yang kurang mendukung dan kecenderungan untuk melakukan aktivitas indoor.
- Musim semi menunjukkan tingkat penyewaan yang cukup stabil, meskipun masih lebih rendah dibandingkan dengan musim gugur dan musim panas.

2. Pola Aktivitas Penyewaan Harian:
- Pengguna casual lebih sering menyewa sepeda pada sore hingga malam, mencerminkan kecenderungan mereka untuk melakukan aktivitas rekreasi di luar jam kerja.
- Pengguna terdaftar memiliki pola aktivitas yang berbeda, dengan penyewaan tertinggi pada pagi hari serta sore hingga malam, yang mengindikasikan penggunaan sepeda untuk perjalanan kerja atau kebutuhan harian.
- Secara keseluruhan, jumlah penyewaan mencapai puncaknya pada sore hingga malam hari.

3. Perbedaan Penggunaan Sepeda antara Hari Kerja dan Hari Libur:
- Aktivitas penyewaan sepeda cenderung lebih tinggi pada hari kerja dibandingkan hari libur.
- Hari kerja memberikan kontribusi positif terhadap penggunaan sepeda, yang mungkin dipengaruhi oleh kebutuhan komutasi dan rutinitas harian.
- Untuk mengoptimalkan penyewaan, disarankan menyesuaikan penawaran pada hari kerja, seperti memberikan diskon di jam sibuk. Selain itu, pengembangan program khusus di hari libur, misalnya tur rekreasi atau paket promosi, dapat meningkatkan minat pelanggan.")

st.caption('Copyright © Bagas Rizky R')
