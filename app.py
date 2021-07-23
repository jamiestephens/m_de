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
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
#gbl = globals()

#with open('./assets/custom_georegions.json', 'r') as fp:
   # custom_geoj = json.load(fp)
    
engine = create_engine('sqlite:///forex.db')

country_convert = {'JPY':'JPN',
                   'GBP':'GBR',
                   'EUR':'DEU',
                   #'EUR':'EUR',
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

futures_JPY = pd.read_sql_table('futures_JPY', engine,index_col='index')
futures_GBP = pd.read_sql_table('futures_GBP', engine,index_col='index')
futures_EUR = pd.read_sql_table('futures_EUR', engine,index_col='index')
futures_AUD = pd.read_sql_table('futures_AUD', engine,index_col='index')
futures_NZD = pd.read_sql_table('futures_NZD', engine,index_col='index')
futures_MXN = pd.read_sql_table('futures_MXN', engine,index_col='index')
futures_ZAR = pd.read_sql_table('futures_ZAR', engine,index_col='index')

futuresdict = {'Japanese Yen':'JPY',
           'British Pound':'GBP',
           'Euro':'EUR',
           'Australian Dollar':'AUD',
           'New Zealand Dollar':'NZD',
           'Mexican Peso':'MXN',
           'South African Rand':'ZAR'}

s = 'hrlytable_EUR'

hrly_times = {'30 days': datetime.now() - relativedelta(years=1),
              '60 days':datetime.now() - relativedelta(months=1),
              '6 months':datetime.now() - relativedelta(months=6),
              '1 year':datetime.now() - relativedelta(years=1)}

min_times = {'Last 24 hours': datetime.now() - relativedelta(days=1),
              'Last 3 days':datetime.now() - relativedelta(days=3),
              'Last 7 days':datetime.now() - relativedelta(days=7)}




app = dash.Dash(__name__)

#d=min_times[]

#def heatmap(currencylist):
final_df = pd.DataFrame(columns=['Currency','First','Last'])
df = pd.read_sql_table('heatmaptable', engine)



last_value = df['Datetime'].loc[~df['Datetime'].isnull()].iloc[-1]
print("Last value "+str(last_value))
threedaysprior = last_value - relativedelta(days=3)
print("Three days prior: "+str(threedaysprior))
df = df[df['Datetime'] < threedaysprior]

print(df.head())
print(df.tail())

final_df['Currency'] = final_df['Currency'].map(country_convert)
#for i in currencylist:
for i,u in country_convert.items():
   if i in df.columns:
        first_value = df[i].loc[~df[i].isnull()].iloc[0]
        last_value = df[i].loc[~df[i].isnull()].iloc[-1]
        final_df.loc[len(final_df.index)] = [i, first_value,last_value]

final_df['Difference'] = final_df['Last'] - final_df['First']
final_df['Percent Chg'] = (final_df['Difference'] / final_df['First'])*100


fig = px.choropleth(final_df, locations="Currency",
            color="Percent Chg",
            hover_name="Currency",
            color_continuous_scale=px.colors.sequential.Plasma)

fig.update_layout(paper_bgcolor='rgb(169,169,169)')
fig.show()
   # return fig

#heatmap_fig = heatmap(currencies) 

def datatable(choice):
    pass

def arbitragetable(i,p,rf):
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
    row15 = html.Tr([html.Td("Borrow USD"), html.Td(" ")])
    row16 = html.Tr([html.Td("Convert USD"), html.Td(" ")])
    row17 = html.Tr([html.Td("Deposit ",i), html.Td(" ")])
    row18 = html.Tr([html.Td("After "+p), html.Td(" ")])
    row19 = html.Tr([html.Td("Value of "+i), html.Td(" ")])
    row22 = html.Tr([html.Td("Deliver amount"), html.Td(" ")])
    row23 = html.Tr([html.Td("Receive interest"), html.Td(" ")])
    row24 = html.Tr([html.Td("Repay loan interest at " + str(rf) + "%"), html.Td(" ")])
    row25 = html.Tr([html.Td("Profit"), html.Td(" ")])
    table_body = [html.Tbody([row1, row2, row3, row4,row5,row6,row7,row8,row9,row10,row11,row12,row13,row14,row15,row16,row17,row18,
                          row19,row22,row23,row24,row25])]
    table = dbc.Table(table_body, bordered=False)
    return table


i = 'Euro'
p = '12 months'
rf = 0.0

table = arbitragetable(i,p,rf)

def linegraph(s):
    hourlychosenmap = pd.read_sql_table(s, engine,index_col='index')
    hourly_fig = go.Figure(data=go.Scatter(x = hourlychosenmap.index, y = hourlychosenmap.Close))
    hourly_fig.update_traces(line_color='#000000')
    hourly_fig.update_layout(paper_bgcolor='rgb(169,169,169)')
    hourly_fig.show()   
    return hourly_fig

hourly_fig = linegraph(s)

body = html.Div([
    html.H1("Foreign Exchange Dashboard")
    , html.H5("Jamie Stephens • July 2021 • Metis",style={'textAlign':'center'})
    , dbc.Row([
            dbc.Col(html.Div(dbc.Alert([html.P("Percent change in value relative to the United States Dollar"),
                                        html.P("Time Duration",style={'font-weight':'700'}),
                                        dcc.RadioItems(id='heatmaptimes',options=[{"label":k, "value":v} for k,v in min_times.items()],
                                             value=list(min_times.keys())[0],
                                             labelStyle={'display': 'block'})]),style={'textAlign':'center','color':'black'}), width=3)
            , dbc.Col(dbc.Alert(html.Div( dcc.Graph(figure=fig),style={})))
            ])
    , dbc.Row(dbc.Col(html.Div(dbc.Alert(html.Div([dcc.Dropdown(
                                                        id='futuresdropdown',
                                                        options=[{"label":k, "value":v} for k,v in futuresdict.items()],
                                                        value = list(futuresdict.keys())[0])])))))    
    ,dbc.Row([dbc.Col(html.Div(dbc.Alert([html.P(i + "/USD Change in Value (Hourly)",style={'textAlign':'center','color':'black','font-weight':'700'}),
                                          html.Div( dcc.Graph(figure=hourly_fig),style={}),
                                          html.Div([dcc.RadioItems(
                                                        id='hrly_timerange',
                                                        options=[{"label":k, "value":v} for k,v in hrly_times.items()],
                                                        labelStyle={'display': 'block'})],style={"width": "50%"})])))
              
              
             ,dbc.Col(html.Div(dbc.Alert([html.P("Futures Contracts",style={'textAlign':'center','color':'black','font-weight':'700'}),dash_table.DataTable(id='table',
                                                             columns=[{"name": i, "id": i} for i in futures_EUR.columns],
                                                             row_selectable='single',
                                                             data=futures_EUR.to_dict('records'),
                                                                 style_data={'backgroundColor': 'transparent',
                                                                             'align':"center"},
                                                             style_cell={'fontSize':10, 'font-family':'sans-serif'})]),
                                        style={'textAlign':'center','color':'black'}))

             ,dbc.Col(html.Div(dbc.Alert(dbc.Alert([html.P("Currency Arbitrage",style={'textAlign':'center','color':'black','font-weight':'700'}),
                                          html.P(table)]))))
    ])])


app.layout = html.Div([body])

if __name__ == '__main__':
 #   app.run_server(host='0.0.0.0', port=8080, debug=True, use_reloader=False)
    app.run_server()