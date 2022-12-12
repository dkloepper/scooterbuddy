#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: David Kloepper (kloe0021@umn.edu)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import json

import geopandas as gpd

import pickle as pkl

import streamlit as st

#from IPython.display import display
#from ipywidgets import embed

from streamlit_folium import st_folium
import folium

from sklearn.neighbors import KNeighborsRegressor

#@st.cache(persist=True)

st.set_page_config(
    page_title="Scooter Buddy",
    page_icon="🛴",
    layout="wide",
)

@st.cache(allow_output_mutation=True)

#filename = 'scooter_pickle.sav'

def decompress_pickle_model(filename):
    with open(filename, 'rb') as fIn:
        scooter_pkl = pkl.load(fIn)
    model = scooter_pkl['model']
    return model

def decompress_pickle_address(filename):
    with open(filename, 'rb') as fIn:
        scooter_pkl = pkl.load(fIn)
    address_df = scooter_pkl['addresses']
    return address_df

def decompress_pickle_centerline(filename):
    with open(filename, 'rb') as fIn:
        scooter_pkl = pkl.load(fIn)
    centerline_df = scooter_pkl['centerlines']
    return centerline_df
    
model = decompress_pickle_model('scooter_pickle.sav')
#address_df = scooter_pkl['addresses']
#centerline_df = scooter_pkl['centerlines']

def get_coordinates(address):
    #Return the coordinates associated with address
    df = decompress_pickle_address('scooter_pickle.sav')
    coordinates = df.loc[df['Display'] == address]
    return coordinates

def find_within_dist(coords,dist):
    df = decompress_pickle_centerline('scooter_pickle.sav')
    df['distances'] = df.apply(lambda r: coords.distance(r['centroid'])  / 5279.98944, 
        axis=1)
    return df[(df['distances'] <= dist)]

def make_prediction(centerline, month, year, day_of_week, day_of_year, hour, cn_bird, cn_lime, cn_lyft, cn_spin):
  entry = pd.DataFrame([[centerline, month, year, day_of_week, day_of_year, hour, cn_bird, cn_lime, cn_lyft, cn_spin]], 
                 columns=["ClosestCenterlineID","month","year","day_of_week","day_of_year","hour","CompanyName_Bird","CompanyName_Lime","CompanyName_Lyft","CompanyName_Spin"])
  prediction = model.predict(entry)
  return prediction[0]

body_container = st.container()
input_container = st.container()
input_form = st.form("input",clear_on_submit=False)
result_container = st.container()
#form_sidebar = st.sidebar()

#with form_sidebar:
#with st.sidebar:
#with input_container:


with body_container:
    st.title("Scooter Buddy")
    st.markdown("""---""")

    with input_form:
        address_select = st.text_input("Enter your address")
        #address_select = st.selectbox("Select your address",address_df['Display'])

        date_select = st.date_input("What day do you want to ride?")

        hour_select = st.selectbox("Pick an hour range",('12am-5am','6am-8am','9am-11am','12pm-2pm','3pm-5pm','6pm-8pm','9pm-11pm'))

        brand = st.radio("Select a preferred brand:",('Bird','Lime','Lyft','Spin'))

        distance = st.selectbox("Select a distance from you",(.1,.15,.2,.25,.3,.35,.4,.45,.5,.75,1))

        #search_button = st.button('Find a scooter!')
        search_button = st.form_submit_button('Find a scooter!')

def mapping():

    month = date_select.month
    year = date_select.year
    day_of_week = date_select.weekday()
    day_of_year = date_select.timetuple().tm_yday

    if hour_select == '12am-5am':
        hour = 0
    elif hour_select == '6am-8am':
        hour = 1
    elif hour_select == '9am-11am':
        hour = 2
    elif hour_select == '12pm-2pm':
        hour = 3
    elif hour_select == '3pm-5pm':
        hour = 4
    elif hour_select == '6pm-8pm':
        hour = 5
    elif hour_select == '9pm-11pm':
        hour = 6 

    cn_bird = 0
    cn_lime = 0
    cn_lyft = 0
    cn_spin = 0

    if brand == 'Bird':
        cn_bird = 1
    elif brand == 'Lime':
        cn_lime = 1
    elif brand == 'Lyft':
        cn_lyft = 1
    elif brand == 'Spin':
        cn_spin = 1

    if distance < .25:
        zoom = 17
    elif distance < .5:
        zoom = 16
    elif distance < .75:
        zoom = 15
    elif distance <= 1:
        zoom = 14
    else:
        zoom = 18

    origin_point = get_coordinates(address_select)

    coords = origin_point.iloc[0]['geometry']
    origin_latlon = origin_point.iloc[0]['latlon']

    m = folium.Map(location=json.loads(origin_latlon), zoom_start=zoom)
    folium.Marker(json.loads(origin_latlon),popup="<i> Your Address: " + address_select + "</i>").add_to(m)

    for _, r in find_within_dist(coords,distance).iterrows():
        centerline = r['GBSID']
        scooters = round(make_prediction(centerline, month, year, day_of_week, day_of_year, hour, cn_bird, cn_lime, cn_lyft, cn_spin),0)
        folium.Marker(json.loads(r['latlon']),popup="<i> Expected Available: " + str(scooters) + "</i>",icon=folium.Icon(color='green')).add_to(m)

    return m

def main():
    if search_button:
        m = mapping()

        with result_container:
            st.header('Mapping Scooter Availability')
            st_data = st_folium(m, width = 725, returned_objects=[])

if __name__ == '__main__':
	main()
