#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: David Kloepper (kloe0021@umn.edu)
"""

import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
#import datetime
import json

#import geopandas as gpd

import pickle as pkl

import streamlit as st

from streamlit_folium import st_folium
import folium

from sklearn.neighbors import KNeighborsRegressor

st.set_page_config(
    page_title="Scooter Buddy",
    page_icon="🛴",
    layout="wide"
)

@st.cache(allow_output_mutation=True)

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

def get_coordinates(address, df):
    #Return the coordinates associated with address
    coordinates = df.loc[df['Display'] == address]
    return coordinates

def find_within_dist(coords,dist,df):
    #df = decompress_pickle_centerline('scooter_pickle.sav')
    df['distances'] = df.apply(lambda r: coords.distance(r['centroid'])  / 5279.98944, 
        axis=1)
    return df[(df['distances'] <= dist)]

def make_prediction(centerline, month, year, day_of_week, day_of_year, hour, cn_bird, cn_lime, cn_lyft, cn_spin):
  entry = pd.DataFrame([[centerline, month, year, day_of_week, day_of_year, hour, cn_bird, cn_lime, cn_lyft, cn_spin]], 
                 columns=["ClosestCenterlineID","month","year","day_of_week","day_of_year","hour","CompanyName_Bird","CompanyName_Lime","CompanyName_Lyft","CompanyName_Spin"])
  prediction = model.predict(entry)
  return prediction[0]


with st.sidebar:
    st.image('scooter.jpg')

st.title("Scooter Buddy")

st.markdown('''

Live or commute in Minneapolis? Ever wondered if there might be a foot scooter available nearby you?

Enter your address, select a data and time, a preferred brand to ride and how far you're willing to search, then let Scooter Buddy do the rest. 

''')

st.markdown("---")

left, right = st.columns(2)

with left:

    st.header('Enter your search criteria')

    address_list = pd.read_csv('Address_List.csv',header=0).squeeze("columns")

    input_form = st.form("input",clear_on_submit=False)

    with input_form:
        address_select = st.selectbox("Select your address",address_list)

        date_select = st.date_input("What day do you want to ride?")

        hour_select = st.selectbox("Pick time to ride",('12am-5am','6am-8am','9am-11am','12pm-2pm','3pm-5pm','6pm-8pm','9pm-11pm'))

        brand = st.radio("Select a preferred brand:",('Bird','Lime','Lyft','Spin'))

        distance = st.selectbox("Select a distance from you",(.1,.15,.2,.25,.3,.35,.4,.45,.5))

        search_button = st.form_submit_button('Find a scooter!')

with right:

    map_container = st.empty()

footer = st.container()

with footer:
    st.markdown("---")

def mapping(address_df,centerline_df):

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

    origin_point = get_coordinates(address_select, address_df)

    coords = origin_point.iloc[0]['geometry']
    origin_latlon = origin_point.iloc[0]['latlon']

    m = folium.Map(location=json.loads(origin_latlon), zoom_start=zoom)
    folium.Marker(json.loads(origin_latlon),popup="<i> Your Address: " + address_select + "</i>",icon=folium.Icon(color='blue')).add_to(m)

    for _, r in find_within_dist(coords,distance,centerline_df).iterrows():
        centerline = r['GBSID']
        scooters = round(make_prediction(centerline, month, year, day_of_week, day_of_year, hour, cn_bird, cn_lime, cn_lyft, cn_spin),0)
        if scooters >= 2:
            icon_color = 'green'
        elif 1 <= scooters < 2 :
            icon_color = 'gray'
        else:
            icon_color = 'red'
        folium.Marker(json.loads(r['latlon']),popup=r['LOCATION'],tooltip="<i> Expected Available: " + str(scooters) + "</i>",icon=folium.Icon(color=icon_color)).add_to(m)

    return m

def main():

    address_df = decompress_pickle_address('scooter_pickle.sav')
    centerline_df = decompress_pickle_centerline('scooter_pickle.sav')

    if search_button:
        with right:
            with st.spinner('Finding your ride...'):
                m = mapping(address_df,centerline_df)
                map_container.empty()
                with map_container.container():
                    st_data = st_folium(m, width = 650, height=650, returned_objects=[])


if __name__ == '__main__':
	main()
