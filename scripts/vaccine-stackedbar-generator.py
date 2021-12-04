import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go
import numpy as np


def generate_graphs(continent, path):
    # Load CSV file from Datasets folder
    df = pd.read_csv('../Datasets/VaccinationsPercentage.csv')

    # making sure it only has data for the current continent
    df = df[df['continent'] == continent]

    # turning every empty string into a NAN type to kill these entries easily
    df.replace('', np.nan, inplace=True)

    # removing all NANs from both dataframes
    df.dropna(subset=['people_fully_vaccinated_per_hundred'], inplace=True)

    df.dropna(subset=['people_vaccinated_per_hundred'], inplace=True)

    # removing all duplicate countries (not just duplicate entries), only saving the latest data for each country
    df = df.drop_duplicates(subset=['location'], keep='last')
    
    # creating a difference variable in the dataframe that holds total % vaccinated - total of fully vaccinated %
    df['difference'] = (df['people_vaccinated_per_hundred'] - df['people_fully_vaccinated_per_hundred'])

    # grouping everything by country (each bar should be a country) and sorting the data
    final_df = df.groupby(['location'])['people_fully_vaccinated_per_hundred'].sum().reset_index()
    final_df = final_df.sort_values(by=['people_fully_vaccinated_per_hundred'], ascending=[False])
                                    
    # grouping the second dataframe
    final_df2 = df.groupby(['location'])['difference'].sum().reset_index()

    # preparing data
    data = [go.Bar(name='% of fully vaccinated people', x=final_df['location'],
                   y=final_df['people_fully_vaccinated_per_hundred']),
            go.Bar(name='% of partially vaccinated people', x=final_df2['location'], y=final_df2['difference'])]

    layout = go.Layout(title=f"Covid-19 Vaccine Proportions by country in {continent} 2021", xaxis_title="Countries",
                       yaxis_title="Population Proportion (%)", barmode='stack')

    fig = go.Figure(data=data, layout=layout)
    
    # resorts data based on total height of the bar
    fig.update_layout(barmode='stack', xaxis={'categoryorder': 'total descending'})


    pyo.plot(fig, filename=path)

# Creating a dictionary of country codes and their respective graph html file paths
# and generating a graph for each entry
continents = {
    "Europe" : '../graphs/europe/europe-vaccination-rates.html',
    "Asia" : '../graphs/asia/asia-vaccination-rates.html',
    "North America" : '../graphs/north-america/north-america-vaccination-rates.html',
    "Africa" : '../graphs/africa/africa-vaccination-rates.html',
    "Oceania" : '../graphs/oceania/oceania-vaccination-rates.html',
    "South America" : '../graphs/south-america/south-america-vaccination-rates.html'
}

for continent, path in continents.items():
    generate_graphs(continent, path)


