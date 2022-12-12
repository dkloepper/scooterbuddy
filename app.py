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

from IPython.display import display
from ipywidgets import embed
import streamlit.components.v1 as components
import streamlit as st

from streamlit_folium import st_folium
import folium


filename = 'scooter_pickle.sav'
with open(filename, 'rb') as fIn:
    scooter_pkl = pkl.load(fIn)

model = scooter_pkl['model']
address_df = scooter_pkl['addresses']
centerline_df = scooter_pkl['centerlines']

month = 12
year = 2022
day_of_week = 2
day_of_year = 345
hour = 17
cn_bird = 0
cn_lime = 0
cn_lyft = 1
cn_spin = 0

body_container = st.container()
result_container = st.container()
form_sidebar = st.sidebar()

with form_sidebar:
    address_select = st.selectbox("Select your address",address_df['Display'],index=1) 

    date_select = st.date_input("What day do you want to ride?")
    hour_select = st.selectbox("Pick an hour range",('12-5','6-9','10-12','1-3','4-6','7-9','10-12'))
    brand = st.radio("Select a preferred brand:",('Bird','Lime','Lyft','Spin'))

    if brand == 'Bird':
        cn_bird = 1
        cn_lime = 0
        cn_lyft = 0
        cn_spin = 0

    if brand == 'Lime':
        cn_bird = 0
        cn_lime = 1
        cn_lyft = 0
        cn_spin = 0

    if brand == 'Lyft':
        cn_bird = 0
        cn_lime = 0
        cn_lyft = 1
        cn_spin = 0

    if brand == 'Spin':
        cn_bird = 0
        cn_lime = 0
        cn_lyft = 0
        cn_spin = 1

    #bird_check = st.checkbox("Bird", value=False)
    #lime_check = st.checkbox("Lime", value=False)
    #lyft_check = st.checkbox("Lyft", value=False)
    #spin_check = st.checkbox("Spin", value=False)
    distance = st.selectbox("Select a distance from you",(.1,.15,.2,.25,.3,.35,.4,.45,.5,.75,1))
    search_button = st.button('Find a scooter!')

with body_container:
    st.title("Scooter Buddy")
    st.markdown("""---""")
    #query = st.text_input("Describe your perfect hotel in Athens:", "walking distance to acropolis, clean rooms, pool")
    #search_button = st.button('Find a hotel')

@st.cache(persist=True)


def get_coordinates(address):
    #Return the coordinates associated with address
    coordinates = address_df.loc[address_df['Display'] == address]
    return coordinates

def find_within_dist(coords,df,dist):
    df['distances'] = df.apply(lambda r: coords.distance(r['centroid'])  / 5279.98944, 
        axis=1)
    return df[(df['distances'] <= dist)]

def make_prediction(centerline, month, year, day_of_week, day_of_year, hour, cn_bird, cn_lime, cn_lyft, cn_spin):
  entry = pd.DataFrame([[centerline, month, year, day_of_week, day_of_year, hour, cn_bird, cn_lime, cn_lyft, cn_spin]], 
                 columns=["ClosestCenterlineID","month","year","day_of_week","day_of_year","hour","CompanyName_Bird","CompanyName_Lime","CompanyName_Lyft","CompanyName_Spin"])
  prediction = model.predict(entry)
  return prediction[0]

def run():

    origin_point = get_coordinates(address_select)

    print(origin_point)

    coords = origin_point['geometry']
    origin_latlon = origin_point['latlon']
    origin_address = origin_point['Display']

    m = folium.Map(location=json.loads(origin_latlon), zoom_start=18)
    folium.Marker(json.loads(origin_latlon),popup="<i> Your Address: " + origin_address + "</i>").add_to(m)

    for _, r in find_within_dist(coords,centerline_df,distance).iterrows():
        centerline = r['GBSID']
        scooters = round(make_prediction(centerline, month, year, day_of_week, day_of_year, hour, cn_bird, cn_lime, cn_lyft, cn_spin),0)
        folium.Marker(json.loads(r['latlon']),popup="<i> Expected Available: " + str(scooters) + "</i>",icon=folium.Icon(color='green')).add_to(m)

    with result_container:
    
        st.header('Mapping Scooter Availability')

        st_data = st_folium(m, width = 725)


if search_button:
    run()
