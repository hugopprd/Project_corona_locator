# Geoscripting 2020 
# Title: Corona Locator
# Team: Baguette (Hugo Poupard & Jochem 't Hart)
# Final Project
# Date: 29-01-2021

import os
import sys
# =============================================================================
# =============================================================================
#os.chdir(sys.path[0]+r'/Project_Starter-Baguette-master/')
#  print(os.getcwd())
# =============================================================================
# =============================================================================
import requests
import zipfile
import geopandas as gpd
import pandas as pd
import functions as funcs

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

# 3. load municipalities as GeoDataFrame
munGDF = gpd.read_file(mun_loc)
cbsDF = pd.read_csv(cbs_loc, sep=';')

# 4. Calculate average cases/deaths for the last week for each day. (csv)
corDF = funcs.CombineMunCbs(munGDF, cbsDF)

# 5. Add csv coronacases to municipality geo-data using DataPreProcessing
MunCorGDF = funcs.DataPreProcessing(munGDF, corDF)
        
# 6. normalize coronacases for inhabitants
corDF_normalized = MunCorGDF.loc[:, '2020-03-05':].div(MunCorGDF['AANT_INW'], axis=0) * 100000

# 7. Visualize
#add the usefull data to table
MunCorGDF_normalized = MunCorGDF.loc[:, :'geometry'].join(corDF_normalized)
funcs.Visualization(MunCorGDF_normalized)

#creating a gif
funcs.CoronaGif(MunCorGDF_normalized)

    
# =============================================================================
    

    #count how many columns with '2020-...-...
# 8. City ranking 
# https://www.youtube.com/watch?v=qThD1InmsuI
# https://github.com/dexplo/bar_chart_race
funcs.MakeBarChart(corDF_normalized, MunCorGDF)
