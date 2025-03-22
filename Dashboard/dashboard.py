import streamlit as st
import pandas as pd
import plotly.express as px

# Load Data
@st.cache_data
def load_data():
    day = pd.read_csv('./Dashboard/day.csv')
    hour = pd.read_csv('./Dashboard/hour.csv')
    df = day.merge(hour, on='dteday', how='inner', suffixes=('_daily', '_hourly'))
    return df

df = load_data()

# Data Processing
season_map = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
df['season_name'] = df['season_daily'].map(season_map)
df['workingday_label'] = df['workingday_daily'].apply(lambda x: 'Hari Kerja' if x == 1 else 'Hari Libur')

# Sidebar Filters
st.sidebar.title("ClearPath")
selected_season = st.sidebar.selectbox("Pilih Musim:", ['All'] + list(season_map.values()))
selected_workingday = st.sidebar.radio("Pilih Hari:", ['All', 'Hari Kerja', 'Hari Libur'])

# Apply Filters
filtered_df = df.copy()
if selected_season != 'All':
    filtered_df = filtered_df[filtered_df['season_name'] == selected_season]
if selected_workingday != 'All':
    filtered_df = filtered_df[filtered_df['workingday_label'] == selected_workingday]

# Title
st.title("Dashboard of Analyzing Bike Sharing Culture")
st.write("Bagas Rizky Ramadhan")

# Function to plot bar charts
def plot_bar_chart(data, x, y, color, title, labels, color_scale=None, color_map=None, category_orders=None):
    if color_scale:
        fig = px.bar(data, x=x, y=y, color=color, title=title, labels=labels, color_continuous_scale=color_scale, template='plotly_dark')
    elif color_map:
        fig = px.bar(data, x=x, y=y, color=color, title=title, labels=labels, color_discrete_map=color_map, category_orders=category_orders, template='plotly_dark')
    else:
        fig = px.bar(data, x=x, y=y, color=color, title=title, labels=labels, template='plotly_dark')
    st.plotly_chart(fig)

# Visualization 1: Seasonal Analysis
st.subheader("1. Bagaimana musim memengaruhi penyewaan sepeda oleh pengguna casual dan registered?")
seasonal_data = filtered_df.groupby(['season_name'])[['casual_daily', 'registered_daily']].mean().reset_index()
plot_bar_chart(seasonal_data, 'season_name', 'casual_daily', 'casual_daily', 'Jumlah Rata-rata Sewa Harian (Casual Users)', {'casual_daily': 'Rata-rata Jumlah Sewa Harian', 'season_name': 'Musim'}, 'reds')
plot_bar_chart(seasonal_data, 'season_name', 'registered_daily', 'registered_daily', 'Jumlah Rata-rata Sewa Harian (Registered Users)', {'registered_daily': 'Rata-rata Jumlah Sewa Harian', 'season_name': 'Musim'}, 'blues')

st.write("Pada musim gugur, pengguna casual mencatatkan tingkat penyewaan sepeda tertinggi, didukung oleh cuaca yang nyaman serta keindahan lingkungan. Pengguna terdaftar juga menunjukkan jumlah penyewaan yang signifikan pada musim ini. Meskipun terjadi sedikit penurunan pada musim panas dibandingkan dengan musim gugur, musim panas tetap menjadi periode dengan penyewaan tinggi untuk pengguna casual dan cukup tinggi untuk pengguna terdaftar. Selama musim dingin, penyewaan dari kedua kelompok menurun drastis, yang kemungkinan disebabkan oleh cuaca yang kurang mendukung dan kecenderungan untuk melakukan aktivitas indoor. Pada musim semi, tingkat penyewaan berada pada level yang moderat, lebih rendah dibandingkan dengan musim gugur dan musim panas untuk kedua kelompok. Dibandingkan antara kedua kelompok, pengguna casual cenderung lebih aktif menyewa pada musim gugur, sementara pengguna terdaftar mencapai puncak penyewaan mereka pada musim panas. Kedua kelompok mengalami penurunan serupa selama musim dingin, dengan pola penyewaan yang relatif mirip terlihat pada musim semi.")

# Visualization 2: Hourly Activity
st.subheader("2. Seperti apa perubahan pola aktivitas penyewaan sepeda sepanjang hari?")
for user_type in ['casual_hourly', 'registered_hourly', 'cnt_hourly']:
    hourly_counts = filtered_df.groupby('hr')[user_type].mean().reset_index()
    color_scale = {'casual_hourly': 'Magenta', 'registered_hourly': 'Teal', 'cnt_hourly': 'Burg'}
    plot_bar_chart(hourly_counts, 'hr', user_type, user_type, f'Distribusi Penyewaan Sepeda berdasarkan Jam dalam Sehari ({user_type.replace("_hourly", "").title()} Users)', {'hr': 'Waktu Penyewaan', user_type: 'Jumlah Penyewaan'}, color_scale[user_type])

st.write('Aktivitas harian penyewaan sepeda oleh pengguna casual mencapai puncaknya pada sore hingga malam hari, terutama sekitar pukul 17.00 hingga 18.00. Pola ini menunjukkan bahwa pengguna casual lebih sering memanfaatkan sepeda untuk kegiatan rekreasi atau aktivitas non-rutin pada waktu tersebut. Di sisi lain, pengguna terdaftar (registered users) memiliki pola yang berbeda, dengan puncak penyewaan terjadi pada dua periode, yaitu pagi sekitar pukul 8.00 dan sore hingga malam sekitar pukul 17.00 hingga 18.00. Hal ini mengindikasikan bahwa pengguna terdaftar lebih sering menggunakan sepeda untuk kebutuhan harian atau perjalanan kerja pada pagi dan sore hari. Secara keseluruhan, jumlah total penyewaan sepeda (count) mencapai puncaknya pada sore hingga malam, yang mencerminkan kombinasi dari pola kedua kelompok. Waktu-waktu tersebut menunjukkan tingginya popularitas penyewaan sepeda secara umum.')


# Visualization 3: Working Day vs Holiday (Perbaikan Warna)
st.subheader("3. Berapa besar selisih penggunaan sepeda antara hari kerja dan hari libur?")

# Plot dengan color_discrete_map yang benar
plot_bar_chart(filtered_df, 'workingday_label', 'cnt_daily', 'workingday_label', 'Perbedaan Penggunaan Sepeda Harian Antara Hari Kerja dan Hari Libur', {'workingday_label': 'Hari', 'cnt_daily': 'Jumlah Penyewaan'}, color_map={'Hari Kerja': 'salmon', 'Hari Libur': 'skyblue'}, category_orders={'workingday_label': ['Hari Libur', 'Hari Kerja']})



# Agregasi Data untuk Menyamakan Frekuensi dengan Gambar
workingday_counts = filtered_df.groupby('workingday_label')['cnt_daily'].mean().reset_index()

# Plot dengan Tema Terang dan Warna Sesuai
plot_bar_chart(
    workingday_counts,
    x='workingday_label',
    y='cnt_daily',
    color='workingday_label',
    color_discrete_map={'Hari Kerja': 'salmon', 'Hari Libur': 'skyblue'},
    labels={'workingday_label': 'Hari', 'cnt_daily': 'Jumlah Sewa Sepeda Harian'},
    title='Perbandingan Penggunaan Sepeda per hari antara Hari Kerja dan Hari Libur',
    category_orders={'workingday_label': ['Hari Libur', 'Hari Kerja']}
)



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
