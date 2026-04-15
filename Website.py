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
    st.write("### 🔍 Search")
    station_options = sorted(df['station_id'].astype(int).unique())
    station_number = st.selectbox("Select Station ID:", options=station_options)
    
    # Pull details for the selected station
    selected_data = df[df['station_id'] == str(station_number)].iloc[0]
    
    st.info(f"**Station:** {selected_data['name']}")
    
    # Show specific live stats for this station in the sidebar
    c1, c2 = st.columns(2)
    c1.write(f"🚲 Bikes: **{selected_data['num_bikes_available']}**")
    c2.write(f"🅿️ Docks: **{selected_data['num_docks_available']}**")

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
    # Initialize Map
    m = folium.Map(
        location=[df['lat'].mean(), df['lon'].mean()], 
        zoom_start=13, 
        tiles="cartodbpositron" 
    )

    # --- UPDATED: TRAFFIC LIGHT MARKERS ---
    for n in range(len(df)):
        bikes = df['num_bikes_available'].iloc[n]
        
        # Color Logic: Green if plenty, Orange if low, Red if empty
        if bikes > 5:
            icon_color = "green"
        elif bikes > 0:
            icon_color = "orange"
        else:
            icon_color = "red"
            
        folium.Marker(
            location=[df['lat'].iloc[n], df['lon'].iloc[n]],
            tooltip=f"ID {df['station_id'].iloc[n]}: {bikes} bikes",
            icon=folium.Icon(color=icon_color),
        ).add_to(m)

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
