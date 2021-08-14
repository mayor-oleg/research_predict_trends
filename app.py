# -*- coding: utf-8 -*-
"""
Created on Sat Aug 14 14:50:51 2021

@author: jr
"""

#Import ganeral libs
import pandas as pd

# dash imports based on flask
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

#viz imports
from plotly import graph_objs as go

#style
PLOTLY_THEME ='simple_white'
STYLE = [dbc.themes.FLATLY]

#building server
app = dash.Dash('sales_predict_app', external_stylesheets=STYLE)
server = app.server

def trends():
    l = r'https://raw.githubusercontent.com/mayor-oleg/research_predict_trends/main/predicted_clothes_df.csv'
    db = pd.read_csv(l)
    trends = db['trends'].tolist()
    return trends
trends = trends()

def clean_df(df):
    new_cols = df.iloc[0,:]
    rcol = df.columns
    for num in range(len(df.columns)):
        df.rename(columns={rcol[num]:new_cols[num]}, inplace=True)
    df = df.iloc[1:,:]    
    return df

#controls
controls =  dbc.Card(
        [
             dbc.Row([
                 dbc.Col(dbc.FormGroup(
                 [
                     dbc.Label("Select a trend:"),
                     dcc.Dropdown(
                             id = "trends-selector",
                             options = [{"label":x, "value":x} for x in trends],
                             value ="24-Hour Living"#, multi = True
                     )
                 ]
                 )),
              ], align = 'center')  
        ],
        body = True
)
                 
   
# inicialisation Graph                 
graph = dcc.Graph (id = 'graph')


#general layout
app.layout = dbc.Container(
    [
     html.H1("Sales prediction reserch"),
     html.Hr(),
     dbc.Row([dbc.Col(controls, width = 6)]),
     #dbc.Row([dbc.Col(html.Div("Wait a few minutes, we collect data"),width = 6)]),
     dbc.Row([dbc.Col(graph, width = 6)]
              #dbc.Col(qtygraph, width = 6)]
                , align =  "center")
     
    ], fluid = True
)


@app.callback(Output (component_id = 'graph', component_property = 'figure'),
              [Input(component_id = 'trends-selector', component_property = 'value')])
def update_date_graph (trend):
    print (trend)
    
    real_clothes_df = pd.read_csv(r'https://raw.githubusercontent.com/mayor-oleg/research_predict_trends/main/clothes_df.csv').drop(['Unnamed: 0'], axis = 1).T
    real_clothes_df = clean_df(real_clothes_df)
    predicted_clothes_df = pd.read_csv(r'https://raw.githubusercontent.com/mayor-oleg/research_predict_trends/main/predicted_clothes_df.csv').drop(['Unnamed: 0'], axis = 1).T
    predicted_clothes_df = clean_df(predicted_clothes_df)
    
    real_makeup_df = pd.read_csv(r'https://raw.githubusercontent.com/mayor-oleg/research_predict_trends/main/makeup_df.csv').drop(['Unnamed: 0'], axis = 1).T
    real_makeup_df = clean_df(real_makeup_df)
    predicted_makeup_df = pd.read_csv(r'https://raw.githubusercontent.com/mayor-oleg/research_predict_trends/main/predicted_makeup_df.csv').drop(['Unnamed: 0'], axis = 1).T
    predicted_makeup_df = clean_df(predicted_makeup_df)
        
    real_shoes_df = pd.read_csv(r'https://raw.githubusercontent.com/mayor-oleg/research_predict_trends/main/shoes_df.csv').drop(['Unnamed: 0'], axis = 1).T
    real_shoes_df = clean_df(real_shoes_df)
    predicted_shoes_df = pd.read_csv(r'https://raw.githubusercontent.com/mayor-oleg/research_predict_trends/main/predicted_shoes_df.csv').drop(['Unnamed: 0'], axis = 1).T
    predicted_shoes_df = clean_df(predicted_shoes_df)
    
## Vizualisation     

    periods_realc = real_clothes_df.index
    periods_predc = predicted_clothes_df.index
    
    periods_realm = real_makeup_df.index
    periods_predm = predicted_makeup_df.index
    
    periods_reals = real_shoes_df.index
    periods_preds = predicted_shoes_df.index
    fig = go.Figure(layout=go.Layout(height=400, width=1024))
# real DATA    
    fig.add_trace(go.Scatter(x = periods_realc,
                             y = real_clothes_df[trend].tolist(),
                             fill = None, mode = 'lines+markers',
                             name = 'Actual clothes', line = {'color':'green', 'width':2}))
# Predicted Data
    fig.add_trace(go.Scatter(x = periods_predc,
                             y = predicted_clothes_df[trend].tolist(),
                             fill = None, mode = 'lines+markers',
                             name = 'Predicted clothes', 
                             line = dict(shape = 'linear', color = 'green', width= 2, dash = 'dash')))


# real DATA    
    fig.add_trace(go.Scatter(x = periods_realm,
                             y = real_makeup_df[trend].tolist(),
                             fill = None, mode = 'lines+markers',
                             name = 'Actual makeup', line = {'color':'blue', 'width':2}))
# Predicted Data
    fig.add_trace(go.Scatter(x = periods_predm,
                             y = predicted_makeup_df[trend].tolist(),
                             fill = None, mode = 'lines+markers',
                             name = 'Predicted makeup', 
                             line = dict(shape = 'linear', color = 'blue', width= 2, dash = 'dash')))



# real DATA    
    fig.add_trace(go.Scatter(x = periods_reals,
                             y = real_shoes_df[trend].tolist(),
                             fill = None, mode = 'lines+markers',
                             name = 'Actual shoes', line = {'color':'yellow', 'width':2}))
# Predicted Data
    fig.add_trace(go.Scatter(x = periods_preds,
                             y = predicted_shoes_df[trend].tolist(),
                             fill = None, mode = 'lines+markers',
                             name = 'Predicted shoes', 
                             line = dict(shape = 'linear', color = 'yellow', width= 2, dash = 'dash')))

    return fig

if __name__ =="__main__":
    app.run_server()
    
                 
