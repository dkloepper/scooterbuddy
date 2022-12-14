import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(
    layout="wide"
)


st.title("Scooter Buddy: Project Overview")
st.text("David Kloepper (kloe0021@umn.edu")
st.markdown("""---""")

st.subheader("Project Origins")
st.markdown("This app was developed as a final course project for MABA6490, fall semester 2022. &nbsp;\
        Full disclosure: I have never rented a scooter or even taken a ride on one. Maybe for graduation...&nbsp; \
        The idea for this app was rather random. I had originally thought to use data on snow emergencies to predict likihood to be towed, but instead saw that scooter data was available and was futher motivated by seeing scooters in from of CSOM.&nbsp; \
        This sent me down the rabbit hole of addresses, centerlines, and geocoordinates.")
st.markdown('GitHub Repository can be found <a href="https://github.com/dkloepper/scooterbuddy/">HERE</a>.',unsafe_allow_html=True)


left, right = st.columns(2)

with left:

    st.header("Project Learnings and Future Work:") 

    st.markdown("* There is a Python module for just about anything. Never would have known about geoPandas or folium without this project.")
    st.markdown("* Streamlit can be a lot of fun to customize. Columns, sidebars, multipages.")
    st.markdown("* Streamlit can be trick to make performant. Case in point: address selection")
    st.markdown("* Exporting models creates really big files! Like GBs of data.")
    st.markdown("* GitHub Desktop is way better than using GitBash (except for LFS)")
    st.markdown("* How to upload large files with GitHub LFS. Had to use GitBash")
    st.markdown("* GitHub has a data cap! This project represents my second repo after crashing the first.")
    st.markdown("* The need to have data for the model for scooters unavailable. Without it, everything predicts as 1")
    st.markdown('* Rethinking training data approach, using 2019 and 2020 data to predict 2021.')
    st.markdown("* Pycaret can be useful for model selection, but also a pain. I encountered sklearn versioning issues galore.")
    st.markdown("* ")

with right:
    st.image('csom1.png', width=500)

    m = folium.Map(location=[44.97040, -93.24511], zoom_start=18)
    folium.Marker(
        [44.97040, -93.24511], popup="Carlson School of Management"
    ).add_to(m)

    st_data = st_folium(m, width = 500, height=500, returned_objects=[])

about_mapping = st.container()

with about_mapping:
    st.subheader("About Mapping") 

    st.markdown("The maps in this app are powered by Folium and streamlit_folium")
    st.markdown("Folium allows you do your data wrangling in Python and apply it to a map build with leaflet.js (NO javascript required)")
    st.markdown("streamlit_folium enables easy application of Folium within a streamlit app.")

    st.markdown("Here is all the code required to draw the map above:")

    mapping_code = '''

    import folium
    import streamlit as st

    from streamlit_folium import st_folium

    m = folium.Map(location=[44.97040, -93.24511], zoom_start=18)
    folium.Marker(
        [44.97040, -93.24511], popup="Carlson School of Management"
    ).add_to(m)

    st_data = st_folium(m, width = 500, height=500, returned_objects=[])'''
    st.code(mapping_code, language='python')