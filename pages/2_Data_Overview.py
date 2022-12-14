import streamlit as st

st.title("Scooter Buddy -- Data Overview")
st.markdown("""---""")

st.header("Data Source --  Open Data Minneapolis")
st.markdown('<a href="https://opendata.minneapolismn.gov/">Open Data Minneapolis</a>',unsafe_allow_html=True)
st.markdown("The city of Minneapolis provides public access to a variety of GIS and non-spatial data, including things like 311 activity, snow emergency towing, and even scooters.")
st.subheader("Scooter Data")
st.markdown('<a href="https://opendata.minneapolismn.gov/search?groupIds=9bc71a032e984a22a5e94312d9d9bf7f">Scooter Data</a>',unsafe_allow_html=True)
st.markdown("Three datasets are available for 2019, 2020, and 2021 that include scooter availability checkpoints within the City of Minneapolis for the pilot program that began in March 2019. Availability data is polled using GBFS feeds every four hours for a snapshot of where scooters were located within the City.")
st.markdown("Field Descriptions")
st.markdown('- *PollTime:* The time the API was polled for a snapshot of available scooters.')
st.markdown('- CompanyName: The name of the company polled. ')
st.markdown('- NumberAvailable: The number of scooters available on the street or trail centerline ID at the time the API was polled.') 
st.markdown('- ClosestCenterlineID: the closest street centerline GBSID or trail centerline Feature Unique ID.')
st.markdown('- ClosestCenterlineType: The type of centerline, either street or trail.') 
st.markdown('- Neighborhood: The neighborhood the centerline segment is located in.')

st.subheader("Location Data")

st.header("Data Type -- GeoJSON")

st.header("Data Cleansing")