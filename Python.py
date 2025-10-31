import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

#gathring
st.title("ANALISIS DATA PENYEWAAN SEPEDA (Bike Sharing Dataset)")

url_day = "https://raw.githubusercontent.com/ibnuaditya-tech/Data-Analisis1/refs/heads/main/day.csv"
day_df = pd.read_csv(url_day)

url_hour = "https://raw.githubusercontent.com/ibnuaditya-tech/Data-Analisis1/main/hour.csv"
hour_df = pd.read_csv(url_hour)

st.write("Dataset harian (day.csv)")
st.dataframe(day_df.head())

st.write("Dataset per jam (hour.csv)")
st.dataframe(hour_df.head())

#assesing
day_df.info()
day_df.describe()
day_df.isna().sum()
day_df.duplicated().sum()
st.write(day_df.describe())

#cleaning
day_df.drop_duplicates(inplace=True)
hour_df.drop_duplicates(inplace=True)

day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

day_df['month'] = day_df['dteday'].dt.month
hour_df['month'] = hour_df['dteday'].dt.month

season_map = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
day_df['season'] = day_df['season'].map(season_map)
hour_df['season'] = hour_df['season'].map(season_map)

#EDA
season_avg = day_df.groupby('season')['cnt'].mean().reset_index()
st.write("Rata-rata jumlah penyewa berdasarkan season:")
st.dataframe(season_avg)

month_avg = day_df.groupby('month')['cnt'].mean().reset_index()
st.write("Rata-rata jumlah penyewa berdasarkan bulan:")
st.dataframe(month_avg)

#visualisasi
st.subheader("Perbandingan berdasarkan musim dan bulan")

fig1, ax1 = plt.subplots(figsize=(10, 6))
sns.barplot(data=season_avg, x='season', y='cnt', hue='season', palette='viridis', ax=ax1, legend=False)
ax1.set_title("Rata-rata Jumlah penyewa berdasarkan musim")
ax1.set_xlabel("Musim")
ax1.set_ylabel("Rata-rata penyewa")
st.pyplot(fig1)

fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.barplot(data=month_avg, x='month', y='cnt', hue='month', palette='coolwarm', ax=ax2, legend=False)
ax2.set_title("Rata-rata penyewa berdasarkan bulan")
ax2.set_xlabel("Bulan")
ax2.set_ylabel("Rata-rata penyewa")
st.pyplot(fig2)