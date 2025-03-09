import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt



day = pd.read_csv('./Dashboard/day.csv')
hour = pd.read_csv('./Dashboard/hour.csv') 


df = day.merge(hour, on='dteday', how='inner', suffixes=('_daily', '_hourly'))

# Mengatur judul dan deskripsi aplikasi
st.title("Dashborad of Analyzing Bike Sharing Behavior")
st.write("Cakra Satriyadana")





# Menampilkan pertanyaan bisnis
st.subheader("1. Bagaimana pengaruh Cuaca terhadap Aktivitas Penyewaan Berdasarkan pengguna Casual Dan Registered")


st.subheader("Grafik Pisah Pengguna Casual Dan Registered")
# Group by daily season and calculate the mean for casual and registered users
seasonal_data_casual = df.groupby(['season_daily'])['casual_daily'].mean().reset_index()
seasonal_data_registered = df.groupby(['season_daily'])['registered_daily'].mean().reset_index()
seasonal_data_casual['season_name'] = ['Spring', 'Summer', 'Fall', 'Winter']
seasonal_data_registered['season_name'] = ['Spring', 'Summer', 'Fall', 'Winter']
seasonal_data_casual = seasonal_data_casual.sort_values(by='casual_daily', ascending=False)
seasonal_data_registered = seasonal_data_registered.sort_values(by='registered_daily', ascending=False)


fig_casual = px.bar(seasonal_data_casual, x='season_name', y='casual_daily',
                    title='Jumlah Rata-rata Sewa Harian (Casual Users)',
                    labels={'casual_daily': 'Rata-rata Jumlah Sewa Harian', 'season_name': 'Musim'},
                    color='casual_daily', color_continuous_scale='blues',template='plotly_dark')

# Plot for Registered Users
fig_registered = px.bar(seasonal_data_registered, x='season_name', y='registered_daily',
                        title='Jumlah Rata-rata Sewa Harian (Registered Users)',
                        labels={'registered_daily': 'Rata-rata Jumlah Sewa Harian', 'season_name': 'Musim'},
                        color='registered_daily', color_continuous_scale='reds',template='plotly_dark')

# Display the plots
st.plotly_chart(fig_casual)
st.plotly_chart(fig_registered)


st.subheader("Grafik Gabungan Pengguna Casual Dan Registered")
seasonal_data = df.groupby(['season_daily'])[['casual_daily', 'registered_daily']].mean().reset_index()
seasonal_data['season_name'] = ['Spring', 'Summer', 'Fall', 'Winter']
seasonal_data = seasonal_data.sort_values(by='casual_daily', ascending=False)

# Set up the Streamlit app
# Plot using Plotly Express
fig = px.bar(seasonal_data, x='season_name', y=['casual_daily', 'registered_daily'],
             title='Jumlah Rata-rata Aktivitas Penyewaaan Berdasarkan Kedua Pengguna',
             labels={'value': 'Rata-rata Jumlah Sewa Harian', 'variable': 'User Type', 'season_name': 'Musim'},
             color_discrete_sequence=['skyblue', 'salmon'],template='plotly_dark')

# Display the Plotly Express plot
st.plotly_chart(fig)

st.write("Pada musim gugur, pengguna casual menjadi kelompok dengan tingkat penyewaan sepeda tertinggi, didukung oleh cuaca yang nyaman dan kondisi lingkungan yang indah. Pengguna terdaftar juga menunjukkan tingkat penyewaan yang tinggi pada musim ini. Meskipun terjadi penurunan selama musim panas dibandingkan dengan musim gugur, musim panas tetap menjadi periode dengan tingkat penyewaan tinggi bagi pengguna casual dan relatif tinggi bagi pengguna terdaftar. Selama musim dingin, kedua kelompok mengalami penurunan tajam yang dapat diatributkan pada kondisi cuaca yang kurang mendukung dan preferensi untuk aktivitas indoor. Musim semi menunjukkan tingkat penyewaan moderat, dengan kecenderungan lebih rendah dibandingkan dengan musim gugur dan panas untuk kedua kelompok pengguna. Perbandingan antara pengguna casual dan terdaftar menunjukkan bahwa pengguna casual cenderung memiliki tingkat penyewaan lebih tinggi pada musim gugur, sementara pengguna terdaftar memiliki tingkat penyewaan lebih tinggi selama musim panas. Kedua kelompok mengalami penurunan yang serupa selama musim dingin, dan pola tingkat penyewaan relatif serupa terlihat pada musim semi.")




st.subheader("2. Bagaimana pola aktivitas penyewaan sepeda berubah dalam satu hari")


# Group by hourly and calculate the mean for casual users
# Casual Users
hourly_counts_casual = df.groupby('hr')['casual_hourly'].mean().reset_index()
fig_casual = px.bar(hourly_counts_casual, x='hr', y='casual_hourly', color='casual_hourly',
                    labels={'hr': 'Waktu Penyewaan', 'casual_hourly': 'Jumlah Penyewaan'},
                    title='Distribusi Penyewaan Sepeda berdasarkan Jam dalam Sehari (Casual Users)',
                    color_continuous_scale=px.colors.sequential.Magenta, template='plotly_dark')

# Registered Users
hourly_counts_registered = df.groupby('hr')['registered_hourly'].mean().reset_index()
fig_registered = px.bar(hourly_counts_registered, x='hr', y='registered_hourly', color='registered_hourly',
                        labels={'hr': 'Waktu Penyewaan', 'registered_hourly': 'Jumlah Penyewaan'},
                        title='Distribusi Penyewaan Sepeda berdasarkan Jam dalam Sehari (Registered Users)',
                        color_continuous_scale=px.colors.sequential.Teal, template='plotly_dark')

