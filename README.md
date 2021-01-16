# Geoscripting project repository.
Geoscripting 2020 
- Title: Corona Locator
- Team: Baguette (Hugo Poupard & Jochem 't Hart)
- Date: 15-01-2021

## Objective
Our objective is to create a map which shows where corona cases are situated for the last week. The visualization of these cases is currently only available per municipality, but we want to show these cases on a smaller grid (100mx100m) based on population numbers. This way, when you want to travel to Amsterdam, you can check how many cases there are in the part of Amsterdam where you are going.

## Datasets
**Corona cases table**
- Link: https://data.rivm.nl/geonetwork/srv/dut/catalog.search#/metadata/5f6bc429-1596-490e-8618-1ed8fd768427?tab=relations
- Metadata: data is made by RIVM and is updated every day. The data gives new corona cases for each day per municipality for the entirety of the Netherlands.
- File download link: https://data.rivm.nl/covid-19/COVID-19_aantallen_gemeente_per_dag.csv

**Municipality shapefile**
- File location: sf::getData GADM library
- Metadata: this file contains the municipality boundaries.

**World population raster**
- Link: https://www.worldpop.org/geodata/summary?id=49840
- Metadata: the data is made by worldpop.org. It is a raster of 3 arc seconds resolution (100x100m at equator) with the number of people per gridcell.
- File download link: https://data.worldpop.org/GIS/Population/Global_2000_2020_Constrained/2020/BSGM/NLD/nld_ppp_2020_constrained.tif

## Method
**Packages**
- raster
- sf

**Steps**
- create folders (data, output)
- download data and store in datafolder
- transform data to be in the same crs (RD New)
- get average cases for last week as cases for today (too much difference in number of cases because of weekends etc.)
- combine corona cases table with municipality shapefile
- visualize cases per municipality as intermediate output (specify risk categories, threshold)
- create empty 100x100m grid (points)
- zonal to get world population statistics to grid
- join by location to get municipality code and number of cases per municipality to grid
- multiply number of cases per municipality with relative number of inhabitants for gridcell compared to municipality
- rasterize and visualize
