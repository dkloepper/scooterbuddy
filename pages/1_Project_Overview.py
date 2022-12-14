import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(
    layout="wide"
)

st.title("Scooter Buddy: Project Overview")
st.text("David Kloepper (kloe0021@umn.edu")
st.markdown("""---""")

left, right = st.columns(2)

st.markdown("This app was developed as a final course project for MABA6490, fall semester 2022. \
        Full disclosure: I have never rented a scooter or even taken a ride on one. \
        The idea for this app was rather random. I had originally thought to use data on snow emergencies to predict likihood to be towed, but instead saw that scooter data was available and was futher motivated by seeing scooters in from of CSOM.")

with left:

    st.subheader("Project Objectives:") 

    st.markdown("* Create a Streamlit app [deployed] to showcase your idea:"
    "* Add any visualization, details on the streamlit"
    "* The app should also be a demo of your idea"
    "* There should be a small intro of the idea at the start of streamlit"
    "* The model should be deployed , i.e. you cannot process the training data /corpus at run time, it has to be loaded in to the streamlit app"
    "* The app should take a user input and ""predict"" something [only on the app at runtime]"
    "* You will get 15 min max to present your entire ideas with Q&A"
    "* You will get an opportunity to provide feedback on each of your peer form for each project [except your own] and email me ONLY. The results will be aggregated and top three projects will be announced."
    "* The peer review will make up a size-able %age of your project grade.")



with right:
    st.image('csom1.png', width=250)

    m = folium.Map(location=[44.67040, -93.24511], zoom_start=18)
    folium.Marker(
        [44.67040, -93.24511], popup="Carlson School of Management"
    ).add_to(m)

    st_data = st_folium(m, width = 250, height=250, returned_objects=[])