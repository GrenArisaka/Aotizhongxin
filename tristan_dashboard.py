import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
# Datas
raw_data = pd.read_csv('PRSA_Data_Aotizhongxin_20130301-20170228.csv')



#Preparing data
# 1. nambahin kolom datetime
# 2. Renamed PM2.5 to PM25
cleaned_data = raw_data
cleaned_data['datetime'] = pd.to_datetime(raw_data[['year', 'month', 'day']])
cleaned_data = raw_data.rename(columns={'PM2.5': 'PM25'})

def cleanData(data):
    cwdf = data
    cwdf['month'] = cwdf['datetime'].dt.month
    average_bulanan_pm25 = cwdf.groupby('month')['PM25'].transform('mean')
    average_bulanan_pm10 = cwdf.groupby('month')['PM10'].transform('mean')
    cwdf['PM25'] = cwdf['PM25'].fillna(average_bulanan_pm25)
    cwdf['PM10'] = cwdf['PM10'].fillna(average_bulanan_pm10)
    return cwdf
cleaned_data = cleanData(cleaned_data)

pm25_harian = cleaned_data.groupby("datetime").PM25.mean().reset_index()
pm10_harian = cleaned_data.groupby("datetime").PM10.mean().reset_index()

pm25_tahunan = cleaned_data.groupby("year").PM25.mean().reset_index()
pm10_tahunan = cleaned_data.groupby("year").PM10.mean().reset_index()
#cleaned_data[['PM25','PM10']].corr() #Correlation between PM2.5 and PM10

#Fungsi untuk menentukan musim dingin bila diberi sebuah tanggal di musim dingin
def get_musim_dingin(date):
  month = date.month
  if month in [12]:
    return f"{date.year}-{date.year+1}"
  elif month in [1,2]:
    return f"{date.year-1}-{date.year}"
#Fungsi untuk membentuk data rata-rata PM2.5 di tiap musim dingin
def get_data_berdasarkan_musim_dingin():
    pm25_harian['Winter'] = pm25_harian['datetime'].apply(get_musim_dingin)
    winter_mean_pm25 = pm25_harian.groupby('Winter').PM25.mean().reset_index()
    return winter_mean_pm25
winter_mean_pm25 = get_data_berdasarkan_musim_dingin()


#Sedikit Glossary dari kode:
# 1. Cleaned Data -> Data yang sudah dibersihkan, data tentang kualitas udara tiap jam dari Maret 2013 - Februari 2017
# 2. pm25_harian, pm10_harian -> Masing masing rata-rata harian dari nilai berturut-turut PM2.5 dan PM10 harian dari cleaned_data
# 3. pm25_tahunan, pm10_tahunan -> Masing masing rata-rata tahunan dari nilai berturut-turut PM2.5 dan PM10 harian dari cleaned_data
# 4. winter_mean_pm25 -> Data rata-rata PM2.5 setiap musim dingin, yaitu 2013-2014, 2014-2015, 2015-2016, 2016-2017

#Bagian Awal
st.header("Dashboard Analisa Air Quality Data di Stasiun Aotizhongxin")
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/Olympic_Sports_Center_Station_Platform_201308.jpeg/1200px-Olympic_Sports_Center_Station_Platform_201308.jpeg")
#Bagian Penelusuran, Pengecekan dan Pembersihan data.


min_date = cleaned_data['datetime'].min()
max_date = cleaned_data['datetime'].max()

st.subheader("Melihat data PM2.5 dan PM10")
st.write("Analisa ini menelaah dua kolom, yaitu PM2.5 dan PM10.")

col1a, col2a, col3a= st.columns(3)

with col1a:
    st.metric("Jumlah Hari", 1460)
with col2a:
    pm25_harian['status'] = pm25_harian.PM25.apply(lambda x: "Dibawah batas WHO" if x <= 15 else "Diatas batas WHO")
    st.metric("% Hari PM2.5 diatas batas WHO", round(pm25_harian.groupby(by='status').count().loc['Diatas batas WHO']['PM25'] / 1460 * 100))
