import requests
import pandas as pd
import numpy as np
from datetime import datetime as dt
import json
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objs as go

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# code and plot setup
# settings
pd.options.plotting.backend = "plotly"
countdown = 20
#global df

# sample dataframe of a wide format
cols = ['temperature']
X = np.ones(50)*18
df=pd.DataFrame(X, columns=cols)

# plotly figure
fig = df.plot(template = 'plotly_dark')

app = JupyterDash(__name__)
app.layout = html.Div([
    html.H1("Winecellar temperatures"),
            dcc.Interval(
            id='interval-component',
            interval=20*1000, # in milliseconds
            n_intervals=0
        ),
    dcc.Graph(id='graph'),
])

# Define callback to update graph
@app.callback(
    Output('graph', 'figure'),
    [Input('interval-component', "n_intervals")]
)
def streamFig(value):
    
    global df
    
    raw= requests.get('http://app:8000/records/all?dt=24')

    Y = raw.json()
    df2 = pd.DataFrame(Y)
    cols = df2['loc'].unique()
    df_new = pd.DataFrame()
    for col in cols:
        try:
            df_iter = df2.loc[df2['loc']==col][['date','temperature']].set_index('date',drop=True).rename(columns={'temperature':col})
            df_new = df_new.join(df_iter,'date')
        except KeyError:
            df_new = df2.loc[df2['loc']==col][['date','temperature']].set_index('date',drop=True).rename(columns={'temperature':col})
    df3 = df_new.copy()
    #df3 = df3.cumsum()#.tail(1000)
    fig = df3.plot(template = 'plotly_dark')
    #fig.show()
    
    colors = px.colors.qualitative.Plotly
    for i, col in enumerate(df3.columns):
            fig.add_annotation(x=df3.index[-1], y=df3[col].iloc[-1],
                                   text = str(df3[col].iloc[-1])[:4],
                                   align="right",
                                   arrowcolor = 'rgba(0,0,0,0)',
                                   ax=25,
                                   ay=0,
                                   yanchor = 'middle',
                                   font = dict(color = colors[i]))
    
    return(fig)

app.run_server(mode='external', host='0.0.0.0',port = 8069, dev_tools_ui=True, #debug=True,
              dev_tools_hot_reload =True, threaded=True)