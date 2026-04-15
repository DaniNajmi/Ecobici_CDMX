import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import requests

# 1. SETUP & DATA FETCHING
st.set_page_config(layout="wide", page_title="EcoPulse CDMX")

@st.cache_data(ttl=60) # Automatically refreshes data every 60 seconds
def get_ecobici_data():
    # A. Fetch Station Information (Static: Name, Lat, Lon)
    info_url = 'https://gbfs.mex.lyftbikes.com/gbfs/en/station_information.json'
    info_res = requests.get(info_url).json()
    df_info = pd.DataFrame(info_res['data']['stations'])
    
    # B. Fetch Station Status (Dynamic: Live Bikes/Docks)
    status_url = 'https://gbfs.mex.lyftbikes.com/gbfs/en/station_status.json'
    status_res = requests.get(status_url).json()
    df_status = pd.DataFrame(status_res['data']['stations'])
    
    # C. Merge both dataframes on 'station_id'
    # This gives us one master table with location + live counts
    df_merged = pd.merge(
        df_info[['station_id', 'name', 'lat', 'lon', 'capacity']], 
        df_status[['station_id', 'num_bikes_available', 'num_docks_available', 'is_installed']], 
        on='station_id'
    )
    return df_merged

try:
    df = get_ecobici_data()
except Exception as e:
    st.error("Could not connect to Ecobici API.")
    st.stop()

# 2. ROW 1: HEADER
st.title("EcoPulse CDMX 🚲🇲🇽")
st.markdown("#### Real-time analysis of Mexico City's bike-sharing network")
st.caption("Developed by Daniela Najmias Lang | Bioengineering & Systems Design")

# --- NEW ADDITION: KPI METRICS ---
# This calculates system-wide totals for the dashboard
total_bikes = df['num_bikes_available'].sum()
total_docks = df['num_docks_available'].sum()
# Percentage of docks currently filled with bikes
occupancy = (total_bikes / (total_bikes + total_docks)) * 100

m1, m2, m3 = st.columns(3)
m1.metric("Bikes Available Now", f"{total_bikes:,}")
m2.metric("Open Docks (Returns)", f"{total_docks:,}")
m3.metric("System Occupancy", f"{occupancy:.1f}%")

st.markdown("---")

# 3. ROW 2: SIDEBAR & MAP
col1, col2 = st.columns([1, 4]) 

with col1:
    st.write("### 🔍 Find a Station")
    search_query = st.text_input("Type a street name or neighborhood:", placeholder="e.g. Reforma")

    if search_query:
        filtered_df = df[df['name'].str.contains(search_query, case=False, na=False)]
    else:
        filtered_df = df

    if not filtered_df.empty:
        station_options = sorted(filtered_df['station_id'].astype(int).unique())
        station_number = st.selectbox(f"Results ({len(filtered_df)} found):", options=station_options)
        
        # 1. GET DATA FOR AUTO-ZOOM & ADDRESS
        selected_data = df[df['station_id'] == str(station_number)].iloc[0]
        
        st.info(f"**Selected Station:**\n{selected_data['name']}")
        
        # 2. SHOW THE "GO-TO" ADDRESS
        # Most GBFS feeds include a 'name' that is the intersection/address.
        st.success(f"📍 **Exact Location:**\n{selected_data['name']}")
        
        c1, c2 = st.columns(2)
        c1.write(f"🚲 Bikes: **{selected_data['num_bikes_available']}**")
        c2.write(f"🅿️ Docks: **{selected_data['num_docks_available']}**")
    else:
        st.error("No stations found.")
        station_number = df['station_id'].iloc[0]

    st.markdown("---")
    st.subheader("📖 Quick Dashboard Guide")
    
    with st.expander("How to read this app", expanded=True):
        st.write("**Top Metrics:**")
        st.write("- **Bikes:** Total units ready to unlock.")
        st.write("- **Docks:** Total spaces to return a bike.")
        st.write("- **Occupancy:** System-wide usage level.")
        
        st.write("**Map Colors:**")
        st.success("🟢 **High:** > 5 bikes")
        st.warning("🟠 **Low:** 1-5 bikes")
        st.error("🔴 **Empty:** 0 bikes / Inactive")
        st.info("☁️ **Blue Cloud:** Selected Station")
        
        st.caption("Data refreshes automatically every 60 seconds.")

with col2:
    # 3. AUTO-ZOOM LOGIC
    # If a station is selected, we center the map on its specific lat/lon
    # We also increase the zoom level from 13 to 16 for a "street view" feel
    target_station = df[df['station_id'] == str(station_number)].iloc[0]
    
    m = folium.Map(
        location=[target_station['lat'], target_station['lon']], 
        zoom_start=16, # Deeper zoom for navigation
        tiles="cartodbpositron"
    )

    # Add all markers (Standard Traffic Lights)
    for n in range(len(df)):
        bikes = df['num_bikes_available'].iloc[n]
        icon_color = "green" if bikes > 5 else "orange" if bikes > 0 else "red"
        
        folium.Marker(
            location=[df['lat'].iloc[n], df['lon'].iloc[n]],
            tooltip=f"ID {df['station_id'].iloc[n]}",
            icon=folium.Icon(color=icon_color),
        ).add_to(m)

    # The Selection Highlight (Cloud)
    folium.Marker(
        location=[target_station['lat'], target_station['lon']],
        popup=f"YOU ARE HERE: {target_station['name']}",
        icon=folium.Icon(icon="cloud", color="blue", icon_color="white"),
    ).add_to(m)

    st_folium(m, width=1200, height=600, key="ecobici_map")

    # Highlight the selected station with a Blue Cloud
    temp = df[df['station_id'] == str(station_number)]
    if not temp.empty:
        folium.Marker(
            location=[temp['lat'].values[0], temp['lon'].values[0]],
            popup=f"Selected Station: {temp['name'].values[0]}",
            icon=folium.Icon(icon="cloud", color="blue"),
        ).add_to(m)

    # Render
    st_folium(m, width=1200, height=600)
