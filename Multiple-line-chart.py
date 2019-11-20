import dash_table_experiments
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import dash_table_experiments as dash_table
import dash
from dash.dependencies import Input, Output
import dash_table
import pandas as pd
import plotly_express as px
import plotly.offline as pyo

dff3 = pd.read_csv('df3.csv', encoding='latin-1', low_memory=False)
dff3
fdr = dff3.groupby(['Time', 'Machine']).sum()

fdrf = fdr.drop(['Units Pruduced'], axis=1)
fdrf = fdrf.drop_duplicates()
fdrf




dff4 = pd.read_csv('df3.csv', encoding='latin-1', low_memory=False)
dff4
fdr4= dff3.groupby(['Machine', 'Time']).sum()
fdr4.reset_index(inplace=True)

fig = px.scatter(fdr4, x="Time", y="Units Pruduced", color="Machine", template="plotly_white")
fig.update_traces(mode='lines+markers')

app = dash.Dash()



app.layout = html.Div([ 


dcc.Graph(
        id = 'GrapGo',
        figure = fig)
    
])


if __name__ == '__main__':
    app.run_server()
