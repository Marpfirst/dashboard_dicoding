import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Memuat data dari file CSV
china = pd.read_csv("China.csv")
china['date'] = pd.to_datetime(china['date'])  # Konversi kolom date ke format datetime


# Fungsi untuk membuat scatter plot
def environmental_factors_vs_pollutants_scatter(station, variable, target_pollutant):
    fig, ax = plt.subplots(figsize=(8, 6))

    if target_pollutant.lower() == 'polusi udara':
        target_pollutant = 'Polusi Udara'

    ax.scatter(station[variable], station[target_pollutant], s=5, alpha=0.5, c="#FACE2D", marker='o', edgecolors="#ed7d53")
    ax.set_xlabel(variable, fontsize=20)
    ax.set_ylabel(target_pollutant, fontsize=20)
    
    if variable == 'TEMP':
        title = "Suhu"
    elif variable == 'PRES':
        title = "Tekanan"
    elif variable == 'DEWP':
        title = "Titik Embun"
    elif variable == 'RAIN':
        title = "Hujan"
    elif variable == 'wd':
        title = "Arah Angin"
    elif variable == 'WSPM':
        title = "Kecepatan Angin"
    else:
        title = variable  # Use the variable name if not in the predefined variables

    title = f"Tingkat Polusi Udara terhadap {title} di {station['station'].iloc[0]}"
    plt.title(title, fontsize=25)

    st.pyplot(fig)

# Fungsi untuk membuat heatmap korelasi
def correlation_heatmap(df, selected_variables, selected_pollutants):
    selected_columns = selected_variables + selected_pollutants
    numeric_columns = df[selected_columns].select_dtypes(include=['float64', 'int64']).columns

    correlation_matrix = df[numeric_columns].corr()

    fig, ax = plt.subplots(figsize=(15, 10))
    sns.heatmap(correlation_matrix, vmax=1, vmin=-1, center=0, cmap="viridis", annot=True, linewidths=.5)
    ax.tick_params(labelsize=15)
    ax.set_title("Correlation Heatmap", loc="center", fontsize=20)

    st.pyplot(fig)

def plot_yearly_variation(data, selected_pollutants):
    # Agregasi data tahunan di semua stasiun
    year_data_all_stations = data.groupby(['station', 'year']).agg({
        'PM2.5': 'mean',
        'PM10': 'mean',
        'SO2': 'mean',
        'NO2': 'mean',
        'CO': 'mean',
        'O3': 'mean'
    }).reset_index()

    # Visualisasi data tahunan di semua stasiun berdasarkan polutan yang dipilih
    fig, ax = plt.subplots(figsize=(14, 8))

    for station in data['station'].unique():
        for selected_pollutant in selected_pollutants:
            station_data = year_data_all_stations[year_data_all_stations['station'] == station]
            ax.plot(station_data['year'], station_data[selected_pollutant], label=f"{station} - {selected_pollutant}")

    ax.set_title(f'Variasi Tahunan {", ".join(selected_pollutants)} di Semua Stasiun')
    ax.set_xlabel('Tahun')
    ax.set_ylabel('Nilai Rata-Rata')
    ax.legend()

    # Menampilkan plot di Streamlit
    st.pyplot(fig)
    
    
# Pilihan variabel dan polutan
variables = ['TEMP', 'PRES', 'DEWP', 'RAIN', 'wd', 'WSPM']
pollutants = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']


with st.sidebar:
    # Title
    st.title("Pra")

    # Logo Image
    st.image("https://img.freepik.com/free-vector/polluted-earth-icon_1308-27704.jpg?w=740&t=st=1709544210~exp=1709544810~hmac=8870f60a4a970bedb13b9302de3e85f59066ab872f3f7e15e829893f0b631674")

st.title("Air Quality in China")

# Tampilkan hasil variasi tahunan 
with st.container():
    st.subheader(f"Variasi Tahunan Polutan Udara di Semua Stasiun")
    # Pilihan polutan
    pollutants = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
    selected_pollutant = st.selectbox("Pilih Polutan", pollutants, key="yearly_variation_pollutant")
    # Memanggil fungsi untuk membuat plot
    plot_yearly_variation(china, [selected_pollutant])


# Tampilkan hasil untuk scatter
with st.container():
    st.subheader(f"Tingkat Polusi Udara dengan Kondisi tertentu terhadap Polutan")
    # Pilihan stasiun, variabel, dan polutan
    stations = china['station'].unique()
    selected_station = st.selectbox("Pilih Stasiun", stations, key="scatter_station")

    variables = ['TEMP', 'PRES', 'DEWP', 'RAIN', 'wd', 'WSPM']
    selected_variable = st.selectbox("Pilih Variabel", variables, key="scatter_variable")

    pollutants = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
    selected_pollutant = st.selectbox("Pilih Polutan", pollutants, key="scatter_pollutant")

    # Filter data berdasarkan stasiun yang dipilih
    selected_station_data = china[china['station'] == selected_station]

    # Memanggil fungsi untuk membuat scatter plot
    environmental_factors_vs_pollutants_scatter(selected_station_data, selected_variable, selected_pollutant)


# Tampilkan hasil untuk heatmap
with st.container():
    st.subheader(f"Heatmap Korelasi")
    # Multiselect untuk variabel dan polutan
    selected_variables = st.multiselect("Pilih Variabel", variables, default=variables, key="heatmap_variables")
    selected_pollutants = st.multiselect("Pilih Polutan", pollutants, default=pollutants, key="heatmap_pollutants")
    # Memanggil fungsi untuk membuat heatmap korelasi
    correlation_heatmap(china, selected_variables, selected_pollutants)
    




