import pandas as pd
import pycountry_convert as pc

'''
Takes in a dataframe and adds a column that contains continent codes to it
Continent codes are two-letter strings that stand for the following:
    'AS' = Asia
    'NA' = North America
    'AF' = Africa
    'OC' = Oceania
    'EU' = Europe
    'SA' = South America
'''
def add_continent_col(df):
    # converting 3 letter country codes to 2 letter ones...
    df['SpatialDimValueCode'] = df['SpatialDimValueCode'].apply(lambda x: pc.country_alpha3_to_country_alpha2(x))
    df.insert(len(df.columns), 'Continent', 0) # adding 'Continent' col as the last col of the dataframe

    # updating new 'tl' alpha2 value to the outdated 'tp' one to make it compatible with pycountry
    df['SpatialDimValueCode'] = df['SpatialDimValueCode'].apply(lambda x: 'TP' if x == 'TL' else x)

    # adding continent codes to 'Continent' col
    df['Continent'] = df['SpatialDimValueCode'].apply(lambda x: pc.country_alpha2_to_continent_code(x))
    return df
