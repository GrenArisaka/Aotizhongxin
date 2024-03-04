
# Analisa Air Quality Stasiun Aoti Zhongxin ✨

## Setup environment
```
conda create --name main-ds python=3.9
conda activate main-ds
pip install pandas matplotlib streamlit numpy
```

## Run steamlit app
```
streamlit run tristan_dashboard.py
```
## Informasi Dataset
Dataset bernama PRSA_Data_Aotizhongxin_20130301-20170228.csv
Agar dapat menjalankan file Notebook, pastikan path ke dataset disesuaikan pada sel kode bagian *Data Gathering* pada notebook tersebut. Terdapat komen yang menjelaskan lebih detail.
## Penggunaan Dashboard
Terdapat tiga tab. Tab pertama berfungsi untuk mendisplay visualisasi data. Masukkan rentang tanggal ke dalam kolom rentang tanggal, lalu pyplot akan menunjukkan data sesuai dengan tanggal tersebut, serta menghitung jumlah hari dan berapa % hari tersebut memiliki nilai diatas batas aman WHO. Selain itu, ada pun data rata-rata PM2.5 maupun PM10 untuk setiap musim dingin 2013-2017. Tab kedua berisi informasi umum mengenai dataset. Tab ketiga berisi pertanyaan dan kesimpulan dari analisa data.
Link ke Streamlite cloud: 
