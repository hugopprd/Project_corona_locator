# Geoscripting project repository.
Geoscripting 2020 
- Title: Corona Locator
- Team: Baguette (Hugo Poupard & Jochem 't Hart)
- Date: 15-01-2021

## Objective
Showing the development of relative coronacases per inhabitant (normalization) in the Netherlands. Visualize it per city and apply some statistics to show interesting corona development trends. Do something like a city-ranking system.

## Datasets
**Corona cases table**
- Link: https://data.rivm.nl/geonetwork/srv/dut/catalog.search#/metadata/5f6bc429-1596-490e-8618-1ed8fd768427?tab=relations
- Metadata: data is made by RIVM and is updated every day. The data gives new corona cases for each day per municipality for the entirety of the Netherlands.
- File download link: https://data.rivm.nl/covid-19/COVID-19_aantallen_gemeente_per_dag.csv

**Municipality shapefile**
- File location: sf::getData GADM library
- Metadata: this file contains the municipality boundaries.

## Method
**Packages**


**Steps**
- create folders (data, output)
- download data and store in datafolder
- transform data to be in the same crs (RD New)
- calculate average coronacases/death for the last week per day.
- add coronacase data to shapefile (~300 columns of each day corona cases)
- add corona death data to shapefile as a seperate file (no priority)
- normalize cases for inhabitants
- visualization
- animation from march to now in a raster
- graph from march to now
- city ranking animation.
