# Geoscripting 2020 
# Title: Corona Locator
# Team: Baguette (Hugo Poupard & Jochem 't Hart)
# Final Project
# Date: 29-01-2021

import os
import requests
import zipfile
import geopandas as gpd
import pandas as pd
import numpy as np

# 1. create folders
if not os.path.exists('data'): os.mkdir('data')
if not os.path.exists('output'): os.mkdir('output')

# 2. Download RIVM csv and municipalities with population
url_cbs = 'https://www.cbs.nl/-/media/cbs/dossiers/nederland-regionaal/wijk-en-buurtstatistieken/wijkbuurtkaart_2020_v1.zip'
url_rivm = 'https://data.rivm.nl/covid-19/COVID-19_aantallen_gemeente_per_dag.csv'

path_cbs_zip = './data/municipality.zip'
mun_loc = './data/gemeente_2020_v1.shp'
cbs_loc = './data/corona.csv'

if not os.path.exists(path_cbs_zip):
    with requests.get(url_cbs)as r:
        print('Downloading...')
        open(path_cbs_zip, 'wb').write(r.content)
        with zipfile.ZipFile(path_cbs_zip, 'r') as z:
            z.extractall('./data/')

with requests.get(url_rivm) as r:
    open(cbs_loc, 'wb').write(r.content)  
    
from functions import DataPreProcessing

#calling function DataPreProcessing function and store it in a variable
data = DataPreProcessing(mun_loc, cbs_loc)

# 4. Calculate average cases/deaths for the last week for each day. (csv)
#for mun in municipalities:
    
#for day in days[7:]:

# 5. Add csv coronacases to municipality geo-data
        
# 6. normalize coronacases for inhabitants

# 7. Rasterize and animate

# 8. City ranking 
# https://www.youtube.com/watch?v=qThD1InmsuI
# https://github.com/dexplo/bar_chart_race