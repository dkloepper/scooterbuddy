import streamlit as st

with st.sidebar:
    st.image('scooter.jpg')

st.title("Scooter Buddy -- Data Overview")
st.markdown("---")

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
st.markdown('I used two location-based datasets as input and connection to the scooter data:')
st.markdown('- *EAS Address:* This dataset contains all addresses for the city of Minneapolis. From this dataset, I used the "display" address as well as the latitude/longitude of the address. In total, there were 154,706 unique address records in the dataset.')
st.markdown('<a href="https://opendata.minneapolismn.gov/datasets/cityoflakes::eas-addresses/about">EAS Addresses/a>',unsafe_allow_html=True)
st.markdown('- *Centerline MPLS:* This dataset contains the coordinates for the center of the pavement for all drivable streets in Minneapolis. These centerlines are used as locations in the scooter data, building hte connection to geo-location. There were 13,838 centerline records in the dataset.')
st.markdown('<a href="https://opendata.minneapolismn.gov/datasets/cityoflakes::mpls-centerline/about">MPLS Centerline</a>',unsafe_allow_html=True)

st.header("Data Type -- GeoJSON & GeoPandas")
st.markdown('''GeoJSON is a format for encoding geographic structures like points, lines, and various polygon shapes.

In the case of the address data, each record contained a POINT with the latitude/longitude coordinates.

The centerline data was, unsuprisinly a LineString with begining and end points marked with latitude/longitude.''')
st.markdown('<a href="https://geojson.org/">GeoJSON</a>',unsafe_allow_html=True)

st.markdown('''The GeoPandas module extends the standard features of Pandas, making it easy to work with the GeoJSON data types within a dataframe. 
It also provides convient functions for processes like calculating distance or finding the centroid of two points.''')
st.markdown('<a href="https://geopandas.org/en/stable/">GeoPandas</a>',unsafe_allow_html=True)

st.header("Data Cleansing")
st.subheader("Scooter Data")
st.markdown('''
The scooter data was transformed in the following ways to support the modeling: 
1. The 2019, 2020 and 2021 datasets were combined into a single data frame. Columns were the same except for the primary ID column.
2. Date transformations were performed to break down the PollDate in to component fields (Year, Month, Hour, Day of Week, Day of Year).
3. Scooter data for "trail" centerlines was dropped since they were not in the MPLS data.
4. Numeric hours were converted into text ranges. This was done because poll times were not consistent across the years
5. Duplicate records were created due to time bucketing and were dropped. 
6. Brand field was converted to one-hot-encoding. Hour ranges were changed to ordinalEncoding. All numeric fields were optimized and uneeded fields dropped. 
''')
st.subheader("Location Data")
st.markdown('''
The location data was modified to support the location finding and minimize uncessary data loaded in Streamlit:
1. For centerlines, a centroid was calcualted for each, creating a single point for each record rather than line ends.
2. For address and centerlines geolocations, latitude and longitude were constructed to a format easily consumed by Folium.
3. Geolocation values were encoded to a new format that enabled easy calculation of distance in feet/miles rather than radians.
4. Numeric hours were converted into text ranges. This was done because poll times were not consistent across the years
5. Uncessary fields were dropped from each, leaving a single description field with the important geolocation information. 
''')