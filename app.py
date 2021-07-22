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
import dash_table
#import webscrape_investing
gbl = globals()


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
          
fig.update_layout(paper_bgcolor='rgb(169,169,169)')
fig.show()   
timespan = ['Last 24 hours','Last 3 days','Last 7 days']


futures_JPY = pd.read_sql_table('futures_JPY', engine,index_col='index')
futures_GBP = pd.read_sql_table('futures_GBP', engine,index_col='index')
futures_EUR = pd.read_sql_table('futures_EUR', engine,index_col='index')
futures_AUD = pd.read_sql_table('futures_AUD', engine,index_col='index')
futures_NZD = pd.read_sql_table('futures_NZD', engine,index_col='index')
#futures_HKD = pd.read_sql_table('futures_HKD', engine,index_col='index')
# futures_SGD = pd.read_sql_table('futures_SGD', engine,index_col='index')
#futures_INR = pd.read_sql_table('futures_INR', engine,index_col='index')
futures_MXN = pd.read_sql_table('futures_MXN', engine,index_col='index')
# futures_PHP = pd.read_sql_table('futures_PHP', engine,index_col='index')
# futures_THB = pd.read_sql_table('futures_THB', engine,index_col='index')
# futures_MYR = pd.read_sql_table('futures_MYR', engine,index_col='index')
futures_ZAR = pd.read_sql_table('futures_ZAR', engine,index_col='index')
#  futures_RUB = pd.read_sql_table('futures_RUB', engine,index_col='index')
   
#for i in currencies:
#    table_name = "futures_"+str(i)
#    print(table_name)
#    try:
#        gbl[table_name] = pd.read_sql_table(table_name, engine,index_col='index')
#    except ValueError:
#        pass

futuresdict = {'Japanese Yen':'JPY',
           'British Pound':'GBP',
           'Euro':'EUR',
           'Australian Dollar':'AUD',
           'New Zealand Dollar':'NZD',
           'Mexican Peso':'MXN',
           'South African Rand':'ZAR'}

print(futures_EUR)    
    
def datatablechange():
    pass
        

app = dash.Dash(__name__)

i = "Euro"
p = "12 months"
#table_header = [
#    html.Thead(html.Tr([html.Th("First Name"), html.Th("Last Name")]))]

rf = 0.0

row1 = html.Tr([html.Td("First currency"), html.Td("United States Dollar")])
row2 = html.Tr([html.Td("Second currency"), html.Td(i)])
row3 = html.Tr([html.Td(p), html.Td("0")])
row4 = html.Tr([html.Td(str(i)+"/USD futures quote"), html.Td(" ")])
row5 = html.Tr([html.Td(str(i)+"/USD spot quote"), html.Td(" ")])
row6 = html.Tr([html.Td("Contracts to trade"), html.Td(" ")])
row7 = html.Tr([html.Td("Contract size"), html.Td(" ")])
row8 = html.Tr([html.Td("Delivery"), html.Td(" ")])
row9 = html.Tr([html.Td(i + " " + p + " interest rate"), html.Td(" ")])
row10 = html.Tr([html.Td("USD " + p + " interest rate"), html.Td(" ")])
row11 = html.Tr([html.Td("Interest rate spread"), html.Td(" ")])
row12 = html.Tr([html.Td("Fair value"), html.Td(" ")])
row13 = html.Tr([html.Td("Anomaly"), html.Td(" ")])
row14 = html.Tr([html.Td("Sell 1x " + i + "/USD future at:"), html.Td(" ")])
row15 = html.Tr([html.Td(" "), html.Td(" ")])
row16 = html.Tr([html.Td(" "), html.Td(" ")])
row17 = html.Tr([html.Td(" "), html.Td(" ")])
row18 = html.Tr([html.Td(" "), html.Td(" ")])
row19 = html.Tr([html.Td(" "), html.Td(" ")])
row20 = html.Tr([html.Td(" "), html.Td(" ")])
row21 = html.Tr([html.Td(" "), html.Td(" ")])
row22 = html.Tr([html.Td("Deliver amount"), html.Td(" ")])
row23 = html.Tr([html.Td("Receive interest"), html.Td(" ")])
row24 = html.Tr([html.Td("Repay loan interest at " + str(rf) + "%"), html.Td(" ")])
row25 = html.Tr([html.Td("Profit"), html.Td(" ")])

table_body = [html.Tbody([row1, row2, row3, row4,row5,row6,row7,row8,row9,row10,row11,row12,row13,row14,row15,row16,row17,row18,
                          row19,row20,row21,row22,row23,row24])]

table = dbc.Table(table_body, bordered=False)


s = 'hrlytable_EUR'

hrly_times = {'30 days':30,
              '60 days':60,
              '6 months':0,
              '1 year':365}

def linegraph(s):
    hourlychosenmap = pd.read_sql_table(s, engine,index_col='index')
    hourly_fig = go.Figure(data=go.Scatter(x = hourlychosenmap.index, y = hourlychosenmap.Close))
    return hourly_fig

hourly_fig = linegraph(s)


body = html.Div([
    html.H1("Foreign Exchange Dashboard")
    , html.H5("Jamie Stephens • July 2021 • Metis",style={'textAlign':'center'})
    , dbc.Row([
            dbc.Col(html.Div(dbc.Alert([html.P("Time Duration",style={'font-weight':'700'}),dcc.RadioItems(id='heatmaptimes',options=[{'value': x, 'label': x} for x in timespan],
                                             value=timespan[0],
                                             labelStyle={'display': 'block'})]),style={'textAlign':'center','color':'black'}), width=3)
            , dbc.Col(dbc.Alert(html.Div( dcc.Graph(figure=fig),style={})))
            ])
    , dbc.Row(dbc.Col(html.Div(dbc.Alert(html.P("USD to ForEx Futures Arbitrage"),style={'textAlign':'center','color':'black'}))))
    , dbc.Row(dbc.Col(html.Div(dbc.Alert(html.Div([dcc.Dropdown(
                                                        id='futuresdropdown',
                                                        options=[{"label":k, "value":v} for k,v in futuresdict.items()],
                                                        value = list(hrly_times.keys())[0])])))))    
    ,dbc.Row([dbc.Col(html.Div(dbc.Alert([html.P(i + " Relative Change in Value",style={'textAlign':'center','color':'black'}),
                                          html.Div( dcc.Graph(figure=hourly_fig),style={}),
                                          html.Div([dcc.RadioItems(
                                                        id='hrly_timerange',
                                                        options=[{"label":k, "value":v} for k,v in hrly_times.items()],
                                                        labelStyle={'display': 'block'})])])))
              
              
             ,dbc.Col(html.Div(dbc.Alert([html.P("Futures Contracts"),dash_table.DataTable(id='table',
                                                             columns=[{"name": i, "id": i} for i in futures_EUR.columns],
                                                             data=futures_EUR.to_dict('records'),
                                                             style_cell={'fontSize':10, 'font-family':'sans-serif'})]),
                                        style={'textAlign':'center','color':'black'}))

             ,dbc.Col(html.Div(dbc.Alert(dbc.Alert([html.P("Currency Arbitrage",style={'textAlign':'center','color':'black'}),
                                          html.P(table)]))))
    ])])


app.layout = html.Div([body])

if __name__ == '__main__':
    app.run_server()