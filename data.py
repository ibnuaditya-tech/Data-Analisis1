import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Judul Aplikasi
st.title("📈 Analisis Data Penyewaan Sepeda (Bike Sharing Dataset)")

# --- GATHERING DATA ---
st.header("1️⃣ Gathering Data")
url_day = "https://raw.githubusercontent.com/ibnuaditya-tech/Data-Analisis1/refs/heads/main/day.csv"
url_hour = "https://raw.githubusercontent.com/ibnuaditya-tech/Data-Analisis1/main/hour.csv"

day_df = pd.read_csv(url_day)
hour_df = pd.read_csv(url_hour)

st.write("**Dataset Harian (day.csv)**")
st.dataframe(day_df.head())

st.write("**Dataset Per Jam (hour.csv)**")
st.dataframe(hour_df.head())

# --- CLEANING DATA ---
st.header("2️⃣ Cleaning Data")
day_df.drop_duplicates(inplace=True)
hour_df.drop_duplicates(inplace=True)

# Konversi dteday ke datetime
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# Tambah kolom month
day_df['month'] = day_df['dteday'].dt.month
hour_df['month'] = hour_df['dteday'].dt.month

# Ubah season ke nama musim
season_map = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
day_df['season'] = day_df['season'].map(season_map)
hour_df['season'] = hour_df['season'].map(season_map)

st.success("Data berhasil dibersihkan dan dikonversi ✅")

# --- EDA (Exploratory Data Analysis) ---
st.header("3️⃣ Exploratory Data Analysis")

# Statistik deskriptif
st.subheader("📊 Statistik Deskriptif")
st.write(day_df.describe())

# Rata-rata berdasarkan season
season_avg = day_df.groupby('season')['cnt'].mean().reset_index()
st.write("**Rata-rata jumlah penyewa berdasarkan season:**")
st.dataframe(season_avg)

# Rata-rata berdasarkan bulan
month_avg = day_df.groupby('month')['cnt'].mean().reset_index()
st.write("**Rata-rata jumlah penyewa berdasarkan bulan:**")
st.dataframe(month_avg)

# Matriks korelasi
numeric_cols = ['temp', 'atemp', 'hum', 'windspeed', 'casual', 'registered', 'cnt']
corr_matrix = day_df[numeric_cols].corr()
st.write("**Matriks Korelasi Fitur Numerik:**")
st.dataframe(corr_matrix)

# --- VISUALISASI ---
st.header("4️⃣ Visualisasi Data")

visualization_option = st.radio(
    "Pilih Jenis Visualisasi:",
    (
        "Perbandingan Berdasarkan Season",
        "Perbandingan Berdasarkan Bulan",
        "Tren Penyewaan Harian Sepanjang Tahun"
    )
)

if visualization_option == "Perbandingan Berdasarkan Season":
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=season_avg, x='season', y='cnt', hue='season', palette='viridis', ax=ax, legend=False)
    ax.set_title("Rata-rata Jumlah Penyewa Berdasarkan Season")
    ax.set_xlabel("Season")
    ax.set_ylabel("Rata-rata Penyewa (cnt)")
    st.pyplot(fig)

elif visualization_option == "Perbandingan Berdasarkan Bulan":
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=month_avg, x='month', y='cnt', hue='month', palette='coolwarm', ax=ax, legend=False)
    ax.set_title("Rata-rata Jumlah Penyewa Berdasarkan Bulan")
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Rata-rata Penyewa (cnt)")
    st.pyplot(fig)

elif visualization_option == "Tren Penyewaan Harian Sepanjang Tahun":
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=day_df, x='dteday', y='cnt', ax=ax, color='orange')
    ax.set_title("Tren Penyewaan Sepeda Harian Sepanjang Tahun")
    ax.set_xlabel("Tanggal")
    ax.set_ylabel("Jumlah Penyewa (cnt)")
    st.pyplot(fig)