with col3a:
    pm10_harian['status'] = pm10_harian.PM10.apply(lambda x: "Dibawah batas WHO" if x <= 45 else "Diatas batas WHO")
    st.metric("% Hari PM10 diatas batas WHO", round(pm10_harian.groupby(by='status').count().loc['Diatas batas WHO']['PM10'] / 1460 * 100))

tab1, tab2, tab3 = st.tabs(["Display Data", "Informasi Data", "Analisa"])

with tab1:
    tab1.header("Display Data")
    st.caption("Menunjukkan data diantara dua tanggal tertentu.")
    haveValidInput=False
    try:
        start_date, end_date = st.date_input(
            label='Lihat data dari rentang waktu',min_value=min_date,
            max_value=max_date,
            value=[min_date, max_date]
        )
        haveValidInput=True
    except:
        st.write("Masukkan jangka tanggal")


    if haveValidInput:
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        pm25_kalender = pm25_harian[(pm25_harian['datetime'] >= start_date) & (pm25_harian['datetime'] <= end_date)]
        pm10_kalender = pm10_harian[(pm25_harian['datetime'] >= start_date) & (pm10_harian['datetime'] <= end_date)]

        fig, ax  = plt.subplots(nrows=1, ncols=2,figsize=(10,5))

        ax[0].plot(pm25_kalender.datetime, pm25_kalender.PM25)
        ax[0].set_xlabel('Tanggal')
        ax[0].set_xticklabels(pm25_harian['datetime'].dt.strftime('%Y-%m-%d'),rotation=45)
        ax[0].set_ylabel('PM2.5 Level, µg/m3')
        ax[0].axhline(y=15, color='r', linestyle='-', label='WHO PM2.5 Limit ')
        ax[0].grid(True)
        ax[0].legend()
        ax[1].plot(pm10_kalender.datetime, pm10_kalender.PM10)
        ax[1].set_xlabel('Tanggal')
        ax[1].set_xticklabels(pm10_harian['datetime'].dt.strftime('%Y-%m-%d'),rotation=45)
        ax[1].set_ylabel('PM10 Level, µg/m3')
        ax[1].axhline(y=45, color='r', linestyle='-', label='WHO PM10 Limit')
        ax[1].grid(True)
        ax[1].legend()
        st.pyplot(fig)
        col1b, col2b, col3b= st.columns(3)

        timeDelta = (end_date-start_date).days
        with col1b:
            st.metric("Jumlah Hari", timeDelta)
        with col2b:
            pm25_kalender['status'] = pm25_kalender.PM25.apply(lambda x: "Dibawah batas WHO" if x <= 15 else "Diatas batas WHO")
            formattedPercent = f"{pm25_kalender.groupby(by='status').count().loc['Diatas batas WHO']['PM25'] / timeDelta * 100:.2f}"
            st.metric("% Hari PM2.5 diatas batas WHO", formattedPercent)
        with col3b:
            pm10_kalender['status'] = pm10_kalender.PM10.apply(lambda x: "Dibawah batas WHO" if x <= 45 else "Diatas batas WHO")
            formattedPercent = f"{pm10_kalender.groupby(by='status').count().loc['Diatas batas WHO']['PM10'] / timeDelta * 100:.2f}"
            st.metric("% Hari PM10 diatas batas WHO", formattedPercent)

    st.subheader("Grafik rata-rata PM2.5 untuk tiap musim dingin 2013-2017")


    fig3, ax3 = plt.subplots(figsize=(7,5))
    ax3.plot(winter_mean_pm25.Winter, winter_mean_pm25.PM25)
    ax3.set_xlabel('Tanggal (Desember-Februari)')
    ax3.set_xticklabels(winter_mean_pm25.Winter,rotation=45)
    ax3.set_ylabel('PM2.5 Level, µg/m3')
    ax3.set_title('Level PM2.5 setiap musim dingin 2013-2017')
    ax3.axhline(y=45, color='r', linestyle='-', label='WHO PM10 Limit')
    ax3.grid(True)
    st.pyplot(fig3)

