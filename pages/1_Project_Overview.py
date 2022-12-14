import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(
    layout="wide"
)

st.title("Scooter Buddy: Project Overview")
st.text("David Kloepper (kloe0021@umn.edu")
st.markdown("""---""")

st.markdown("This app was developed as a final course project for MABA6490, fall semester 2022. U+000A \
        Full disclosure: I have never rented a scooter or even taken a ride on one. U+000A \
        The idea for this app was rather random. I had originally thought to use data on snow emergencies to predict likihood to be towed, but instead saw that scooter data was available and was futher motivated by seeing scooters in from of CSOM.")

left, right = st.columns(2)

with left:

    st.subheader("Project Learnings:") 

    st.markdown("* There is a Python module for just about anything.")
    st.markdown("* Streamlit can be a lot of fun to customize.")
    st.markdown("* Streamlit can be trick to make performant")
    st.markdown("* Exporting models creates really big files!")
    st.markdown("* How to upload large files with GitHub LFS")
    st.markdown("* GitHub has a data cap!")
    st.markdown("* The need to have data for the model for scooters unavailable")
    st.markdown("* ")
    st.markdown("* ")
    st.markdown("* ")

with right:
    st.image('csom1.png', width=500)

    m = folium.Map(location=[44.97040, -93.24511], zoom_start=18)
    folium.Marker(
        [44.97040, -93.24511], popup="Carlson School of Management"
    ).add_to(m)

    st_data = st_folium(m, width = 500, height=500, returned_objects=[])