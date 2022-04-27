import json, requests
from urllib.request import urlopen
import streamlit as st
import pandas as pd

# input parameters
lat = st.sidebar.slider(
    'Latitude:',
    -90.0, 90.0, (30.26)
) 
long = st.sidebar.slider(
    'Longitude',
    -180.0, 180.0, (-97.74)
) 

size = st.sidebar.slider(
    'Size of PV array:',
    0.0, 100.0, (50.0)
)

# url generator
nrel_api_key = 'kVTh5O88nbYohgldbB92JC17TL4UzxwauQo1x2Ha'

url = 'https://developer.nrel.gov/api/pvwatts/v6.json?api_key=%s&lat=%s&lon=%s&system_capacity=%s&azimuth=180&tilt=40&array_type=1&module_type=1&losses=10' % (nrel_api_key, lat, long, size)

## add catch for bad locations
if(requests.get(url).status_code == 200):

    response = urlopen(url)
    pv_out = json.loads(response.read())

    location = pv_out['station_info']['state']
    gen = round(pv_out['outputs']['ac_annual'])

    st.write('A %s kW solar PV array in %s should output about %s kWh per year!' % (size, location, gen))
    
else:
    st.write('You appear to have chosen a location without data! Maybe try again?')

# plot the location data on a map!
map_data = pd.DataFrame(data={'lat': float(lat), 'lon': float(long)}, index=[0])
st.map(map_data)