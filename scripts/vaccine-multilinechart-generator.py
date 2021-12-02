import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go

# Load CSV file from Datasets folder
df = pd.read_csv('E:\PycharmProjects\FinalProjectTest\my_venv\Datasets\VaccinationsPercentage.csv')

df = df.query('continent == "Asia"')
Start = '2020-11-15'
End = '2021-11-30'
df['date'] = pd.to_datetime(df['date'], dayfirst=True)
mask = (df['date'] > Start) & (df['date'] <= End)
df1 = df.loc[mask]

# Filter and pivot dataset for each country,
# and add lines for each country
fig = go.Figure()
for c in df1['location'].unique()[:]:
    dfp = df1[df1['location']==c].pivot(index='date', columns='location', values='people_fully_vaccinated_per_hundred')
    fig.add_traces(go.Scatter(x=dfp.index, y=dfp[c], mode='lines', name = c))

fig.show()