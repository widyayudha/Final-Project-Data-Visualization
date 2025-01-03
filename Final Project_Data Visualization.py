import streamlit as st
import pandas as pd
import altair as alt

# Load the dataset
file_path = 'Tingkat Pengangguran Terbuka (TPT) dan Tingkat Partisipasi Angkatan Kerja (TPAK) Menurut Provinsi, 2023.xlsx'
data = pd.read_excel(file_path, sheet_name='Sheet1')

# Clean and prepare data
data.columns = [col.strip() for col in data.columns]  # Strip whitespace from column names

# Bersihkan data untuk memastikan kolom numerik tidak mengandung nilai non-numerik
data['Tingkat Pengangguran Terbuka (TPT) - Februari'] = pd.to_numeric(
    data['Tingkat Pengangguran Terbuka (TPT) - Februari'], errors='coerce'
)
data['Tingkat Pengangguran Terbuka (TPT) - Agustus'] = pd.to_numeric(
    data['Tingkat Pengangguran Terbuka (TPT) - Agustus'], errors='coerce'
)

# Isi nilai NaN dengan 0 atau hapus baris dengan nilai NaN jika diperlukan
data = data.dropna(subset=[
    'Tingkat Pengangguran Terbuka (TPT) - Februari',
    'Tingkat Pengangguran Terbuka (TPT) - Agustus'
])

# Streamlit app setup
st.set_page_config(
    page_title="Visualisasi Data Pengangguran Indonesia",
    page_icon="📊",
    layout="wide",
)

# Header and description
st.title("📊 Visualisasi Data Pengangguran Indonesia - 2023")
st.markdown(
    """
    Dataset ini menampilkan Tingkat Pengangguran Terbuka (TPT) 
    dan Tingkat Partisipasi Angkatan Kerja (TPAK) menurut provinsi di Indonesia untuk tahun 2023 pada bulan Februari dan Agustus.
    
    ---
    Dataset ini memberikan gambaran penting tentang kondisi ketenagakerjaan di Indonesia,
    khususnya tingkat pengangguran dan partisipasi tenaga kerja.
    """
)

# Sidebar filters
st.sidebar.header("🔍 Filter Data")
selected_provinces = st.sidebar.multiselect(
    "Pilih Provinsi",
    options=data['Provinsi'].unique().tolist(),
    default=data['Provinsi'].unique().tolist()
)

metric = st.sidebar.selectbox(
    "Pilih Metrik",
    [
        "Tingkat Pengangguran Terbuka (TPT) - Februari",
        "Tingkat Pengangguran Terbuka (TPT) - Agustus"
    ]
)

min_value, max_value = st.sidebar.slider(
    "Filter Rentang Nilai",
    min_value=float(data[metric].min()),
    max_value=float(data[metric].max()),
    value=(float(data[metric].min()), float(data[metric].max()))
)

chart_type = st.sidebar.radio(
    "Pilih Tipe Chart",
    options=["Bar", "Line", "Scatter"],
    index=0
)

# Filter data
filtered_data = data[
    (data['Provinsi'].isin(selected_provinces)) &
    (data[metric] >= min_value) &
    (data[metric] <= max_value)
]

# Main section with chart and data table
st.subheader(f"Visualisasi {metric}")

# Create chart based on the selected type
if chart_type == "Bar":
    chart = alt.Chart(filtered_data).mark_bar().encode(
        x=alt.X('Provinsi:N', sort='-y', title="Provinsi"),
        y=alt.Y(metric, title=metric),
        color=alt.Color(metric, scale=alt.Scale(scheme='blues'), legend=alt.Legend(
            titleLimit=200,
            titleAlign="left"
        )),
        tooltip=['Provinsi', metric]
    ).properties(
        width=800,
        height=450
    )
elif chart_type == "Line":
    chart = alt.Chart(filtered_data).mark_line(point=True).encode(
        x=alt.X('Provinsi:N', sort='-y', title="Provinsi"),
        y=alt.Y(metric, title=metric),
        color=alt.Color('Provinsi:N', legend=None),
        tooltip=['Provinsi', metric]
    ).properties(
        width=800,
        height=450
    )
else:  # Scatter
    chart = alt.Chart(filtered_data).mark_circle(size=100).encode(
        x=alt.X('Provinsi:N', sort='-y', title="Provinsi"),
        y=alt.Y(metric, title=metric),
        color=alt.Color(metric, scale=alt.Scale(scheme='blues'), legend=alt.Legend(
            titleLimit=200,
            titleAlign="left"
        )),
        tooltip=['Provinsi', metric]
    ).properties(
        width=800,
        height=450
    )

st.altair_chart(chart, use_container_width=True)

# Display data table
st.subheader("📋 Data Tabel")
st.dataframe(filtered_data)

# Footer
st.markdown(
    """
    ---
    **Dibuat dengan ❤️ oleh Kelompok TETEH**  
    """
)
