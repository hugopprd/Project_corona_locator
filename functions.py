# Geoscripting 2020 
# Title: Corona Locator
# Team: Baguette (Hugo Poupard & Jochem 't Hart)
# Final Project
# Date: 29-01-2021

def CombineMunCbs (munGDF, cbsDF):
    import pandas as pd
    tempDF = cbsDF.groupby(['Municipality_code']).sum()
    tempDF['Municipality_code'] = tempDF.index
    tempDF.reset_index(drop=True, inplace=True)
    tempDF = pd.DataFrame(tempDF['Municipality_code'])

    days = cbsDF['Date_of_publication'].unique().tolist()

    for day in days:
        dayDF = cbsDF[cbsDF['Date_of_publication'] == day]
        dayDF = dayDF.rename(columns={'Total_reported': ''})
        dayDF.reset_index(drop=True, inplace=True)
        dayDF = dayDF['']
        tempDF = tempDF.join(dayDF, rsuffix=day)

    corDF = tempDF.drop(columns=[''])
    
    for day in days[7:]:
        index = days.index(day)
        corDF[day + '_sum'] = (corDF.iloc[:, index-7:index].sum(axis=1)) / 7
    
    return corDF
    
def DataPreProcessing(municipality_data, corona_data):
    import pandas as pd
    import geopandas as gpd
    # dropping water areas
    munGDF_upd = municipality_data[municipality_data["H2O"] == "NEE"]
    #join table
    mergedf = pd.merge(munGDF_upd, corona_data, left_on = 'GM_CODE', right_on = 'Municipality_code')
    #set index
    Preprocessed_data = mergedf.set_index(["GM_CODE"])
    MunCorGDF = gpd.GeoDataFrame(Preprocessed_data)
    #get rid of the useless columns
    MunCorGDF = MunCorGDF.drop(columns=['JRSTATCODE', 'H2O', 'OPP_WATER', 'OAD', 'STED', 'BEV_DICHTH'])
    #save file as csv
    MunCorGDF.to_csv(r'./data/coronapermun.csv')   
    return MunCorGDF

def Visualization(MunCorGDF_ready):
    import folium
    #create map
    coronamap = folium.Map([52.2130, 5.2794],
                 zoom_start=8,
                 tiles='cartodbpositron')
    # folium.TileLayer('openstreetmap',name="Light Map",control=False).add_to(coronamap)
    municipality_bord = MunCorGDF_ready.to_crs(epsg='4326')

    # get the name of the last updated
    last_date = MunCorGDF_ready.columns[-31]

    #setting a measurement scale and create a layer
    scale = (municipality_bord[last_date].quantile((0,0.25,0.75,1))).tolist()
    coronamap.choropleth(municipality_bord, data=municipality_bord,                      
                     columns=['GM_NAAM', last_date],
                     key_on='feature.properties.GM_NAAM', 
                     fill_color = 'YlOrRd',
                     threshold_scale=scale, 
                     fill_opacity=0.7,
                     line_opacity=0.2, legend_name='Percentage of corona cases')

    #create a highlight function
    style_function = lambda x: {'fillColor': '#ffffff', 
                            'color':'#000000', 
                            'fillOpacity': 0.1, 
                            'weight': 0.1}
    highlight_function = lambda x: {'fillColor': '#000000', 
                                'color':'#000000', 
                                'fillOpacity': 0.50, 
                                'weight': 0.1}
    NIL = folium.features.GeoJson(
            municipality_bord,
            style_function=style_function, 
            control=False,
            highlight_function=highlight_function, 
            tooltip=folium.features.GeoJsonTooltip(
                    fields=['GM_NAAM', last_date],
                    aliases=['Municipality: ', 'Percentage of corona cases per inhabitant in the last 24h'],
                    style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
                    )
            )

    coronamap.add_child(NIL)
    coronamap.keep_in_front(NIL)
    folium.LayerControl().add_to(coronamap)
    #save map
    coronamap.save('./output/CoronaMap.html')
    print('Map saved in output folder bro')