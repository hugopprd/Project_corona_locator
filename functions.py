# Geoscripting 2020 
# Title: Corona Locator
# Team: Baguette (Hugo Poupard & Jochem 't Hart)
# Final Project
# Date: 29-01-2021

def CombineMunCbs (munGDF, cbsDF):
    print('Calculating new Corona cases per day per municipality...')
    # Get a DF of all municipality codes as a base to add other dataframes to
    tempDF = cbsDF.groupby(['Municipality_code']).sum()
    # Make municipality codes as index
    tempDF['Municipality_code'] = tempDF.index
    tempDF = tempDF.drop(columns=['Total_reported', 'Hospital_admission', 'Deceased'])
    
    # Create a list of unique days to loop through
    days = cbsDF['Date_of_publication'].unique().tolist()
    
    # Loop through each day and get the new coronacases from that date and add it to a new column in the municipality dataframe
    for day in days:
        # Get the cases for each municipality on this day
        dayDF = cbsDF[cbsDF['Date_of_publication'] == day]
        # Make municipality code the index to use for join later on.
        dayDF.set_index('Municipality_code', inplace=True)
        # Take the sum of cases if a municipality code is mentioned twice on each day
        dayDF = dayDF.groupby(dayDF.index).sum()
        dayDF = dayDF.rename(columns={'Total_reported': ''})
        dayDF = dayDF['']
        # Join cases per municipality to the big dataset
        tempDF = tempDF.join(dayDF, rsuffix=day)

    corDF = tempDF.drop(columns=[''])
    
    # Take the average of the sum of the last 7 days. This way, there won't be large spikes after the weekend or low numbers during the weekends.
    for day in days[7:]:
        index = days.index(day)
        corDF[day + '_sum'] = (corDF.iloc[:, index-7:index].sum(axis=1)) / 7
        
    corDF = corDF.drop(columns=['Municipality_code'])
    corDF = corDF.loc[:,'2020-03-05_sum':]
    # Change column name
    corDF.columns = corDF.columns.str.replace('_sum','')
    
    return corDF
    

def DataPreProcessing(municipality_data, corona_data):
    import pandas as pd
    import geopandas as gpd
    print('Adding corona data to municipality GeoDataFrame...')
    
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


def Visualization(MunCorGDF_normalized):
    import folium
    print('Creating Folium map...')
    
    #create map
    coronamap = folium.Map([52.2130, 5.2794],
                 zoom_start=8,
                 tiles='cartodbpositron')
    # folium.TileLayer('openstreetmap',name="Light Map",control=False).add_to(coronamap)
    municipality_bord = MunCorGDF_normalized.to_crs(epsg='4326')

    # get the name of the last updated
    last_date = MunCorGDF_normalized.columns[-1]

    #setting a measurement scale and create a layer
    scale = (municipality_bord[last_date].quantile((0,0.25,0.75,1))).tolist()
    coronamap.choropleth(municipality_bord, data=municipality_bord,                      
                     columns=['GM_NAAM', last_date],
                     key_on='feature.properties.GM_NAAM', 
                     fill_color = 'YlOrRd',
                     threshold_scale=scale, 
                     fill_opacity=0.7,
                     line_opacity=0.2, legend_name='Percentage of population infected with COVID-19 today')

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
                  fields=['GM_NAAM', 
                            last_date, 
                            'P_00_14_JR', 
                            'P_15_24_JR', 
                            'P_25_44_JR',  
                            'P_45_64_JR', 
                            'P_65_EO_JR'],
                    aliases=['Municipality: ', 
                             'Percentage of population infected with COVID-19 today', 
                             '% of 0yo to 14yo', 
                             '% of 15yo to 24yo', 
                             '% of 25yo to 44yo', 
                             '% of 45yo to 64yo', 
                             '% of 65yo and plus'],
                    style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
                    )
            )

    coronamap.add_child(NIL)
    coronamap.keep_in_front(NIL)
    folium.LayerControl().add_to(coronamap)
    #save map
    coronamap.save('./output/CoronaMap.html')
    print('Map saved in output folder bro')
   
    
def Plotgif(MunCorGDF_normalized, date, index):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, figsize=(6, 10))
    MunCorGDF_normalized.plot(column=date, k=4, cmap='YlOrRd', ax=ax)
    ax.set_title(date, fontdict={'fontsize': '25', 'fontweight' : '3'})
    ax.set_axis_off()
    plt.savefig('data/png/'+str(index)+'.png')
    plt.close()
    fig.clf()



def CoronaGif(MunCorGDF_normalized):
    import imageio
    import glob
    print("Creating PNG's of corona cases throughout the Netherlands from March to today...")
    
    for index, col_nb in enumerate(MunCorGDF_normalized.columns[30:]):
        #select each column one by one
        date = col_nb
        #launch function that creates maps and store them as png
        Plotgif(MunCorGDF_normalized, date, index)
        print('finished with map '+ str(date))
        
    print('Creating GIF...')
    out_gif = './output/CoronaGif.gif'
    images = []
    filenames = glob.glob('./data/png/*.png')
    filenames.sort(key = lambda f: int(f[11:-4])) 
    for filename in filenames:
        images.append(imageio.imread(filename))
    try:
        imageio.mimsave(out_gif, images, duration=0.2)
    except:
        print('No images to convert')
    
    
def MakeBarChart(corDF_poht, MunCorGDF):
    import bar_chart_race as bcr
    print('Creating Bar Chart Race. This may take 5 Minutes...')
    # Get the municipality names
    df = corDF_poht.join(MunCorGDF['GM_NAAM'])
    # Use municipality name as index instead of municipality code
    df.set_index('GM_NAAM', inplace=True)
    # Transform to get a wide dataset instead of long
    df = df.T
    df = df.rename_axis(None,axis=1).rename_axis('date')
    # Convert to int, because the bar_char_race function takes int and not float. Also change data to cumulative instead of new cases.
    df = df.cumsum().astype(int)
    df = df.iloc[:, :-1]
    
    # Create bar chart race
    bcr.bar_chart_race(df=df,
                          filename='./output/bar_chart_race.mp4',
                          n_bars=20,
                          interpolate_period=False,
                          title='Number of People per 10.000 That Have Been Infected With COVID-19'
                          )
    
