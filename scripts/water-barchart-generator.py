import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go

# Load data
df = pd.read_csv('../Datasets/SafelyManagedDrinkingWater.csv')

# Select continent
df = df[df.ParentLocation == 'Europe']

# Sort from lowest to highest
filtered_df = df.sort_values(by=['Location'])

#TODO Get an average ['Value'] for each country, as they're currently split into regions/urban/suburban/etc.

# Preparing data
data = [go.Bar(
        x=filtered_df['Location'],
        y=filtered_df['Value'] # Not averaged yet
)]

# Preparing layout
layout = go.Layout(title='safety_managed_drinking_water', xaxis_title="Countries",
                   yaxis_title="Population using safely managed drinking-water services (%)")


fig = go.Figure(data=data, layout=layout)
fig.show()
