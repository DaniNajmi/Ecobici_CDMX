import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import requests

# 1. SETUP & DATA FETCHING
st.set_page_config(layout="wide", page_title="EcoPulse CDMX")

@st.cache_data # This keeps the app fast by not re-downloading every click
def get_ecobici_data():
    # Fetching station information (Names, Lat, Lon)
    info_url = 'https://gbfs.mex.lyftbikes.com/gbfs/en/station_information.json'
    response = requests.get(info_url)
    data = response.json()
    df_info = pd.DataFrame(data['data']['stations'])
    
    # We only need these specific columns for your map logic
    return df_info[['station_id', 'name', 'lat', 'lon']]

try:
    df = get_ecobici_data()
except Exception as e:
    st.error("Could not connect to Ecobici API. Please check your internet connection.")
    st.stop()

# 2. ROW 1: HEADER
# Title and Caption as requested
st.title("EcoPulse CDMX 🚲🇲🇽: An interactive, real-time dashboard built to visualize and analyze Mexico City's Ecobici bike-sharing network.")
st.caption("Developed by Daniela Najmias Lang | Bioengineering & Systems Design")
st.markdown("---")

# 3. ROW 2: SIDEBAR & MAP
# Creating columns: col1 for the dropdown (left), col2 for the map (right)
col1, col2 = st.columns([1, 4]) 

with col1:
    st.write("### Search")
    # Dropdown menu using station_id column
    # We convert to int then sort so the list is numerical
    station_options = sorted(df['station_id'].astype(int).unique())
    station_number = st.selectbox(
        "Select Station ID to highlight:", 
        options=station_options
    )
    
    # Show station name for better UX
    selected_name = df[df['station_id'] == str(station_number)]['name'].values[0]
    st.info(f"**Station Name:**\n{selected_name}")

with col2:
    # Plotting logic adapted for Streamlit
    # We center the map on the average of all coordinates
    m = folium.Map(
        location=[df['lat'].mean(), df['lon'].mean()], 
        zoom_start=13, 
        tiles="cartodbpositron" # Cleaner look for urban maps
    )

    # Add all markers (The Red Icons)
    for n in range(len(df)):
        folium.Marker(
            location=[df['lat'].iloc[n], df['lon'].iloc[n]],
            tooltip=f"ID: {df['station_id'].iloc[n]}",
            icon=folium.Icon(color="red"),
        ).add_to(m)

    # The "Highlight" logic (The Cloud Icon)
    temp = df[df['station_id'] == str(station_number)]
    
    if not temp.empty:
        folium.Marker(
            location=[temp['lat'].values[0], temp['lon'].values[0]],
            tooltip=f"Selected: {temp['station_id'].values[0]}",
            icon=folium.Icon(icon="cloud", color="blue"), # Made it blue to stand out
        ).add_to(m)
    else:
        st.warning("Station not found in current API feed")

    # Display the map using st_folium
    st_folium(m, width=1200, height=600)
