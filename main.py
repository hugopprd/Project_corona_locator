# Geoscripting 2020 
# Title: Corona Locator
# Team: Baguette (Hugo Poupard & Jochem 't Hart)
# Final Project
# Date: 29-01-2021

import os
import sys
#os.chdir(sys.path[0]+r'/Project')
#print(os.getcwd())
import requests
import zipfile
import geopandas as gpd
import pandas as pd
import bar_chart_race as bcr
import functions as funcs
import imageio

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
#####gifmap

#bonus step
#create a gif that shows evolution of corona cases through a map
# Drop on-line courses
import os
import shutil
import time

import folium
import imageio
import webbrowser
import zipfile
import json
import fileinput

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from os import path
from branca.colormap import linear
#from selenium import webdriver
from PIL import Image
from pathlib import Path
# Keeping only 'CO_MUNICIPIO' and 'DT_INICIO_FUNCIONAMENTO'
last_date = MunCorGDF_ready.columns[-31]
MunCorGDF_gifmap = MunCorGDF_ready.loc[:, '2020-03-05': last_date]
MunCorGDF_gifmap = MunCorGDF_gifmap.join(MunCorGDF_ready.iloc[:, -1], rsuffix='j')
# Creating new var with foundation year for each course
# Checking nan values

sns.heatmap(MunCorGDF_gifmap.isnull(), 
            yticklabels=False, 
            cbar=False, 
            cmap='viridis'
           )

# Dropping nan values 

MunCorGDF_gifmap.dropna(inplace=True)

# Float to Int

MunCorGDF_gifmap = MunCorGDF_gifmap.astype(int)
MunCorGDF_gifmap_json = MunCorGDF_gifmap.to_json()

for i in range(1808,2019,10):
    
    # Gen a new df with total courses in each decade per municipality. This df is transformed into a dict
    total_perYear = courses[courses['FOUNDATION_YEAR'] <= i]
    total_perYear.drop('FOUNDATION_YEAR', axis=1, inplace=True)
    total_perYear['COUNT'] = 1
    total_perYear['CO_MUNICIPIO'] = total_perYear['CO_MUNICIPIO'].astype(str)   
    total_perYear = total_perYear.groupby('CO_MUNICIPIO')['COUNT'].sum()
    total_perYear = np.log(total_perYear) + 1
    total_perYear = total_perYear.to_dict()
    
    # Add municipalities keys with 0 courses at the giving year
    for j in cd_municipios:
        if j in  total_perYear.keys():
            continue
        else: 
             total_perYear[str(j)] = 0
    
    # Create a folium map centered in Brazil
    m_i = folium.Map(width=500, height=500,
               location=[-15.77972, -54.92972], 
               zoom_start=4,
               tiles='cartodbpositron')
    
    # Add year label to the map
    title_html = '''
                 <h3 align="left" style="font-size:22px"><b>{}</b></h3>
                 '''.format('Year: ' + str(i))   
    m_i.get_root().html.add_child(folium.Element(title_html))
    
    # Plot colors to the map using json geographical borders, and total courses from total_perYear dict
    folium.GeoJson(
        geo_json_data,
        style_function=lambda feature: {
            'fillColor': colormap(total_perYear[feature['properties']['id']]),
            'color': 'darkred',
            'weight': 0.5,
            'lineColor': 'white',
            'stroke' : False
        } 
    ).add_to(m_i)

    
    m_i.save('GifMap/total_perYear_' + str(i) + '.html')
    
    
# 8. City ranking 
# https://www.youtube.com/watch?v=qThD1InmsuI
# https://github.com/dexplo/bar_chart_race
df = corDF_normalized.join(MunCorGDF['GM_NAAM'])
df.set_index('GM_NAAM', inplace=True)
df = df.T
df = df.rename_axis(None,axis=1).rename_axis('date')
df = df.cumsum().astype(int)
df = df.iloc[:, :-1]

bcr.bar_chart_race(df=df,
                          filename='./output/bar_chart_race.mp4',
                          n_bars=10,
                          #steps_per_period=7,
                          #period_length=500,
                          interpolate_period=False)

'''
bcr.bar_chart_race(
    df=df,
    filename='./data/test.gif',
    orientation='h',
    sort='desc',
    n_bars=10,
    fixed_order=False,
    fixed_max=False,
    steps_per_period=10,
    interpolate_period=False,
    label_bars=True,
    bar_size=.95,
    period_label={'x': .99, 'y': .25, 'ha': 'right', 'va': 'center'},
    period_fmt='%B %d, %Y',
    period_length=500,
    figsize=(20, 20),
    dpi=144,
    cmap='dark12',
    title='COVID-19 Cases by Municipality',
    title_size='',
    bar_label_size=7,
    tick_label_size=7,
    shared_fontdict={'family' : 'Helvetica', 'color' : '.1'},
    scale='linear',
    writer=None,
    fig=None,
    bar_kwargs={'alpha': .7},
    filter_column_colors=False)  
'''
