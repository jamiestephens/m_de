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


jpy = yf.download(tickers = 'JPYAUD=X' ,period ='2d', interval = '1m')

jpy =  jpy.reset_index()

fig = px.line(jpy, x="Datetime", y="Adj Close", title='JPY to AUD')

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
    })
])
app.run_server(debug=False)