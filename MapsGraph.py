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

# =========================
# i18n Dictionary
# =========================
LANG = {
    "en": {
        "page_title": "West Java Map",
        "title": "🗺️ West Java Map with Distance Calculator",
        "desc": "Interactive map showing all cities/regencies in West Java with distance calculation",
        "about": "About",
        "about_info": "This application displays cities and regencies in West Java province with distance calculation between any two selected locations.",
        "features": "**Features:**",
        "feat_1": "- Interactive map with all cities/regencies",
        "feat_2": "- Connection lines between locations",
        "feat_3": "- Distance calculator",
        "feat_4": "- Route highlighting",
        "list_title": "City/Regency List",
        "main_map": "West Java Province Map",
        "show_connections": "Show connection lines between all cities",
        "tooltip_click": "Click for {city} info",
        "distance_calc": "📍 Distance Calculator",
        "select_first": "Select first city:",
        "select_second": "Select second city:",
        "calc_btn": "Calculate Distance",
        "warn_same": "Please select two different cities.",
        "distance_between": "**Distance between {c1} and {c2}: {d:.2f} km**",
        "route_title": "Route: {c1} → {c2}",
        "start": "Start: {city}",
        "dest": "Destination: {city}",
        "route_tooltip": "Route: {d:.2f} km",
        "map_features": "Map Features",
        "how_to": "How to Use",
        "mf": """
- **Blue markers**: City/regency locations
- **Red circles**: Highlighted city points
- **Gray lines**: Connections between cities
- **Blue route line**: Selected route between two cities
- **Green marker**: Starting point
- **Red marker**: Destination point
""",
        "htu": """
1. View all cities on the main map
2. Toggle connection lines on/off
3. Select two different cities
4. Click 'Calculate Distance'
5. View the route and distance
""",
        "footer": "West Java Cities and Regencies Map | Created with Streamlit and Folium",
        "lang_label": "Language / Bahasa",
        "lang_en": "English",
        "lang_id": "Bahasa Indonesia",
    },
    "id": {
        "page_title": "Peta Jawa Barat",
        "title": "🗺️ Peta Jawa Barat dengan Kalkulator Jarak",
        "desc": "Peta interaktif menampilkan seluruh kota/kabupaten di Jawa Barat serta perhitungan jarak",
        "about": "Tentang",
        "about_info": "Aplikasi ini menampilkan kota dan kabupaten di Provinsi Jawa Barat serta menghitung jarak antara dua lokasi yang dipilih.",
        "features": "**Fitur:**",
        "feat_1": "- Peta interaktif semua kota/kabupaten",
        "feat_2": "- Garis penghubung antar lokasi",
        "feat_3": "- Kalkulator jarak",
        "feat_4": "- Penyorotan rute",
        "list_title": "Daftar Kota/Kabupaten",
        "main_map": "Peta Provinsi Jawa Barat",
        "show_connections": "Tampilkan garis penghubung antar semua kota",
        "tooltip_click": "Klik untuk info {city}",
        "distance_calc": "📍 Kalkulator Jarak",
        "select_first": "Pilih kota pertama:",
        "select_second": "Pilih kota kedua:",
        "calc_btn": "Hitung Jarak",
        "warn_same": "Silakan pilih dua kota yang berbeda.",
        "distance_between": "**Jarak antara {c1} dan {c2}: {d:.2f} km**",
        "route_title": "Rute: {c1} → {c2}",
        "start": "Mulai: {city}",
        "dest": "Tujuan: {city}",
        "route_tooltip": "Rute: {d:.2f} km",
        "map_features": "Fitur Peta",
        "how_to": "Cara Menggunakan",
        "mf": """
- **Marker biru**: Lokasi kota/kabupaten
- **Lingkaran merah**: Penanda titik kota
- **Garis abu-abu**: Koneksi antar kota
- **Garis rute biru**: Rute terpilih antara dua kota
- **Marker hijau**: Titik awal
- **Marker merah**: Titik tujuan
""",
        "htu": """
1. Lihat semua kota di peta utama
2. Aktif/nonaktifkan garis koneksi
3. Pilih dua kota yang berbeda
4. Klik 'Hitung Jarak'
5. Lihat rute dan jaraknya
""",
        "footer": "Peta Kota dan Kabupaten Jawa Barat | Dibuat dengan Streamlit dan Folium",
        "lang_label": "Language / Bahasa",
        "lang_en": "English",
        "lang_id": "Bahasa Indonesia",
    }
}

