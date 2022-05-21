<img width="500" src="docs/logo_wide">

# Open Agriculture 

Open Agriculture is an open-source decision-support system for precision farming.

<img width="720" src="docs/dashboard.png">

## Remote Sensing

Open Agriculture integrates a module for the extraction of different vegetation index from Sentinel-2 satellite images taken with a multispectral instrument.

<img width="720" src="docs/field_details.png">

Current supported Multispectra index

| Index  | Aim | Status |
| ------------- | ------------- |------------- |
| Normalized Difference Vegetation Index (NDVI) | Photosynthetic activity  | :heavy_check_mark: |
| Normalized Multi-band Drought Index (NDMI) | Water Content | :x: |

## Architecture

Application backend it is written in Pytho3 using Flask, while the front-end is built using Bootstrap5 and Leaflet.js for spatial data handling.

## Current status

:warning: :construction: The project is still under development.


| Feature  | Status |
| ------------- | ------------- |
| Field Management  | :x: |
| Satellite images  | :heavy_check_mark:  |
| Field Logbook| :x: |
| Warehouse management | :x: |
| Weather Data | :x: |
