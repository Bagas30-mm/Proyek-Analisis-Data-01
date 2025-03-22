import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt



day = pd.read_csv('./Dashboard/day.csv')
hour = pd.read_csv('./Dashboard/hour.csv') 


df = day.merge(hour, on='dteday', how='inner', suffixes=('_daily', '_hourly'))


# Streamlit UI
st.title("Dashboard of Analyzing Bike Sharing Culture")
st.write("Bagas Rizky Ramadhan")


# Fitur interaktif: Filter berdasarkan tanggal
st.sidebar.header("Filter Data")
selected_dates = st.sidebar.date_input("Pilih Rentang Tanggal", [pd.to_datetime(df['dteday']).min(), pd.to_datetime(df['dteday']).max()], key='date_range')

if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
    start_date, end_date = selected_dates
    df = df[(pd.to_datetime(df['dteday']) >= pd.to_datetime(start_date)) & (pd.to_datetime(df['dteday']) <= pd.to_datetime(end_date))]

# Fitur interaktif tambahan: Filter berdasarkan musim dan hari kerja
selected_season = st.sidebar.multiselect("Pilih Musim", ['Spring', 'Summer', 'Fall', 'Winter'], ['Spring', 'Summer', 'Fall', 'Winter'])
selected_workingday = st.sidebar.radio("Pilih Jenis Hari", ['Semua', 'Hari Kerja', 'Hari Libur'])

# Filter data berdasarkan musim
if selected_season:
    season_map = {'Spring': 1, 'Summer': 2, 'Fall': 3, 'Winter': 4}
    selected_season_codes = [season_map[season] for season in selected_season]
    df = df[df['season_daily'].isin(selected_season_codes)]

# Filter data berdasarkan jenis hari
if selected_workingday == 'Hari Kerja':
    df = df[df['workingday_daily'] == 1]
elif selected_workingday == 'Hari Libur':
    df = df[df['workingday_daily'] == 0]

# Menampilkan pertanyaan bisnis
st.subheader("1. Bagaimana musim memengaruhi penyewaan sepeda oleh pengguna casual dan registered?")


st.subheader("Visualisasi Terpisah Pengguna Casual dan Registered.")
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
                    color='casual_daily', color_continuous_scale='reds',template='plotly_dark')

# Plot for Registered Users
fig_registered = px.bar(seasonal_data_registered, x='season_name', y='registered_daily',
                        title='Jumlah Rata-rata Sewa Harian (Registered Users)',
                        labels={'registered_daily': 'Rata-rata Jumlah Sewa Harian', 'season_name': 'Musim'},
                        color='registered_daily', color_continuous_scale='blues',template='plotly_dark')


# Display the plots
st.plotly_chart(fig_casual)
st.plotly_chart(fig_registered)


st.subheader("Visualisasi Terpisah Pengguna Casual dan Registered")
seasonal_data = df.groupby(['season_daily'])[['casual_daily', 'registered_daily']].mean().reset_index()
seasonal_data['season_name'] = ['Spring', 'Summer', 'Fall', 'Winter']
seasonal_data = seasonal_data.sort_values(by='casual_daily', ascending=False)

# Set up the Streamlit app
# Plot using Plotly Express
fig = px.bar(seasonal_data, x='season_name', y=['casual_daily', 'registered_daily'],
             title='Rata-rata Aktivitas Penyewaan Sepeda Berdasarkan Kedua Jenis Pengguna.',
             labels={'value': 'Rata-rata Jumlah Sewa Harian', 'variable': 'User Type', 'season_name': 'Musim'},
             color_discrete_sequence=['skyblue', 'salmon'],template='plotly_dark')

# Display the Plotly Express plot
st.plotly_chart(fig)

