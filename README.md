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

### 2. Station-Level Intelligence
* **Deep Dive Analytics:** Select specific stations to view critical metadata, including exact coordinates, total capacity, and station name.
* **Availability Thresholds:** Visual indicators to distinguish between station information and live operational status.

### 3. Smart Filtering & Discovery
* **Inventory Management:** Identifies station capacities ranging from small local docks to large high-traffic hubs (e.g., 39+ bike capacity stations).
* **Neighborhood Precision:** Built to navigate the specific grid of CDMX, from Polanco to Coyoacán.


## Tech Stack & Data Logic
* **Framework:** [Streamlit](https://streamlit.io/) for the reactive UI.
* **Data Engine:** Pandas for processing complex nested JSON objects from live APIs.
* **Mapping:** Streamlit Map components for geospatial rendering.
* **API Integration:**
    * `station_information.json`: Physical metadata (Lat/Lon, Name, Capacity).
    * `station_status.json`: Live metrics (Available bikes, docks, operational status).