# Total Counts
hourly_counts_total = df.groupby('hr')['cnt_hourly'].mean().reset_index()
fig_total = px.bar(hourly_counts_total, x='hr', y='cnt_hourly', color='cnt_hourly',
                   labels={'hr': 'Waktu Penyewaan', 'cnt_hourly': 'Jumlah Penyewaan'},
                   title='Distribusi Penyewaan Sepeda berdasarkan Jam dalam Sehari (Total Counts)',
                   color_continuous_scale=px.colors.sequential.Burg, template='plotly_dark')

# Streamlit app
st.plotly_chart(fig_casual)
st.plotly_chart(fig_registered)
st.plotly_chart(fig_total)


st.write('Aktivitas penyewaan sepeda harian (casual users) menunjukkan pola tertinggi pada rentang waktu sore hingga malam, khususnya puncaknya sekitar pukul 17.00 hingga 18.00. Ini menunjukkan bahwa pengguna casual lebih cenderung menyewa sepeda untuk kegiatan rekreasi atau non-rutin pada periode tersebut.Pengguna terdaftar (registered users) memiliki pola aktivitas yang berbeda, dengan puncak aktivitas pada dua rentang waktu, yaitu pagi sekitar pukul 8.00 dan sore hingga malam sekitar pukul 17.00 hingga 18.00. Hal ini mungkin mengindikasikan bahwa pengguna terdaftar cenderung menggunakan sepeda untuk keperluan harian atau komutasi pada pagi dan sore hari.Secara keseluruhan, jumlah penyewaan sepeda (count) menunjukkan puncak aktivitas pada sore hingga malam. Pola ini mencerminkan gabungan dari kecenderungan pengguna casual dan registered users. Aktivitas penyewaan sepeda secara umum lebih tinggi pada periode tersebut, menunjukkan popularitas penggunaan sepeda pada waktu-waktu tersebut.')
     

st.subheader("3. Seberapa besar perbedaan penggunaan sepeda antara hari libur dan hari kerja")

# Plotly Express bar chart
fig = px.bar(df, x="workingday_daily", y="cnt_daily", color="workingday_daily",
             labels={'workingday_daily': 'Hari'},
             title='Perbandingan Penggunaan Sepeda per hari antara Hari Kerja dan Hari Libur',
             category_orders={'workingday_daily': [0, 1]},
             color_discrete_map={0: 'skyblue', 1: 'salmon'})

# Menambahkan label pada sumbu x
fig.update_xaxes(ticktext=["Hari Libur", "Hari Kerja"], tickvals=[0, 1])


# Streamlit app
st.plotly_chart(fig)


st.write('Perbandingan jumlah sewa sepeda antara hari kerja dan hari libur menunjukkan bahwa aktivitas penyewaan sepeda lebih tinggi pada hari kerja. Grafik menyoroti dampak positif hari kerja terhadap penggunaan sepeda, dengan jumlah sewa harian yang lebih tinggi dibandingkan hari libur. Rekomendasi untuk mengoptimalkan aktivitas penyewaan melibatkan penyesuaian penawaran pada hari kerja dengan memberikan diskon pada jam-jam sibuk. Pengembangan program khusus pada hari libur, seperti tur rekreasi atau penawaran paket, juga dapat meningkatkan daya tarik pelanggan. Analisis lebih lanjut terhadap faktor-faktor penyebab perbedaan aktivitas antara hari libur dan hari kerja direkomendasikan untuk mendapatkan wawasan lebih mendalam dan mendukung strategi peningkatan aktivitas penyewaan sepeda.')


# Menampilkan kesimpulan dari analisis
st.header("Kesimpulan Keseluruhan")
st.write("Dari semua hasil analisis berikut adalah kesimpulan keseluruhan dari semua data tersebut")
st.text(''' 1.Pengaruh Cuaca Terhadap Aktivitas Penyewaan:

- Musim gugur menjadi puncak aktivitas penyewaan, kemungkinan dipengaruhi oleh cuaca yang nyaman dan lingkungan yang indah.
- Meskipun terjadi penurunan, musim panas tetap menjadi salah satu musim dengan tingkat penyewaan tertinggi.
- Musim dingin menunjukkan penurunan tajam, mungkin karena kondisi cuaca kurang mendukung dan preferensi untuk aktivitas indoor.
- Musim semi menunjukkan tingkat penyewaan yang moderat, tetapi lebih rendah dibandingkan musim gugur dan panas.''')

st.text('''2. Pola Aktivitas Penyewaan Harian:

- Pengguna casual cenderung menyewa sepeda pada sore hingga malam, menunjukkan preferensi untuk kegiatan rekreasi di luar jam kerja.
- Pengguna terdaftar menunjukkan pola yang berbeda, dengan aktivitas terpusat pada pagi hari dan sore hingga malam, mencerminkan penggunaan sepeda untuk komutasi atau pekerjaan.
- Jumlah penyewaan secara keseluruhan mencapai puncaknya pada sore hingga malam.''')

st.text('''
        3. Perbedaan Penggunaan Sepeda antara Hari Kerja dan Hari Libur:
- Jumlah penyewaan sepeda lebih tinggi pada hari kerja dibandingkan dengan hari libur.
- Hari kerja memiliki dampak positif terhadap penggunaan sepeda, kemungkinan terkait dengan kebutuhan komutasi dan aktivitas harian.''')

st.caption('Copyright © Cakra Satriyadana 2023')
