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
