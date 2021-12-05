import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go
from traitlets.traitlets import default
import data_cleaner as dc

def generate_graphs(continent, path):
    df = pd.read_csv('../Datasets/AirPollution.csv')

    # adding continent col to df
    df = dc.add_continent_col(df)

    # keeping the selected continent rows only
    df = df[df['Continent'] == continent]

    data = []
    country_list = df['Location'].to_list() # unique list of countries in the df
    latest_country_df = df.drop_duplicates(subset=['Location'], keep='last') # country vals for latest year only

    # list of default countries shown in the graph
    # countries only show up on the graph if their FactValueNumeric value is among the 5 highest
    # out of every country value from 2016
    default_country_list = latest_country_df.nsmallest(n=5, columns=['FactValueNumeric'])['Location'].to_list()

    # adding traces to data list
    for country in country_list:
        curr_df = df[df['Location'] ==  country]
        line = go.Scatter(x=curr_df['Period'], y=curr_df['FactValueNumeric'], mode='lines+markers', name=country)
        data.append(line)

    # preparing and outputting graph
    layout = go.Layout(title=f'Concentrations of fine particulate matter (PM2.5) in {continent} from 2010 to 2016', xaxis_title="Year", yaxis_title="Annual mean level of fine particulate matter (weighted by population)")
    fig = go.Figure(data=data, layout=layout)
    fig.for_each_trace(lambda trace: trace.update(visible="legendonly") if trace.name not in default_country_list else ())
    pyo.plot(fig, filename=path)

# Creating a dictionary of country codes and their respective graph html file paths
# and generating a graph for each entry
continents = {
    "EU" : '../graphs/europe/europe-air-pollution.html',
    "AS" : '../graphs/asia/asia-air-pollution.html',
    "NA" : '../graphs/north-america/north-america-air-pollution.html',
    "AF" : '../graphs/africa/africa-air-pollution.html',
    "OC" : '../graphs/oceania/oceania-air-pollution.html',
    "SA" : '../graphs/south-america/south-america-air-pollution.html'
}

for continent, path in continents.items():
    generate_graphs(continent, path)


