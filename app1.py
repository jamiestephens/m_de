# -*- coding: utf-8 -*-
"""
Created on Thu Jul 22 13:35:07 2021

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
from dash_extensions.enrich import Output, DashProxy, Input, MultiplexerTransform, State
gbl = globals()

#with open('./assets/custom_georegions.json', 'r') as fp:
#    custom_geoj = json.load(fp)
    
engine = create_engine('sqlite:///forex.db')

country_convert = {'JPY':'JPN',
                   'GBP':'GBR',
                   'EUR':'DEU',
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

futuresdict = {'Japanese Yen':'JPY',
            'British Pound':'GBP',
            'Euro':'EUR',
            'Australian Dollar':'AUD',
            'New Zealand Dollar':'NZD',
            'Mexican Peso':'MXN',
            'South African Rand':'ZAR'}

app = dash.Dash(__name__)

min_times = {'Last 24 hours': 1,
              'Last 3 days': 2,
              'Last 7 days': 3}
    
def arbitragetable(money,p,rf):
    row1 = html.Tr([html.Td("First currency"), html.Td("United States Dollar")])
    row2 = html.Tr([html.Td("Second currency"), html.Td(money)])
    row3 = html.Tr([html.Td(p), html.Td("0")])
    row4 = html.Tr([html.Td(str(money)+"/USD futures quote"), html.Td(" ")])
    row5 = html.Tr([html.Td(str(money)+"/USD spot quote"), html.Td(" ")])
    row6 = html.Tr([html.Td("Contracts to trade"), html.Td(" ")])
    row7 = html.Tr([html.Td("Contract size"), html.Td(" ")])
    row8 = html.Tr([html.Td("Delivery"), html.Td(" ")])
    row9 = html.Tr([html.Td(money + " " + p + " interest rate"), html.Td(" ")])
    row10 = html.Tr([html.Td("USD " + p + " interest rate"), html.Td(" ")])
    row11 = html.Tr([html.Td("Interest rate spread"), html.Td(" ")])
    row12 = html.Tr([html.Td("Fair value"), html.Td(" ")])
    row13 = html.Tr([html.Td("Anomaly"), html.Td(" ")])
    row14 = html.Tr([html.Td("Sell 1x " + money + "/USD future at:"), html.Td(" ")])
    row15 = html.Tr([html.Td("Borrow USD"), html.Td(" ")])
    row16 = html.Tr([html.Td("Convert USD"), html.Td(" ")])
    row17 = html.Tr([html.Td("Deposit ",money), html.Td(" ")])
    row18 = html.Tr([html.Td("After "+ p), html.Td(" ")])
    row19 = html.Tr([html.Td("Value of "+ money), html.Td(" ")])
    row22 = html.Tr([html.Td("Deliver amount"), html.Td(" ")])
    row23 = html.Tr([html.Td("Receive interest"), html.Td(" ")])
    row24 = html.Tr([html.Td("Repay loan interest at " + str(rf) + "%"), html.Td(" ")])
    row25 = html.Tr([html.Td("Profit"), html.Td(" ")])
    table_body = [html.Tbody([row1, row2, row3, row4,row5,row6,row7,row8,row9,row10,row11,row12,row13,row14,row15,row16,row17,row18,
                          row19,row22,row23,row24,row25])]
    table = dbc.Table(table_body, bordered=False)
    return table

table = arbitragetable('Euro','12 months',0.0)

hrly_times = {'30 days': 30,
              '60 days':60,
              '6 months': 182,
              '1 year':365}

rfrates_USD = {30:0.04,
               60:0.04,
               90:0.05,
               365:0.07,
               730:0.2,
               1095:0.37,
               1825:0.71,
               2555:1.02,
               3650:1.27,
               7300:1.82,
               10950:1.9}

rfrates_NZD = {365:0,
    730:0.74,
    1825:1.15,
    3650:1.52}

rfrates_EUR = {90:-0.663,
               365:-0.663,
               730:-0.725,
               1095:-0.789}


header_line = html.H1("Foreign Exchange Dashboard")
second_line = html.H5("Jamie Stephens • July 2021 • Metis",style={'textAlign':'center'})

body = html.Div([
    header_line
    , second_line
    , dbc.Row([
            dbc.Col(html.Div(dbc.Alert([html.P("Time Duration",style={'font-weight':'700'}),
                                        html.P("Percent change in value relative to the United States Dollar")
                                        ,dcc.RadioItems(id='heatmaptimes',options=[{"label":k, "value":v} for k,v in min_times.items()],
                                             value=list(min_times.values())[2],
                                             labelStyle={'display': 'block'})]),style={'textAlign':'center','color':'black'}), width=3)
            , dbc.Col(dbc.Alert(html.Div( dcc.Graph(id='heatmap_map'),style={})))
            ])
    , dbc.Row(dbc.Col(html.Div(dbc.Alert(html.Div([dcc.Dropdown(
                                                        id='futuresdropdown',
                                                        searchable=False,
                                                        clearable=False,
                                                        options=[{"label":k, "value":v} for k,v in futuresdict.items()],
                                                        value = list(futuresdict.values())[0])])))))    
    ,dbc.Row([dbc.Col(dbc.Alert([html.Div(id='linegraphheader'),
                                          html.Div( dcc.Graph(id='singleforex'),style={}),
                                          html.Div([dcc.RadioItems(
                                                        id='hrly_timerange',
                                                        options=[{"label":k, "value":v} for k,v in hrly_times.items()],
                                                        value = list(hrly_times.values())[3],
                                                        labelStyle={'display': 'block'})],style={"width": "50%"})]))
              
             ,dbc.Col(dbc.Alert([html.P("Futures Contracts",style={'textAlign':'center','color':'black','font-weight':'700'}),
                                          html.Div(id='content')]),
                                        style={'textAlign':'center','color':'black'})

             ,dbc.Col(dbc.Alert([html.Div(id='content3'),html.P("Currency Arbitrage",style={'textAlign':'center','color':'black','font-weight':'700'}),
                                          ]))
    ])])
#    ])

app.layout = html.Div([body])


@app.callback(
    Output('heatmap_map','figure'),
    Input('heatmaptimes','value'))
def heatmap(d):
    df = pd.read_sql_table('heatmaptable', engine)
    final_df = pd.DataFrame(columns=['Currency','First','Last'])
    
    lastdatetimevalue = df['Datetime'].loc[~df['Datetime'].isnull()].iloc[-1]
    
    if d == 2:
        threedaysprior = lastdatetimevalue - relativedelta(days=3)
        df = df[df['Datetime'] > threedaysprior]
    elif d == 1:
        onedayprior = lastdatetimevalue - relativedelta(days=1)
        df = df[df['Datetime'] > onedayprior]
    
    for i,u in country_convert.items():
        if i in df.columns:
            first_value = df[i].loc[~df[i].isnull()].iloc[0]
            last_value = df[i].loc[~df[i].isnull()].iloc[-1]
            final_df.loc[len(final_df.index)] = [i, first_value,last_value]
    
    final_df['Difference'] = final_df['Last'] - final_df['First']
    final_df['Percent Chg'] = (final_df['Difference'] / final_df['First'])*100

    final_df['Currency'] = final_df['Currency'].map(country_convert)
    fig = px.choropleth(final_df, locations="Currency",
                color="Percent Chg",
                hover_name="Currency",
                range_color = (-2,2),
                color_continuous_scale=px.colors.sequential.Plasma)
    fig.update_layout(paper_bgcolor='rgb(169,169,169)')
    fig.show()
    return fig

@app.callback(Output('linegraphheader','children'),
            Output('singleforex','figure'),
              Output('content', 'children'),
            Input('futuresdropdown', 'value'),
            Input('hrly_timerange', 'value'))
def newlinegraphanddatatable(currencyname,hrlychoiceline):
    sqltablename = 'hrlytable_'+str(currencyname)
    hourlychosenmap = pd.read_sql_table(sqltablename, engine,index_col='index')
    
    lowestvalue = hourlychosenmap['Close'].max()
    highestvalue = hourlychosenmap['Close'].min()
    
    lastdatetimevalue = hourlychosenmap.index[-1]
    
    if hrlychoiceline == 182:
        sixmonths = lastdatetimevalue - relativedelta(months=6)
        hourlychosenmap = hourlychosenmap[hourlychosenmap.index > sixmonths]
    elif hrlychoiceline == 60:
        threemonths = lastdatetimevalue - relativedelta(months=3)
        hourlychosenmap = hourlychosenmap[hourlychosenmap.index > threemonths]    
    elif hrlychoiceline == 30:
        onemonth = lastdatetimevalue - relativedelta(months=1)
        hourlychosenmap = hourlychosenmap[hourlychosenmap.index > onemonth]           

    hourly_fig = go.Figure(data=go.Scatter(x = hourlychosenmap.index, y = hourlychosenmap.Close))
    hourly_fig.update_traces(line_color='#000000')
    hourly_fig.update_layout(paper_bgcolor='rgb(169,169,169)')

    if currencyname != "":
        sqlfuturesname = 'futures_' + str(currencyname)
        fut_datatable = pd.read_sql_table(sqlfuturesname, engine,index_col='index')
        xyz = dash_table.DataTable(id='futures_datatable',                   
                columns=[{"name": i, "id": i} for i in fut_datatable.columns],
                row_selectable='single',
                data=fut_datatable.to_dict('records'),
                style_data={'backgroundColor': 'transparent','align':"center"},
                style_cell={'fontSize':10, 'font-family':'sans-serif'})
        
    hourly_fig.update_layout(yaxis_range=[lowestvalue,highestvalue])
    hourly_fig.show()
    linechartheader = html.P(currencyname + "/USD Change in Value",style={'textAlign':'center','color':'black','font-weight':'700'})
    
    return linechartheader,hourly_fig,xyz

@app.callback(
    Output('content3','children'),
    Input('linegraphheader', "children"),
    Input('content','data'),
    Input('content','selected_rows'))
def docalculations(currname,data,selected_rows):
    
    var = str(currname['props'])

    var_partt = var.split('USD')[0]

    curr = var_partt[-4:-1]
    
    if len(curr) > 1:
        print(curr)
    
    # if selected_rows != None:
    #     print(data)
    #     print(currname)
    #     copy = str(data)
    #     copy_split = copy.split('}')
    #     print(copy_split)
    #     print("NOT NONE")
    #     print(selected_rows)
        
    htmlcalculator = html.P(curr)    
    
    return htmlcalculator

if __name__ == '__main__':
 #   app.run_server(host='0.0.0.0', port=8080, debug=True, use_reloader=False)
    app.run_server()

