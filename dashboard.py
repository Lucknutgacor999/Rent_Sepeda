import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("data_clean.csv")

# Sidebar
st.sidebar.title("Bicycle Rent")
st.sidebar.image("logo.jpg", width=300)

# Title
st.title("📊 Dashboard Penyewaan Sepeda")
st.markdown("---")

# Menampilkan Total Penyewa
total_casual = df['casual'].sum()
total_registered = df['registered'].sum()
total_rentals = df['total_rentals'].sum()

st.subheader("📌 Total Penyewa")
col1, col2, col3 = st.columns(3)
col1.metric("Casual", f"{total_casual:,}")
col2.metric("Registered", f"{total_registered:,}")
col3.metric("Total", f"{total_rentals:,}")
st.markdown("---")

# Menampilkan Total Penyewa Berdasarkan Tahun
st.subheader("📆 Total Penyewa Berdasarkan Tahun")
total_kasual_pertahun = df.groupby("year")["casual"].sum().reset_index()
total_terdaftar_pertahun = df.groupby("year")["registered"].sum().reset_index()

fig_casual_year = px.bar(total_kasual_pertahun, x="year", y="casual", title="Total Penyewa Casual per Tahun", text_auto=True, color_discrete_sequence=["#19D3F3"], labels={"year": "Tahun", "casual": "Total Penyewa Casual"})
fig_registered_year = px.bar(total_terdaftar_pertahun, x="year", y="registered", title="Total Penyewa Registered per Tahun", text_auto=True, color_discrete_sequence=["#FF6692"], labels={"year": "Tahun", "registered": "Total Penyewa Registered"})

fig_casual_year.update_xaxes(type='category')
fig_registered_year.update_xaxes(type='category')
fig_casual_year.update_layout(template="plotly_white", xaxis_title=None, yaxis_title=None)
fig_registered_year.update_layout(template="plotly_white", xaxis_title=None, yaxis_title=None)

st.plotly_chart(fig_casual_year, use_container_width=True)
st.plotly_chart(fig_registered_year, use_container_width=True)

# Menampilkan Total Penyewa Berdasarkan Bulan
st.subheader("📅 Total Penyewa Berdasarkan Bulan")
order = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
df["month"] = pd.Categorical(df["month"], categories=order, ordered=True)

total_perbulan = df.groupby("month")["total_rentals"].sum().reset_index()
fig_month = px.bar(total_perbulan, x="month", y="total_rentals", title="Total Penyewa per Bulan", text_auto=True, color_discrete_sequence=["#636EFA"])

st.plotly_chart(fig_month, use_container_width=True)
st.markdown("---")

# Menampilkan Total Penyewa Berdasarkan Musim
st.subheader("🌦️ Total Penyewa Berdasarkan Musim")
season_rentals = df.groupby("season")["total_rentals"].sum().reset_index()
fig_season = px.bar(season_rentals, x='season', y='total_rentals', title="Total Penyewa per Musim", text_auto=True, color_discrete_sequence=["#636EFA"], labels={"season": "Musim", "total_rentals": "Total Penyewa"})
fig_season.update_layout(template="plotly_white", xaxis_title=None, yaxis_title=None)
st.plotly_chart(fig_season, use_container_width=True)
st.markdown("---")

