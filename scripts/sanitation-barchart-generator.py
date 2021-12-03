import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go
import data_cleaner as dc
import numpy as np
import pycountry_convert as pc

# generates a barchart graph of sanitation data for each continent given
def generate_graphs(continent, path):
    df = pd.read_csv('../Datasets/PopulationUsingSafelyManagedSanitationServices.csv')

    # adding continent ids to the dataframe
    cont_df = dc.add_continent_col(df)

    # making sure it only has data for the current continent
    cont_df = cont_df[cont_df['Continent'] == continent]

    # limiting data to 2020
    cont_df = cont_df[cont_df['Period'] == 2020]

    # getting rid of empty spaces
    cont_df.replace('', np.nan, inplace=True)
    cont_df.dropna(subset=['FactValueNumeric'], inplace=True)

    # only including total proportion
    cont_df = cont_df[cont_df['Dim1ValueCode'] == 'TOTL']

    # replacing long country names with their alpha2 codes
    cont_df['Location'] = cont_df['SpatialDimValueCode'].apply(lambda x: pc.country_alpha2_to_country_name(x) if len(pc.country_alpha2_to_country_name(x)) < 18 else x)

    # sorting proportion values
    final_df = cont_df.groupby(['Location'])['FactValueNumeric'].sum().reset_index()
    final_df = final_df.sort_values(by=['FactValueNumeric'], ascending=[False])

    # making the graph...
    data = [go.Bar(x=final_df['Location'], y=final_df['FactValueNumeric'])]

    layout = go.Layout(title=f"Population Proportion Using Safely Managed Sanitation Services in {continent} in 2020", xaxis_title="Countries", yaxis_title="Population Proportion")

    fig = go.Figure(data=data, layout=layout)
    with open(f"{path[:-4]}.txt", 'w') as file:
        file.write(pyo.plot(fig, include_plotlyjs=False, output_type='div'))
    pyo.plot(fig, filename=path)

# Creating a dictionary of country codes and their respective graph html file paths
# and generating a graph for each entry
continents = {
    "EU" : '../graphs/europe/europe-sanitation.html',
    "AS" : '../graphs/asia/asia-sanitation.html',
    "NA" : '../graphs/north-america/north-america-sanitation.html',
    "AF" : '../graphs/africa/africa-sanitation.html',
    "OC" : '../graphs/oceania/oceania-sanitation.html',
    "SA" : '../graphs/south-america/south-america-sanitation.html'
}

for continent, path in continents.items():
    generate_graphs(continent, path)