import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
data = pd.read_csv("main_data.csv")

# Convert date column to datetime
data["dteday"] = pd.to_datetime(data["dteday"])

# Extract weekday names
data["weekday"] = data["dteday"].dt.day_name()

# Sidebar filters
st.sidebar.image("logo.jpg", width=250)
st.sidebar.title("Bike Rental Analysis")
st.sidebar.header("🔍 Filter Data")
st.sidebar.markdown("Gunakan filter ini untuk menyesuaikan tampilan data.")
selected_year = st.sidebar.selectbox("📅 Pilih Tahun:", sorted(data["year"].unique()))
selected_season = st.sidebar.selectbox("🌦 Pilih Musim:", data["season"].unique())
selected_weather = st.sidebar.selectbox("☁ Pilih Cuaca:", data["weathersit"].unique())

data_filtered = data[(data["year"] == selected_year) & (data["season"] == selected_season) & (data["weathersit"] == selected_weather)]

# Dashboard title
st.markdown("# 🚲 Dashboard Penyewaan Sepeda")
st.markdown("**Analisis tren penyewaan sepeda berdasarkan berbagai faktor.**")
# Total Users Metrics
st.subheader("📊 Total Penyewaan Sepeda")

# Hitung total casual dan registered users
total_casual = data["casual"].sum()
total_registered = data["registered"].sum()
total_users = total_casual + total_registered

# Tampilkan dalam 3 kolom
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("👤 Total Casual Renters", value=f'{total_casual:,}', delta_color="inverse")

with col2:
    st.metric("🧑‍💼 Total Registered Renters", value=f'{total_registered:,}', delta_color="inverse")

with col3:
    st.metric("🚴‍♂️ Total Renters", value=f'{total_users:,}', delta_color="inverse")


# Warna seragam untuk semua chart
color_palette = "#1f77b4"

# Chart total penyewa per hari (Filtered)
st.subheader("📆 Total Penyewa per Hari")
data_daily = data_filtered.groupby("weekday")["total_rentals"].sum().reset_index()
ordered_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
data_daily["weekday"] = pd.Categorical(data_daily["weekday"], categories=ordered_days, ordered=True)
data_daily = data_daily.sort_values("weekday")
fig2 = px.bar(data_daily, x="weekday", y="total_rentals", title="Total Penyewa per Hari", template="seaborn", color_discrete_sequence=[color_palette])
st.plotly_chart(fig2, use_container_width=True)

# Chart penyewa per bulan (Tidak bisa difilter)
st.subheader("📅 Penyewa per Bulan")
data["month"] = data["dteday"].dt.month  # Pastikan 'month' berasal dari tanggal
month_names = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
data_monthly = data.groupby("month")["total_rentals"].sum().reindex(range(1, 13), fill_value=0).reset_index()
data_monthly["month"] = data_monthly["month"].apply(lambda x: month_names[x-1])  # Konversi angka ke nama bulan
fig1 = px.bar(data_monthly, x="month", y="total_rentals", title="Total Penyewa per Bulan", template="seaborn", color_discrete_sequence=[color_palette])
st.plotly_chart(fig1, use_container_width=True)

# Chart penyewa berdasarkan musim
st.subheader("🍂 Penyewa berdasarkan Musim")
fig3 = px.bar(data.groupby("season")["total_rentals"].sum().reset_index(), x="season", y="total_rentals", title="Total Penyewa Berdasarkan Musim", template="seaborn", color_discrete_sequence=[color_palette])
st.plotly_chart(fig3, use_container_width=True)

# Chart penyewa berdasarkan cuaca
st.subheader("🌤 Penyewa berdasarkan Cuaca")
fig4 = px.bar(data.groupby("weathersit")["total_rentals"].sum().reset_index(), x="weathersit", y="total_rentals", title="Total Penyewa Berdasarkan Cuaca", template="seaborn", color_discrete_sequence=[color_palette])
st.plotly_chart(fig4, use_container_width=True)

# Chart perbandingan penyewa casual dan registered per tahun
st.subheader("👥 Perbandingan Penyewa Casual dan Registered per Tahun")
data_grouped_year = data.groupby("year")[["casual", "registered"]].sum().reset_index()
data_grouped_year["year"] = data_grouped_year["year"].astype(str)  # Ensure year is categorical for proper display
fig5 = px.bar(data_grouped_year, x="year", y=["casual", "registered"], title="Perbandingan Penyewa per Tahun", barmode="group", template="seaborn", color_discrete_sequence=[color_palette, "#ff7f0e"])
st.plotly_chart(fig5, use_container_width=True)

# Chart bulan puncak penyewa registered dan casual
st.subheader("📈 Bulan Puncak Penyewa Registered dan Casual")
data_peak_month = data.groupby("month")[["casual", "registered"]].sum().reset_index()
data_peak_month["month"] = data_peak_month["month"].apply(lambda x: month_names[x-1])
fig6 = px.line(data_peak_month, x="month", y=["casual", "registered"], title="Tren Penyewa Registered dan Casual", markers=True, template="seaborn", color_discrete_sequence=[color_palette, "#ff7f0e"])
st.plotly_chart(fig6, use_container_width=True)

# Chart rata-rata penyewa casual dan registered setiap musim
st.subheader("📊 Rata-rata Penyewa Casual dan Registered Setiap Musim")
data_avg_season = data.groupby("season")[["casual", "registered"]].mean().reset_index()
fig7 = px.bar(data_avg_season, x="season", y=["casual", "registered"], title="Rata-rata Penyewa Berdasarkan Musim", barmode="group", template="seaborn", color_discrete_sequence=[color_palette, "#ff7f0e"])
st.plotly_chart(fig7, use_container_width=True)
