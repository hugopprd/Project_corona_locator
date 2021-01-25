# Geoscripting 2020 
# Title: Corona Locator
# Team: Baguette (Hugo Poupard & Jochem 't Hart)
# Final Project
# Date: 29-01-2021



def DataPreProcessing(municipality_data, corona_data):
    import geopandas as gpd
    import pandas as pd
    # dropping water areas
    munGDF_upd = municipality_data[municipality_data["H2O"] == "NEE"]

    #join table
    mergedf = pd.merge(munGDF_upd, corona_data, left_on = 'GM_CODE', right_on = 'Municipality_code')

    #set index
    Preprocessed_data = mergedf.set_index(["GM_CODE"])

    #save file as csv
    Preprocessed_data.to_csv(r'./data/coronapermun.csv')   
    return Preprocessed_data
