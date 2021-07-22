# -*- coding: utf-8 -*-
"""
Created on Tue Jul 13 12:56:58 2021

@author: Administrator
"""
import yfinance as yf
import plotly
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
from sqlalchemy import create_engine
import numpy as np
import geojson
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
import json
import plotly.graph_objects as go

import webscrape_investing



with open('./assets/custom_georegions.json', 'r') as fp:
    custom_geoj = json.load(fp)
    
engine = create_engine('sqlite:///forex.db')

currencies = ['JPY','GBP','EUR','AUD','NZD','CNY','HKD','SGD','INR','MXN','PHP','THB','MYR','ZAR','RUB']

df = pd.read_sql_table('heatmaptable', engine)

final_df = pd.DataFrame(columns=['Currency','First','Last'])
for i in currencies:
    if i in df.columns:
        first_value = df[i].loc[~df[i].isnull()].iloc[0]
        last_value = df[i].loc[~df[i].isnull()].iloc[-1]
        final_df.loc[len(final_df.index)] = [i, first_value,last_value]
final_df['Difference'] = final_df['Last'] - final_df['First']
final_df['Percent Chg'] = (final_df['Difference'] / final_df['First'])*100
country_convert = {'JPY':'JPN',
                   'GBP':'GBR',
                   'EUR':'EUR',
                   'AUD':'AUS',
                   'NZD':'NZL',
                   'CNY':'CHN',
                   'HKD':'HKG',
                   'SGD':'SGP',
                   'INR':'IDN',
                   'MXN':'MEX',
                   'PHP':'PHL',
                   'THB':'THA',
                   'MYR':'MYS',
                   'ZAR':'ZAF',
                   'RUB':'RUS'}

final_df['Currency'] = final_df['Currency'].map(country_convert)

fig = px.choropleth(final_df, locations="Currency",
                color="Percent Chg",
                hover_name="Currency",
                color_continuous_scale=px.colors.sequential.Plasma)
          
fig.update_layout(paper_bgcolor='rgb(211,211,211)')
fig.show()   
timespan = ['Last 24 hours','Last 3 days','Last 7 days']

app = dash.Dash(__name__)

body = html.Div([
    html.H1("Foreign Exchange Arbitrage Dashboard")
    , dbc.Row(dbc.Col(html.Div(dbc.Alert("Jamie Stephens • July 2021 • Metis"),style={'textAlign':'center','color':'black'})))
    , dbc.Row([
            dbc.Col(html.Div([html.P("Time Duration",style={'font-weight':'700'}),dcc.RadioItems(id='heatmaptimes',options=[{'value': x, 'label': x} for x in timespan],
                                             value=timespan[0],
                                             labelStyle={'display': 'block'})],style={'textAlign':'center'}), width=3)
            , dbc.Col(html.Div( dcc.Graph(figure=fig),style={}))
            ])
    ,dbc.Row([dbc.Col(html.Div(dbc.Alert("Jamie Stephens"),style={'textAlign':'center','color':'black'})),
             dbc.Col(html.Div(dbc.Alert("Jamie Stephens"),style={'textAlign':'center','color':'black'}))
            ])
    ])


app.layout = html.Div([body])

if __name__ == '__main__':
    app.run_server()