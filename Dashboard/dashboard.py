import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt

# Load data
day = pd.read_csv('./Dashboard/day.csv')
hour = pd.read_csv('./Dashboard/hour.csv')
df = day.merge(hour, on='dteday', how='inner', suffixes=('_daily', '_hourly'))

# Streamlit UI
st.title("Dashboard of Analyzing Bike Sharing Culture")
st.write("Bagas Rizky Ramadhan")

# Filter interaktif
st.sidebar.header("Filter Interaktif")
selected_season = st.sidebar.multiselect("Pilih Musim:", ['Spring', 'Summer', 'Fall', 'Winter'], default=['Spring', 'Summer', 'Fall', 'Winter'])
selected_workingday = st.sidebar.radio("Pilih Hari:", ['Semua', 'Hari Kerja', 'Hari Libur'])

# Mapping season names
df['season_name'] = df['season_daily'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})

# Filter data berdasarkan pilihan pengguna
filtered_df = df[df['season_name'].isin(selected_season)]
if selected_workingday == 'Hari Kerja':
    filtered_df = filtered_df[filtered_df['workingday_daily'] == 1]
elif selected_workingday == 'Hari Libur':
    filtered_df = filtered_df[filtered_df['workingday_daily'] == 0]

# Visualisasi Pertanyaan 1: Pengaruh Musim
st.subheader("1. Bagaimana musim memengaruhi penyewaan sepeda oleh pengguna casual dan registered?")
seasonal_data_casual = filtered_df.groupby(['season_daily'])['casual_daily'].mean().reset_index()
seasonal_data_registered = filtered_df.groupby(['season_daily'])['registered_daily'].mean().reset_index()
seasonal_data_casual['season_name'] = ['Spring', 'Summer', 'Fall', 'Winter']
seasonal_data_registered['season_name'] = ['Spring', 'Summer', 'Fall', 'Winter']
seasonal_data_casual = seasonal_data_casual.sort_values(by='casual_daily', ascending=False)
seasonal_data_registered = seasonal_data_registered.sort_values(by='registered_daily', ascending=False)

fig_casual = px.bar(seasonal_data_casual, x='season_name', y='casual_daily',
                    title='Jumlah Rata-rata Sewa Harian (Casual Users)',
                    labels={'casual_daily': 'Rata-rata Jumlah Sewa Harian', 'season_name': 'Musim'},
                    color='casual_daily', color_continuous_scale='reds', template='plotly_dark')

fig_registered = px.bar(seasonal_data_registered, x='season_name', y='registered_daily',
                        title='Jumlah Rata-rata Sewa Harian (Registered Users)',
                        labels={'registered_daily': 'Rata-rata Jumlah Sewa Harian', 'season_name': 'Musim'},
                        color='registered_daily', color_continuous_scale='blues', template='plotly_dark')

st.plotly_chart(fig_casual)
st.plotly_chart(fig_registered)

# Visualisasi Pertanyaan 2: Pola Aktivitas Sepanjang Hari
st.subheader("2. Seperti apa perubahan pola aktivitas penyewaan sepeda sepanjang hari?")

hourly_counts_total = filtered_df.groupby('hr')['cnt_hourly'].mean().reset_index()
fig_hourly = px.line(hourly_counts_total, x='hr', y='cnt_hourly', markers=True,
                     labels={'hr': 'Jam', 'cnt_hourly': 'Jumlah Penyewaan'},
                     title='Perubahan Pola Aktivitas Penyewaan Sepanjang Hari',
                     template='plotly_dark')
st.plotly_chart(fig_hourly)

# Visualisasi Pertanyaan 3: Selisih Penggunaan Sepeda Antara Hari Kerja dan Hari Libur
st.subheader("3. Berapa besar selisih penggunaan sepeda antara hari kerja dan hari libur?")

workingday_counts = filtered_df.groupby('workingday_daily')['cnt_daily'].mean().reset_index()
fig_workingday = px.bar(workingday_counts, x='workingday_daily', y='cnt_daily',
                        labels={'workingday_daily': 'Hari', 'cnt_daily': 'Jumlah Penyewaan'},
                        title='Selisih Penggunaan Sepeda Antara Hari Kerja dan Hari Libur',
                        color='workingday_daily', color_discrete_map={0: 'skyblue', 1: 'salmon'},
                        template='plotly_dark')
fig_workingday.update_xaxes(ticktext=["Hari Libur", "Hari Kerja"], tickvals=[0, 1])
st.plotly_chart(fig_workingday)

# Menampilkan kesimpulan dari analisis
st.header("Kesimpulan")
st.write("Dari semua hasil analisis berikut adalah kesimpulan keseluruhan dari semua data tersebut")
st.text('''1. Pengaruh Cuaca Terhadap Aktivitas Penyewaan:
- Aktivitas penyewaan mencapai puncaknya pada musim gugur, diduga dipengaruhi oleh kondisi cuaca yang menyenangkan dan pemandangan yang memikat.
- Walaupun terdapat penurunan, musim panas tetap menjadi salah satu periode dengan jumlah penyewaan yang tinggi.
- Musim dingin mengalami penurunan drastis dalam aktivitas penyewaan, kemungkinan disebabkan oleh cuaca yang kurang mendukung serta preferensi terhadap aktivitas di dalam ruangan.
- Musim semi menunjukkan tingkat penyewaan yang cukup stabil, meskipun masih lebih rendah dibandingkan dengan musim gugur dan musim panas.''')

st.text('''2. Pola Aktivitas Penyewaan Harian:
- Pengguna casual lebih sering menyewa sepeda pada sore hingga malam, mencerminkan kecenderungan mereka untuk melakukan aktivitas rekreasi di luar jam kerja.
- Pengguna terdaftar memiliki pola aktivitas yang berbeda, dengan penyewaan tertinggi pada pagi hari serta sore hingga malam, yang mengindikasikan penggunaan sepeda untuk perjalanan kerja atau kebutuhan harian.
- Secara keseluruhan, jumlah penyewaan mencapai puncaknya pada sore hingga malam hari.''')

st.text('''3. Perbedaan Penggunaan Sepeda antara Hari Kerja dan Hari Libur:
- Aktivitas penyewaan sepeda cenderung lebih tinggi pada hari kerja dibandingkan hari libur.
- Hari kerja memberikan kontribusi positif terhadap penggunaan sepeda, yang mungkin dipengaruhi oleh kebutuhan komutasi dan rutinitas harian.''')

st.caption('Copyright © Bagas Rizky R')
