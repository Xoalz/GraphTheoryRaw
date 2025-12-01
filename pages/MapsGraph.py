import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.distance import geodesic
import pandas as pd

# Data koordinat kabupaten/kota di Jawa Barat
CITY_DATA = {
    "Bandung": (-6.914744, 107.609810),
    "Bogor": (-6.597147, 106.806038),
    "Bekasi": (-6.238270, 106.975571),
    "Cirebon": (-6.732023, 108.552316),
    "Garut": (-7.227906, 107.908699),
    "Tasikmalaya": (-7.350580, 108.217163),
    "Ciamis": (-7.332000, 108.349000),
    "Sumedang": (-6.858000, 107.919000),
    "Indramayu": (-6.337000, 108.325000),
    "Majalengka": (-6.836000, 108.227000),
    "Kuningan": (-6.976000, 108.483000),
    "Cianjur": (-6.818000, 107.140000),
    "Sukabumi": (-6.924000, 106.930000),
    "Purwakarta": (-6.539000, 107.443000),
    "Karawang": (-6.304000, 107.305000),
    "Subang": (-6.570000, 107.763000),
    "Pangandaran": (-7.667000, 108.650000),
    "Depok": (-6.402484, 106.794243),
    "Cimahi": (-6.884082, 107.541307),
    "Banjar": (-7.369722, 108.534722)
}

# Konfigurasi halaman Streamlit
st.set_page_config(layout="wide", page_title="West Java Map")
st.title("🗺️ West Java Map with Distance Calculator")
st.markdown("Interactive map showing all cities/regencies in West Java with distance calculation")

# Sidebar untuk informasi
with st.sidebar:
    st.header("About")
    st.info("This application displays cities and regencies in West Java province with distance calculation between any two selected locations.")
    st.markdown("**Features:**")
    st.markdown("- Interactive map with all cities/regencies")
    st.markdown("- Connection lines between locations")
    st.markdown("- Distance calculator")
    st.markdown("- Route highlighting")
    
    st.header("City/Regency List")
    for i, city in enumerate(CITY_DATA.keys(), 1):
        st.write(f"{i}. {city}")

# Buat peta Jawa Barat utama
st.subheader("West Java Province Map")

# Pilihan untuk menampilkan garis penghubung
show_connections = st.checkbox("Show connection lines between all cities", value=True)

# Buat peta
m = folium.Map(location=[-6.914744, 107.609810], zoom_start=8)

# Tambahkan marker untuk setiap kota dengan styling yang lebih baik
for city, coords in CITY_DATA.items():
    folium.Marker(
        location=coords,
        popup=f"<b>{city}</b>",
        tooltip=f"Click for {city} info",
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)
    
    # Tambahkan circle marker untuk menonjolkan titik
    folium.CircleMarker(
        location=coords,
        radius=8,
        popup=city,
        color='red',
        fill=True,
        fill_color='red',
        fill_opacity=0.6,
        weight=2
    ).add_to(m)

# Tambahkan garis penghubung antar kota jika checkbox dicentang
if show_connections:
    cities_list = list(CITY_DATA.items())
    for i in range(len(cities_list)):
        for j in range(i + 1, len(cities_list)):
            folium.PolyLine(
                locations=[cities_list[i][1], cities_list[j][1]],
                color="gray",
                weight=1,
                opacity=0.3,
                tooltip=f"{cities_list[i][0]} - {cities_list[j][0]}"
            ).add_to(m)

# Tampilkan peta utama
st_data = st_folium(m, width=1200, height=500)

# Section untuk kalkulator jarak
st.subheader("📍 Distance Calculator")

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    city1 = st.selectbox("Select first city:", 
                        options=list(CITY_DATA.keys()), 
                        index=0,
                        key="city1")

with col2:
    # Filter untuk tidak memilih kota yang sama
    city2_options = [city for city in CITY_DATA.keys() if city != city1]
    city2 = st.selectbox("Select second city:", 
                        options=city2_options, 
                        index=0,
                        key="city2")

with col3:
    st.write("")  # Spacer
    st.write("")  # Spacer
    calculate_btn = st.button("Calculate Distance", type="primary")

if calculate_btn or (city1 and city2):
    if city1 == city2:
        st.warning("Please select two different cities.")
    else:
        # Hitung jarak
        distance = geodesic(CITY_DATA[city1], CITY_DATA[city2]).kilometers
        
        # Tampilkan hasil
        st.success(f"**Distance between {city1} and {city2}: {distance:.2f} km**")
        
        # Buat peta khusus untuk rute yang dipilih
        st.subheader(f"Route: {city1} → {city2}")
        
        # Hitung titik tengah untuk zoom yang optimal
        lat1, lon1 = CITY_DATA[city1]
        lat2, lon2 = CITY_DATA[city2]
        center_lat = (lat1 + lat2) / 2
        center_lon = (lon1 + lon2) / 2
        
        m2 = folium.Map(location=[center_lat, center_lon], zoom_start=9)
        
        # Tambahkan marker untuk kedua kota dengan warna berbeda
        folium.Marker(
            location=CITY_DATA[city1],
            popup=f"<b>Start: {city1}</b>",
            tooltip=f"Start: {city1}",
            icon=folium.Icon(color='green', icon='play', prefix='fa')
        ).add_to(m2)
        
        folium.Marker(
            location=CITY_DATA[city2],
            popup=f"<b>Destination: {city2}</b>",
            tooltip=f"Destination: {city2}",
            icon=folium.Icon(color='red', icon='stop', prefix='fa')
        ).add_to(m2)
        
        # Garis berwarna untuk rute yang dipilih
        folium.PolyLine(
            locations=[CITY_DATA[city1], CITY_DATA[city2]],
            color="blue",
            weight=4,
            opacity=0.8,
            tooltip=f"Route: {distance:.2f} km"
        ).add_to(m2)
        
        # Tambahkan circle marker untuk menonjolkan titik
        folium.CircleMarker(
            location=CITY_DATA[city1],
            radius=10,
            popup=city1,
            color='green',
            fill=True,
            fill_color='green',
            fill_opacity=0.7,
            weight=3
        ).add_to(m2)
        
        folium.CircleMarker(
            location=CITY_DATA[city2],
            radius=10,
            popup=city2,
            color='red',
            fill=True,
            fill_color='red',
            fill_opacity=0.7,
            weight=3
        ).add_to(m2)
        
        st_folium(m2, width=1200, height=400)

# Informasi tambahan
st.markdown("---")
col_info1, col_info2 = st.columns(2)

with col_info1:
    st.subheader("Map Features")
    st.markdown("""
    - **Blue markers**: City/regency locations
    - **Red circles**: Highlighted city points
    - **Gray lines**: Connections between cities
    - **Blue route line**: Selected route between two cities
    - **Green marker**: Starting point
    - **Red marker**: Destination point
    """)

with col_info2:
    st.subheader("How to Use")
    st.markdown("""
    1. View all cities on the main map
    2. Toggle connection lines on/off
    3. Select two different cities
    4. Click 'Calculate Distance'
    5. View the route and distance
    """)

# Footer
st.markdown("---")
st.caption("West Java Cities and Regencies Map | Created with Streamlit and Folium")