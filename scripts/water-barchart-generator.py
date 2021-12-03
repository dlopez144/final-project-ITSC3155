from numpy import nan
import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go

# Load data
df = pd.read_csv('../Datasets/SafelyManagedDrinkingWater.csv')

# Select continent
df = df[df.ParentLocation == 'Americas']

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
layout = go.Layout(title='safety_managed_drinking_water', xaxis_title="Countries",
                   yaxis_title="Population using safely managed drinking-water services (%)")


fig = go.Figure(data=data, layout=layout)
fig.show()
