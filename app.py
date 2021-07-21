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

engine = create_engine('sqlite:///forex.db')

currencies = ['JPY','GBP','EUR','AUD','NZD','CNY','HKD','SGD','INR','MXN','PHP','THB','MYR','ZAR','RUB']

def makeheatmapdf():
    df = pd.read_sql_table('heatmaptable', engine)
    df
    
    final_df = pd.DataFrame(columns=['Currency','First','Last'])
    for i in currencies:
        if i in df.columns:
            first_value = df[i].loc[~df[i].isnull()].iloc[0]
            last_value = df[i].loc[~df[i].isnull()].iloc[-1]
            final_df.loc[len(final_df.index)] = [i, first_value,last_value]
    final_df['Difference'] = final_df['Last'] - final_df['First']
    final_df['Percent Chg'] = final_df['Difference'] / final_df['First']
    final_df.reset_index()
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
                       'RUB':'RUS'
        }
    print(final_df)
    final_df['Currency'] = final_df['Currency'].map(country_convert)
    print(final_df)
    fig = px.choropleth(final_df, locations="Currency",
                    color="Percent Chg",
                    hover_name="Currency",
                    color_continuous_scale=px.colors.sequential.Plasma)
    return fig
    
fig = makeheatmapdf()


def linechart():
    pass



external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }
]

app = dash.Dash(__name__,
                external_stylesheets=external_stylesheets)


app.layout = html.Div(children=[
    html.H1(
        children='Foreign Exchange Arbitrage Dashboard',
        style={
            'textAlign': 'center'
        }
    ),
    html.Div(children='Jamie Stephens', style={
        'textAlign': 'center'
    }),
    html.Div([
    dcc.Graph(figure=fig)])
])

if __name__ == '__main__':
    app.run_server()