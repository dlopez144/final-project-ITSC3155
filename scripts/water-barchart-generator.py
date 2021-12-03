from numpy import nan
import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go


def gen_barchart(continent, path):
    # Load data
    df = pd.read_csv('../Datasets/SafelyManagedDrinkingWater.csv')

    # Select continent
    df = df[df.ParentLocation == continent]

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
    ["Europe", '../graphs/europe/europe-water.html'],
    ["South-East Asia", '../graphs/asia/asia-water.html'],
    ["Americas", '../graphs/north-america/north-america-water.html'],
    ["Africa", '../graphs/africa/africa-water.html'],
    ["Western Pacific", '../graphs/oceania/oceania-water.html'],
    ["Americas", '../graphs/south-america/south-america-water.html']
]

for j in jobs:
    gen_barchart(j[0], j[1])
