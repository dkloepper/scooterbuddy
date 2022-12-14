import streamlit as st

st.title("Scooter Buddy -- Data Overview")
st.markdown("""---""")

st.header("Data Source --  Open Data Minneapolis")
st.markdown('<a url="https://opendata.minneapolismn.gov/">Open Data Minneapolis</a>',unsafe_allow_html=True)
st.markdown("The city of Minneapolis provides public access to a variety of GIS and non-spatial data, including things like 311 activity, snow emergency towing, and even scooters.")
st.subheader("Scooter Data")
st.markdown('<a url="https://opendata.minneapolismn.gov/search?groupIds=9bc71a032e984a22a5e94312d9d9bf7f">Scooter Data</a>',unsafe_allow_html=True)
st.subheader("Location Data")

st.header("Data Type -- GeoJSON")

st.header("Data Cleansing")