with tab2:
    tab2.header("Informasi Data")
    st.subheader("Informasi Selengkapnya tentang Dataset")
    st.write("Dataset adalah PRSA_Data_Aotizhongxin_20130301-20170228.csv")
    st.write("Berikut lima baris data pertama dari dataset tersebut.")
    st.write(cleaned_data.head())

    st.write("Informasi setiap kolom data:")
    st.markdown("""
    - Tahun, Bulan, Hari, dan Jam
    - PM2.5 dan PM10 (Pada kasus ini diubah nama kolom PM2.5 menjadi PM25 untuk kemudahan kode) yaitu *Particulate matter* berturut turut berukuran kurang dari 2.5 micron dan kurang dari 10 micron. Satuan yang digunakan adalah microgram per meter kubik (µg/m3)
    - SO2, NO2, CO, O3, adalah ukuran bahan kimia sesuai namanya, dengan satuan mikrogram per meter kubik (µg/m3)
    - PRES adalah singkatan untuk *Pressure* atau tekanan, diukur dalam hPA
    - DEWP adalah temperatur Dewpoint. Diukur dalam Celcius
    - RAIN adalah nilai presipitasi, diukur dalam mm
    - wd adalah arah angin, dipilih dari 16 arah sebagai nilai string unik
    - WSPM adalah kecepatan angin dalam m/s 
    - (Tambahan) datetime, yaitu tahun, bulan dan hari dalam satu kolom.
    """)
with tab3:
    st.subheader("Pertanyaan Bisnis untuk Analisa")
    st.markdown(""
                "- Pertanyaan 1 : Apakah ukuran *Particulate Matter* PM2.5 dan PM10 di stasiun Aoti Zhongxin dari musim semi tahun 2013 sampai akhir musim dingin 2017 sesuai dengan standar WHO, yaitu untuk PM2.5 rata-rata tahunan dibawah 5 µg/m3, rata-rata harian dibawah 15µg/m3 sedangkan untuk PM10 rata-rata tahunan dibawah 15µg/m3, rata-rata harian dibawah 45µg/m3?"
                "")
    st.markdown("- Pertanyaan 2 : Walau daerah perkotaan Beijing sudah menggunakan pemanasan distrik untuk musim dingin, daerah-daerah disekitar Beijing masih menggunakan pembakaran batu bara sebagai sumber panas. Pembakaran batu bara diketahui sebagai sumber polutan yang dapat meningkatkan kadar PM2.5. Bagaimana tren rata-rata PM2.5 pada musim dingin dari tahun 2013-2017? (Musim dingin di Beijing yaitu Bulan Desember-Februari)")
    st.subheader("Hasil Analisa")
    st.markdown("""- Kesimpulan pertanyaan 1 adalah bahwa ukuran PM2.5 maupun PM10 berada diatas batas aman WHO tahunan maupun sebagian besar harian. Angka rata-rata PM2.5 dan PM10 tahunan paling tinggi pada tahun 2014 dengan angka berturut-turut 92.5µg/m3 dan 123.5µg/m3, sedangkan batas aman WHO untuk PM2.5 dan PM10 berturut turut adalah 5µg/m3 dan 15µg/m3. Seperti yang ditemukan pada tahap EDA, ternyata ditemukan hanya 120 hari dari 1460 hari dalam dataset dimana PM2.5 memiliki nilai aman, dan hanya 288 hari dibawah batas untuk PM10. Rekor harian PM2.5 tertinggi adalah 512µg/m3 dan PM10 adalah 545µg/m3.
- Kesimpulan pertanyaan 2 adalah bahwa rata-rata ukuran PM2.5 setiap musim dingin turun dari musim dingin 2013-2014 ke 2014-2015, stagnan, kemudian naik dari 2015-2016 ke 2016-2017. """)
