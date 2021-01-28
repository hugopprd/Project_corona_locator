# Geoscripting 2020 
# Title: Corona Locator
# Team: Baguette (Hugo Poupard & Jochem 't Hart)
# Final Project
# Date: 29-01-2021

import os
import sys
# =============================================================================
# os.chdir(sys.path[0]+r'/Project')
# print(os.getcwd())
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






def gif(MunCorGDF_normalized, date):
    import folium
# =============================================================================
   # import selenium
    from selenium import webdriver
#     import time
# =============================================================================
    import io
    from PIL import Image

#     driver = webdriver.Firefox(executable_path='./geckodriver-0.29.0')
#     driver.get('http://inventwithpython.com')
    #create map
    coronamap = folium.Map([52.2130, 5.2794],
                 zoom_start=8,
                 tiles='cartodbpositron')
    # folium.TileLayer('openstreetmap',name="Light Map",control=False).add_to(coronamap)
    municipality_bord = MunCorGDF_normalized.to_crs(epsg='4326')

    # get the name of the last updated

    #setting a measurement scale and create a layer
    scale = (municipality_bord[date].quantile((0,0.25,0.75,1))).tolist()
    coronamap.choropleth(municipality_bord, data=municipality_bord,                      
                     columns=['GM_NAAM', date],
                     key_on='feature.properties.GM_NAAM', 
                     fill_color = 'YlOrRd',
                     threshold_scale=scale, 
                     fill_opacity=0.7,
                     line_opacity=0.2, legend_name='Number of new corona cases per 100.000 in the last 24h')

    folium.LayerControl().add_to(coronamap)
    #save map / From here I need to save as html and then make a screenshot of the map 
    map_output_html = './output/'+str(date)+'.html'
    map_output_png = './output/'+str(date)+'.png'
    #save as html
    coronamap.save(map_output_html)
    #code that didnt work because of that error ->  WebDriverException: 'geckodriver' executable needs to be in PATH. 
# =============================================================================
    img_data = coronamap._to_png(5)
    img = Image.open(io.BytesIO(img_data))
    img.save(map_output_png)
# =============================================================================
# other code which work but png file is white because I need to add some delay 
# for the browser to open and display the map before it makes the screenshot and that I don't know how to do
# =============================================================================
#     import os
#     import subprocess
#     import time
#     url = "file://{}/"+str(map_output_html).format(os.getcwd())
#     outfn = os.path.join(map_output_png)
#     subprocess.check_call(["cutycapt","--url={}".format(url), "--out={}".format(outfn)])
# =============================================================================
    os.remove('./output/'+ str(date) + '.html')

    print('Map ' + date + ' saved in output folder bro')

def CoronaGif(MunCorGDF_normalized):
    col_nb = len(MunCorGDF_normalized.columns[30:])
    for i in range(col_nb):
        #select each column one by one
        date = MunCorGDF_normalized.columns[30+i]
        #launch function that creates maps and store them as png
        gif(MunCorGDF_normalized, date)
        print('finished with map '+ str(date))
    
CoronaGif(MunCorGDF_normalized)
    
    
    

    #count how many columns with '2020-...-...
# 8. City ranking 
# https://www.youtube.com/watch?v=qThD1InmsuI
# https://github.com/dexplo/bar_chart_race
funcs.MakeBarChart(corDF_normalized, MunCorGDF)
