import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

# Konfigurasi halaman
st.set_page_config(page_title="Dashboard Penyewaan Sepeda", layout="wide")
st.markdown("<h1 style='text-align: center; color: #2E8B57;'>🚴 Dashboard Penyewaan Sepeda 🚴</h1>", unsafe_allow_html=True)

# Load dataset
data = pd.read_csv("data_clean.csv")
data["dteday"] = pd.to_datetime(data["dteday"])
data["year"] = data["dteday"].dt.year
data["month"] = data["dteday"].dt.month

# Sidebar
st.sidebar.image("logo.jpg", width=250)
st.sidebar.header("Filter Data")
selected_year = st.sidebar.selectbox("Pilih Tahun", options=sorted(data["year"].unique()))
data_filtered = data[data["year"] == selected_year]

# Pilihan Bulan
dict_bulan = {
    1: "Januari", 2: "Februari", 3: "Maret", 4: "April", 5: "Mei", 6: "Juni",
    7: "Juli", 8: "Agustus", 9: "September", 10: "Oktober", 11: "November", 12: "Desember"
}
selected_month = st.sidebar.selectbox("Pilih Bulan", options=[dict_bulan[m] for m in sorted(data_filtered["month"].unique())])
selected_month_num = {v: k for k, v in dict_bulan.items()}[selected_month]
data_filtered = data_filtered[data_filtered["month"] == selected_month_num]

# Visualisasi 1: Penyewaan per Hari
st.subheader("📅 Jumlah Penyewaan Sepeda per Hari")
fig = px.line(data_filtered, x="dteday", y="total_rentals", labels={"dteday": "Tanggal", "total_rentals": "Jumlah Penyewa"})
st.plotly_chart(fig, use_container_width=True)

# Visualisasi soal 1: Penyewaan per Bulan
st.subheader("📊 Jumlah Penyewa Sepeda per Bulan")
monthly_rentals = data.groupby("month")["total_rentals"].sum().reset_index()
monthly_rentals["Month"] = monthly_rentals["month"].map(dict_bulan)
fig = px.bar(monthly_rentals, x="Month", y="total_rentals", labels={"total_rentals": "Jumlah Penyewa"}, color="total_rentals", color_continuous_scale="blues")
st.plotly_chart(fig, use_container_width=True)

# Visualisasi soal 2: Perbedaan Jenis Pengguna
st.subheader("👥 Perbandingan Pengguna Kasual dan Terdaftar")
data_pertahun = data.groupby("year")[["casual", "registered"]].sum().reset_index()
data_pertahun_melt = data_pertahun.melt(id_vars="year", var_name="Tipe Pengguna", value_name="Jumlah Penyewa")
fig = px.bar(data_pertahun_melt, x="year", y="Jumlah Penyewa", color="Tipe Pengguna", barmode="group")
st.plotly_chart(fig, use_container_width=True)

# Visualisasi soal 3: Rata-rata penyewaan sepeda per musim

total_kasual_permusim = data.groupby("season")["casual"].mean().reset_index()
total_terdaftar_permusim = data.groupby("season")["registered"].mean().reset_index()

data_permusim = pd.merge(
    left=total_kasual_permusim,
    right=total_terdaftar_permusim,
    how="left",
    on="season"
)
data_permusim.rename(columns={"casual": "avg_casual", "registered": "avg_registered"}, inplace=True)

st.subheader("🌦️ Rata-rata Penyewaan Sepeda per Musim")
fig, ax = plt.subplots()
colors = plt.get_cmap("Set1").colors
season_labels = ["Spring", "Summer", "Fall", "Winter"]
seasons = range(len(data_permusim))

ax.bar(seasons, data_permusim["avg_casual"], width=0.4, label="Kasual", color=colors[0], alpha=0.7)
ax.bar([s + 0.4 for s in seasons], data_permusim["avg_registered"], width=0.4, label="Terdaftar",color=colors[1], alpha=0.7)

ax.set_xticks(seasons)
ax.set_xticklabels(season_labels)
ax.set_xlabel("Musim")
ax.set_ylabel("Rata-rata Penyewa")
ax.set_title("Rata-rata Penyewa Kasual dan Terdaftar per Musim")
ax.legend()

st.pyplot(fig)

