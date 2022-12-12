import streamlit as st

from streamlit_folium import st_folium


st.set_page_config(
    page_title="Scooter Buddy - Project Overview",
    page_icon="🛴",
    layout="wide",
)

m = folium.Map(location=[44.968996124, -93.240332372], zoom_start=18)
folium.Marker(
    [44.968996124, -93.240332372], popup="Carlson School of Management"
).add_to(m)

st_data = st_folium(m, width = 725, returned_objects=[])