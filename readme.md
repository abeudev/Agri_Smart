<img width="500" src="docs/logo_wide">

# Agriculture 

:warning: :construction: This project is still under development.

| Feature  | Status |
| ------------- | ------------- |
| Field Management  | :x: |
| Satellite images  | :construction:  |
| Field Logbook| :x: |
| Warehouse management | :x: |
| Weather Data | :x: |

## Introduction

Agriculture is an open-source decision-support system for precision farming.
This application is thought to be self-hosted using a low-power SBC (e.g., Raspberry Pi 3, Pine A64) and accessed within a local network.


## Remote Sensing  :satellite:

Modern precision farming makes heavy use of satellite imagery in order to extract meaningful information on crops and monitor their status. Within the available satellite, the ESA (European Space Agency) Sentinel-2 mission is particularly suitable for monitoring land surface variations at a spatial scale compatible with precision farming (from 10 m to 30 m depending on the band).
Agriculture uses Sentinel-2 images and processes them in order to provide vegetation indexes maps clipped over user field footprints.

<img width="720" src="docs/field_details.png">

### Supported Multi-Spectra-Instrument Indexes :seedling:

There are different wide-band indexes that can be extracted from Sentinel-2 images (for an exhaustive list, see [Index Database](https://www.indexdatabase.de/db/is.php?sensor_id=96) ). 

Other indexes will be added in future

| Index  | Aim | Status |
| ------------- | ------------- |------------- |
| Normalized Difference Vegetation Index (NDVI) | Photosynthetic activity  | :heavy_check_mark: |
| Normalized Multi-band Drought Index (NDMI) | Water Content | :x: |

## Weather Data

:warning: :construction: Not yet available.

## Warehouse

:warning: :construction: Not yet available.

## Field Logbook

:warning: :construction: Not yet available.



