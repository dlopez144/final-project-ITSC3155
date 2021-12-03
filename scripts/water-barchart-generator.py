from numpy import nan
import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go
import data_cleaner as dc

def gen_barchart(continent, path):
    # Load data
    df = pd.read_csv('../Datasets/SafelyManagedDrinkingWater.csv')

    # Adding continent column to dataframe
    df = dc.add_continent_col(df)

    # Select continent
    df = df[df.Continent == continent]

    # Leave only one row for each country in the selected continent
    filtered_df = df.drop_duplicates('Location', keep='first')

    # Average a specific country's access to water
    avg_df = {}
    for country in filtered_df['Location']:
        country_df = df[df.Location == country]
        avg_df[country] = country_df['Value'].mean()

    # Sort by descending order of % pop with clean water
    sorted_df = dict(sorted(avg_df.items(), key=lambda x: x[1], reverse=True))

    # Remove countries with no data
    sorted_df = {k: v for k, v in sorted_df.items() if v is not nan}

    # Data
    data = [
        go.Bar(x=list(sorted_df.keys()),
               y=list(sorted_df.values()))
    ]

    # Layout
    layout = go.Layout(title=f'Access to Safe Drinking Water in {continent}', xaxis_title="Countries",
                       yaxis_title="Population drinking safe water (%)")

    # Write file
    fig = go.Figure(data=data, layout=layout)
    pyo.plot(fig, filename=path)


jobs = [
    ["EU", '../graphs/europe/europe-water.html'],
    ["AS", '../graphs/asia/asia-water.html'],
    ["NA", '../graphs/north-america/north-america-water.html'],
    ["AF", '../graphs/africa/africa-water.html'],
    ["OC", '../graphs/oceania/oceania-water.html'],
    ["SA", '../graphs/south-america/south-america-water.html']
]

for j in jobs:
    gen_barchart(j[0], j[1])
