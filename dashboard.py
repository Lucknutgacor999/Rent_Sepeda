import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mticker

# Load dataset
data = pd.read_csv("data_clean.csv")

# Convert date column
data["dteday"] = pd.to_datetime(data["dteday"])

# Tambahkan kolom tahun dan bulan
data["year"] = data["dteday"].dt.year
data["month"] = data["dteday"].dt.month
data["day"] = data["dteday"].dt.day

# Dictionary mapping angka bulan ke nama bulan dalam bahasa Indonesia
dict_bulan = {
    1: "Januari", 2: "Februari", 3: "Maret", 4: "April", 5: "Mei", 6: "Juni",
    7: "Juli", 8: "Agustus", 9: "September", 10: "Oktober", 11: "November", 12: "Desember"
}

# Title
st.title("Dashboard Penyewaan Sepeda")

#Sidebar
st.sidebar.title("Bicycle Rent")
st.sidebar.image ("../img/logo.jpg", width=300)
st.sidebar.title("Filter Jumlah Penyewaan Per Hari")
selected_year = st.sidebar.selectbox("Pilih Tahun", options=sorted(data["dteday"].dt.year.unique()))

# Filter data berdasarkan tahun 
data_filtered = data[data["dteday"].dt.year == selected_year]

# Filter Bulan
selected_month = st.sidebar.selectbox(
    "Pilih Bulan",
    options=[dict_bulan[m] for m in sorted(data_filtered["month"].unique())]
)

# Konversi nama bulan ke angka
selected_month_num = {v: k for k, v in dict_bulan.items()}[selected_month]

# Filter data berdasarkan bulan
data_filtered = data_filtered[data_filtered["month"] == selected_month_num]

# Visualisasi jumlah penyewa per hari
st.subheader("Jumlah Penyewa Sepeda per Hari")
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(x=data_filtered["dteday"], y=data_filtered["total_rentals"], ax=ax)
ax.set_xlabel("Tanggal")
ax.set_ylabel("Jumlah Penyewa")
st.pyplot(fig)

# Visualisasi jumlah penyewa per bulan
dict_bulan = {
    1: "Januari", 2: "Februari", 3: "Maret", 4: "April", 5: "Mei", 6: "Juni",
    7: "Juli", 8: "Agustus", 9: "September", 10: "Oktober", 11: "November", 12: "Desember"
}

monthly_rentals = data_filtered.groupby("month")["total_rentals"].sum().reset_index()
monthly_rentals["month_name"] = monthly_rentals["month"].map(dict_bulan)  # Ubah angka bulan ke nama bulan

# Urutkan nama bulan sesuai urutan kalender
monthly_rentals = data.groupby("month")["total_rentals"].sum().reset_index()
monthly_rentals["month_name"] = monthly_rentals["month"].map(dict_bulan)
monthly_rentals = monthly_rentals.sort_values(by="month")

st.subheader("Jumlah Penyewa Sepeda per Bulan")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x=monthly_rentals["month_name"], y=monthly_rentals["total_rentals"], ax=ax, palette="Blues")
ax.set_xlabel("Bulan")
ax.set_ylabel("Jumlah Penyewa")
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
st.pyplot(fig)

# Visualisasi soal 1: Perbedaan jumlah penyewaan sepeda per tahun
total_kasual_pertahun = data.groupby("year")["casual"].sum().reset_index()
total_terdaftar_pertahun = data.groupby("year")["registered"].sum().reset_index()
data_pertahun = pd.merge(total_kasual_pertahun, total_terdaftar_pertahun, on="year")
data_pertahun_melt = data_pertahun.melt(id_vars='year', var_name='tipe_pengguna', value_name='jumlah_pengguna')

st.subheader("Perbedaan Penyewaan Sepeda per Tahun")
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x="year", y="jumlah_pengguna", hue="tipe_pengguna", data=data_pertahun_melt, palette="Set1", ax=ax)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
plt.xlabel("Tahun")
plt.ylabel("Jumlah Penyewa")
st.pyplot(fig)

# Visualisasi soal 2: Puncak casual vs terdaftar
dict_bulan = {
    "Januari": 1, "Februari": 2, "Maret": 3, "April": 4, "Mei": 5, "Juni": 6,
    "Juli": 7, "Agustus": 8, "September": 9, "Oktober": 10, "November": 11, "Desember": 12
}
if data["month"].dtype == object:
    data["month"] = data["month"].map(dict_bulan)

data["month"] = pd.to_numeric(data["month"], errors='coerce')

# Menghitung jumlah penyewa kasual dan terdaftar per bulan
total_kasual_perbulan = data.groupby("month")["casual"].sum().reset_index()
total_terdaftar_perbulan = data.groupby("month")["registered"].sum().reset_index()

# Menggabungkan data
data_perbulan = pd.merge(
    left=total_kasual_perbulan,
    right=total_terdaftar_perbulan,
    how="left",
    on="month"
)

data_perbulan["month"] = data_perbulan["month"].astype(int)

dict_bulan_reverse = {v: k for k, v in dict_bulan.items()}
data_perbulan["month_name"] = data_perbulan["month"].map(dict_bulan_reverse)
data_perbulan = data_perbulan.sort_values(by="month")

# Pilihan jenis pengguna
jenis_pengguna = st.multiselect(
    "Pilih jenis pengguna:",
    ["Kasual", "Terdaftar"],
    default=["Kasual", "Terdaftar"]
)

fig, ax = plt.subplots()
colors = plt.get_cmap("Set1").colors
width = 0.4 
months = range(len(data_perbulan))

if "Kasual" in jenis_pengguna:
    ax.bar([m - width/2 for m in months], data_perbulan["casual"], width=width, label="Kasual", alpha=0.7, color=colors[0])
if "Terdaftar" in jenis_pengguna:
    ax.bar([m + width/2 for m in months], data_perbulan["registered"], width=width, label="Terdaftar", alpha=0.7, color=colors[1])

ax.set_xticks(months)
ax.set_xticklabels(data_perbulan["month_name"], rotation=60)
ax.set_xlabel("Bulan")
ax.set_ylabel("Puncak Penyewa")
ax.set_title("Puncak Penyewa Kasual dan Terdaftar per Bulan")
ax.legend()

st.pyplot(fig)

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

st.subheader("Rata-rata Penyewaan Sepeda per Musim")
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