st.write("Pada musim gugur, pengguna casual mencatatkan tingkat penyewaan sepeda tertinggi, didukung oleh cuaca yang nyaman serta keindahan lingkungan. Pengguna terdaftar juga menunjukkan jumlah penyewaan yang signifikan pada musim ini. Meskipun terjadi sedikit penurunan pada musim panas dibandingkan dengan musim gugur, musim panas tetap menjadi periode dengan penyewaan tinggi untuk pengguna casual dan cukup tinggi untuk pengguna terdaftar. Selama musim dingin, penyewaan dari kedua kelompok menurun drastis, yang kemungkinan disebabkan oleh cuaca yang kurang mendukung dan kecenderungan untuk melakukan aktivitas indoor. Pada musim semi, tingkat penyewaan berada pada level yang moderat, lebih rendah dibandingkan dengan musim gugur dan musim panas untuk kedua kelompok. Dibandingkan antara kedua kelompok, pengguna casual cenderung lebih aktif menyewa pada musim gugur, sementara pengguna terdaftar mencapai puncak penyewaan mereka pada musim panas. Kedua kelompok mengalami penurunan serupa selama musim dingin, dengan pola penyewaan yang relatif mirip terlihat pada musim semi.")




st.subheader("2. Seperti apa perubahan pola aktivitas penyewaan sepeda sepanjang hari?")


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


st.write('Aktivitas harian penyewaan sepeda oleh pengguna casual mencapai puncaknya pada sore hingga malam hari, terutama sekitar pukul 17.00 hingga 18.00. Pola ini menunjukkan bahwa pengguna casual lebih sering memanfaatkan sepeda untuk kegiatan rekreasi atau aktivitas non-rutin pada waktu tersebut. Di sisi lain, pengguna terdaftar (registered users) memiliki pola yang berbeda, dengan puncak penyewaan terjadi pada dua periode, yaitu pagi sekitar pukul 8.00 dan sore hingga malam sekitar pukul 17.00 hingga 18.00. Hal ini mengindikasikan bahwa pengguna terdaftar lebih sering menggunakan sepeda untuk kebutuhan harian atau perjalanan kerja pada pagi dan sore hari. Secara keseluruhan, jumlah total penyewaan sepeda (count) mencapai puncaknya pada sore hingga malam, yang mencerminkan kombinasi dari pola kedua kelompok. Waktu-waktu tersebut menunjukkan tingginya popularitas penyewaan sepeda secara umum.')
     

st.subheader("3. Berapa besar selisih penggunaan sepeda antara hari kerja dan hari libur?")

# Plotly Express bar chart
fig = px.bar(df, x="workingday_daily", y="cnt_daily", color="workingday_daily",
             labels={'workingday_daily': 'Hari'},
             title='Perbedaan Penggunaan Sepeda Harian Antara Hari Kerja dan Hari Libur.',
             category_orders={'workingday_daily': [0, 1]},
             color_discrete_map={0: 'skyblue', 1: 'salmon'})

# Menambahkan label pada sumbu x
fig.update_xaxes(ticktext=["Hari Libur", "Hari Kerja"], tickvals=[0, 1])


# Streamlit app
st.plotly_chart(fig)


st.write('Analisis perbandingan aktivitas penyewaan sepeda menunjukkan bahwa jumlah penyewaan lebih tinggi pada hari kerja dibandingkan hari libur. Grafik menggambarkan dampak positif hari kerja terhadap frekuensi penyewaan, dengan jumlah sewa harian yang lebih dominan. Untuk mengoptimalkan penyewaan, disarankan menyesuaikan penawaran pada hari kerja, seperti memberikan diskon di jam sibuk. Selain itu, pengembangan program khusus di hari libur, misalnya tur rekreasi atau paket promosi, dapat meningkatkan minat pelanggan. Penelitian lebih lanjut terkait faktor penyebab perbedaan penyewaan antara hari kerja dan hari libur direkomendasikan untuk mendapatkan wawasan yang lebih mendalam guna mendukung strategi peningkatan penyewaan sepeda.')


# Menampilkan kesimpulan dari analisis
st.header("Kesimpulan")
st.write("Dari semua hasil analisis berikut adalah kesimpulan keseluruhan dari semua data tersebut")
st.text('''1.Pengaruh Cuaca Terhadap Aktivitas Penyewaan:

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
