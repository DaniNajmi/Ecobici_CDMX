# Ecobici Live Tracker: CDMX
## Daniela Najmias Lang

### Real-Time Micro-Mobility Analytics Dashboard

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B.svg)](https://streamlit.io/)
[![Data Source](https://img.shields.io/badge/Data-GBFS%20CDMX-orange.svg)](https://gbfs.mex.lyftbikes.com/gbfs/gbfs.json)

An interactive, real-time dashboard built to visualize and analyze Mexico City's Ecobici bike-sharing network. This tool transforms official GBFS (General Bikeshare Feed Specification) live feeds into actionable geospatial insights.


## Strategic Features

### 1. Live Network Visualization
* **Dynamic Mapping:** View the entire network of 670+ active stations across CDMX.
* **Real-Time Synchronization:** Connects directly to the `gbfs.json` auto-discovery endpoint to ensure data accuracy.
* The network is visualized through a dynamic color-coded system to show station health at a glance:
* **Green Pins:** High availability (>5 bikes).
* **Orange Pins:** Low availability (1-5 bikes) — move fast!
* **Red Pins:** Empty or inactive stations.

### 2. Station-Level Intelligence
* **Deep Dive Analytics:** Select specific stations to view critical metadata, including exact coordinates, total capacity, and station name.
* **Availability Thresholds:** Visual indicators to distinguish between station information and live operational status.

### 3. Smart Filtering & Discovery
* **Inventory Management:** Identifies station capacities ranging from small local docks to large high-traffic hubs (e.g., 39+ bike capacity stations).
* **Neighborhood Precision:** Built to navigate the specific grid of CDMX, from Polanco to Coyoacán.

### 4. Intuitive Smart Search & Auto-Zoom
Designed for real-world utility, users can search for stations by **Street Name** or **Neighborhood** (e.g., "Reforma" or "Roma"). 
* **Dynamic Filtering:** The system instantly narrows down 670+ stations based on your keyword.
* **Precision Focus:** Upon selection, the map automatically zooms into a street-level view (Level 16) to help you locate the exact dock.

### 5. "Last-Mile" Navigation
Once a station is selected, the app provides a direct handshake with **Google Maps**. With one click, users can launch GPS navigation directly to the station’s coordinates, ensuring a frictionless transition from digital insight to physical travel.

---

## 📊 System Vitality Metrics (KPIs)
The dashboard provides a "Pulse Check" of the entire CDMX network:
* **Live Bike Count:** Total units currently available for unlock.
* **Return Capacity:** Real-time monitoring of open docks for bike returns.
* **System Occupancy:** A percentage-based view of current network utilization.

---

## 🛠️ Technical Architecture
This application utilizes a sophisticated data pipeline to ensure accuracy:
1. **API Integration:** Connects to official GBFS endpoints for station metadata and live status.
2. **Data Merging:** Uses Pandas to join disparate JSON feeds into a single source of truth.
3. **Reactive UI:** Built with Streamlit and Folium to provide a responsive, state-managed experience.

## Tech Stack & Data Logic
* **Framework:** [Streamlit](https://streamlit.io/) for the reactive UI.
* **Data Engine:** Pandas for processing complex nested JSON objects from live APIs.
* **Mapping:** Streamlit Map components for geospatial rendering.
* **API Integration:**
    * `station_information.json`: Physical metadata (Lat/Lon, Name, Capacity).
    * `station_status.json`: Live metrics (Available bikes, docks, operational status).