# =========================
# Language selector (Sidebar)
# =========================
with st.sidebar:
    language = st.selectbox(
        LANG["en"]["lang_label"],
        options=[LANG["en"]["lang_en"], LANG["en"]["lang_id"]],
        index=1,  # default: Bahasa Indonesia
    )
lang_key = "en" if language == LANG["en"]["lang_en"] else "id"
T = LANG[lang_key]

# Konfigurasi halaman Streamlit
st.set_page_config(layout="wide", page_title=T["page_title"])
st.title(T["title"])
st.markdown(T["desc"])

# Sidebar untuk informasi
with st.sidebar:
    st.header(T["about"])
    st.info(T["about_info"])
    st.markdown(T["features"])
    st.markdown(T["feat_1"])
    st.markdown(T["feat_2"])
    st.markdown(T["feat_3"])
    st.markdown(T["feat_4"])

    st.header(T["list_title"])
    for i, city in enumerate(CITY_DATA.keys(), 1):
        st.write(f"{i}. {city}")

# Buat peta Jawa Barat utama
st.subheader(T["main_map"])

# Pilihan untuk menampilkan garis penghubung
show_connections = st.checkbox(T["show_connections"], value=True)

# Buat peta
m = folium.Map(location=[-6.914744, 107.609810], zoom_start=8)

# Tambahkan marker untuk setiap kota
for city, coords in CITY_DATA.items():
    folium.Marker(
        location=coords,
        popup=f"<b>{city}</b>",
        tooltip=T["tooltip_click"].format(city=city),
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

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
st_folium(m, width=1200, height=500)

# Section untuk kalkulator jarak
st.subheader(T["distance_calc"])

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    city1 = st.selectbox(
        T["select_first"],
        options=list(CITY_DATA.keys()),
        index=0,
        key="city1"
    )

with col2:
    city2_options = [city for city in CITY_DATA.keys() if city != city1]
    city2 = st.selectbox(
        T["select_second"],
        options=city2_options,
        index=0,
        key="city2"
    )

with col3:
    st.write("")
    st.write("")
    calculate_btn = st.button(T["calc_btn"], type="primary")

if calculate_btn or (city1 and city2):
    if city1 == city2:
        st.warning(T["warn_same"])
    else:
        distance = geodesic(CITY_DATA[city1], CITY_DATA[city2]).kilometers
        st.success(T["distance_between"].format(c1=city1, c2=city2, d=distance))

        st.subheader(T["route_title"].format(c1=city1, c2=city2))

        lat1, lon1 = CITY_DATA[city1]
        lat2, lon2 = CITY_DATA[city2]
        center_lat = (lat1 + lat2) / 2
        center_lon = (lon1 + lon2) / 2

        m2 = folium.Map(location=[center_lat, center_lon], zoom_start=9)

        folium.Marker(
            location=CITY_DATA[city1],
            popup=f"<b>{T['start'].format(city=city1)}</b>",
            tooltip=T["start"].format(city=city1),
            icon=folium.Icon(color='green', icon='play', prefix='fa')
        ).add_to(m2)

        folium.Marker(
            location=CITY_DATA[city2],
            popup=f"<b>{T['dest'].format(city=city2)}</b>",
            tooltip=T["dest"].format(city=city2),
            icon=folium.Icon(color='red', icon='stop', prefix='fa')
        ).add_to(m2)

        folium.PolyLine(
            locations=[CITY_DATA[city1], CITY_DATA[city2]],
            color="blue",
            weight=4,
            opacity=0.8,
            tooltip=T["route_tooltip"].format(d=distance)
        ).add_to(m2)

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
    st.subheader(T["map_features"])
    st.markdown(T["mf"])

with col_info2:
    st.subheader(T["how_to"])
    st.markdown(T["htu"])

# Footer
st.markdown("---")
st.caption(T["footer"])
