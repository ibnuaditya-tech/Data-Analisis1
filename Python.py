# ===============================================
# 📊 Analisis Data Penyewaan Sepeda - Streamlit
# ===============================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Konfigurasi halaman
st.set_page_config(page_title="Analisis Penyewaan Sepeda", layout="wide")
st.title("🚲 Analisis Data Penyewaan Sepeda (Bike Sharing Dataset)")

# =========================
# 1. Load Dataset
# =========================
url_day = "https://raw.githubusercontent.com/ibnuaditya-tech/Data-Analisis1/refs/heads/main/day.csv"
url_hour = "https://raw.githubusercontent.com/ibnuaditya-tech/Data-Analisis1/main/hour.csv"

day_df = pd.read_csv(url_day)
hour_df = pd.read_csv(url_hour)

# =========================
# 2. Preprocessing
# =========================
day_df.drop_duplicates(inplace=True)
hour_df.drop_duplicates(inplace=True)

day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

day_df['month'] = day_df['dteday'].dt.month
hour_df['month'] = hour_df['dteday'].dt.month

# Mapping musim
season_map = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
day_df['season'] = day_df['season'].map(season_map)
hour_df['season'] = hour_df['season'].map(season_map)

# =========================
# 3. Sidebar Filter
# =========================
st.sidebar.header("🔍 Filter Data")

# Pilihan musim
selected_season = st.sidebar.selectbox(
    "Pilih musim:",
    options=['All'] + sorted(day_df['season'].unique().tolist())
)

# Pilihan bulan
selected_month = st.sidebar.selectbox(
    "Pilih bulan:",
    options=['All'] + sorted(day_df['month'].unique().tolist())
)

# Pilihan jam
selected_hour = st.sidebar.selectbox(
    "Pilih jam:",
    options=['All'] + sorted(hour_df['hr'].unique().tolist())
)

# =========================
# 4. Filter Data
# =========================
filtered_day = day_df.copy()
filtered_hour = hour_df.copy()

if selected_season != 'All':
    filtered_day = filtered_day[filtered_day['season'] == selected_season]
    filtered_hour = filtered_hour[filtered_hour['season'] == selected_season]

if selected_month != 'All':
    filtered_day = filtered_day[filtered_day['month'] == int(selected_month)]
    filtered_hour = filtered_hour[filtered_hour['month'] == int(selected_month)]

if selected_hour != 'All':
    filtered_hour = filtered_hour[filtered_hour['hr'] == int(selected_hour)]

# =========================
# 5. Analisis dan Visualisasi
# =========================

# --- Rata-rata per musim ---
season_avg = filtered_day.groupby('season')['cnt'].mean().reset_index()

# --- Rata-rata per bulan ---
month_avg = filtered_day.groupby('month')['cnt'].mean().reset_index()

# --- Rata-rata per jam ---
hour_avg = filtered_hour.groupby('hr')['cnt'].mean().reset_index()

# =========================
# 6. Tampilkan Data
# =========================
st.subheader("📅 Statistik Dataset Harian")
st.write(filtered_day.describe())

# =========================
# 7. Visualisasi
# =========================

sns.set(style="whitegrid")

# Grafik per musim
st.subheader("🌤️ Rata-rata Penyewa Berdasarkan Musim")
fig1, ax1 = plt.subplots(figsize=(8, 4))
sns.barplot(data=season_avg, x='season', y='cnt', palette='viridis', ax=ax1)
ax1.set_title("Rata-rata jumlah penyewa berdasarkan musim", fontsize=14)
ax1.set_xlabel("Musim")
ax1.set_ylabel("Rata-rata penyewa")
st.pyplot(fig1)

# Grafik per bulan
st.subheader("🗓️ Rata-rata Penyewa Berdasarkan Bulan")
fig2, ax2 = plt.subplots(figsize=(8, 4))
sns.barplot(data=month_avg, x='month', y='cnt', palette='coolwarm', ax=ax2)
ax2.set_title("Rata-rata jumlah penyewa berdasarkan bulan", fontsize=14)
ax2.set_xlabel("Bulan")
ax2.set_ylabel("Rata-rata penyewa")
st.pyplot(fig2)

# Grafik per jam
st.subheader("⏰ Rata-rata Penyewa Berdasarkan Jam")
fig3, ax3 = plt.subplots(figsize=(8, 4))
sns.lineplot(data=hour_avg, x='hr', y='cnt', marker='o', ax=ax3)
ax3.set_title("Rata-rata jumlah penyewa berdasarkan jam", fontsize=14)
ax3.set_xlabel("Jam")
ax3.set_ylabel("Rata-rata penyewa")
st.pyplot(fig3)

# =========================
# 8. Kesimpulan
# =========================

