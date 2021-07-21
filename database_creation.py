# -*- coding: utf-8 -*-
"""
Created on Tue Jul 20 03:10:28 2021

@author: Administrator
"""
import yfinance as yf
import sqlalchemy
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import datetime
from pytz import all_timezones
import pytz

currencies = ['JPY=X','GBPUSD=X','AUDUSD=X','NZDUSD=X','CNY=X','HKD=X','SGD=X','INR=X','MXN=X','PHP=X','THB=X','MYR=X','ZAR=X','RUB=X']
engine = create_engine('sqlite:///forex.db', echo = True)
meta = MetaData()

heat_df = pd.DataFrame()

for i in currencies:
    j = i[0:3]
    df = yf.download(tickers = i,period='1y',interval='1h')
    df = df.reset_index()
    del df['Volume']
    del df['Adj Close']
    table_name = 'hrlytable_' + j
    df.to_sql(table_name,engine)
    
    df_1 = yf.download(tickers=i,period='7d',interval='1m')
    
    df_1.tz_convert('Europe/London')
    
    #local1 = pytz.timezone("Europe/London")
    #local_dt1 = local1.localize(df_1, is_dst=None)
    #df_1 = df_1 = df_1.tz_localize(tz = 'Europe / London')
   # df_1.index = df_1.index.tz_convert(pytz.utc)
    df_1 = df_1.reset_index()
    
    table_name = 'minutetable_' + j
    df_1.to_sql(table_name,engine)
    
    selected_columns = df_1[['Datetime']]
    
    if heat_df.empty:
        f = datetime.datetime.now().replace(second=00).replace(microsecond=0)
        days = datetime.timedelta(7)
        g = f - days
        rng = pd.date_range(g, periods=10080, freq='T')
        heat_df['Datetime'] = rng
        heat_df = heat_df.set_index('Datetime')
        heat_df = heat_df = heat_df.tz_localize(tz = 'Europe/London')
        
        #f = datetime.datetime.now().replace(second=00).replace(microsecond=0)
        #days = datetime.timedelta(7)
        
        #local = pytz.timezone("US/Eastern")
        #local_dt = local.localize(f, is_dst=None)
        #utc_dt = local_dt.astimezone(pytz.utc)
        #g = f - days
        #rng = pd.date_range(g, periods=10080, freq='T')
        #print(type(rng))
        #heat_df['Datetime'] = rng
    del df_1['Open']
    del df_1['High']
    del df_1['Low']
    heat_df = pd.merge(heat_df,df_1,on='Datetime',how='outer')
    heat_df.rename(columns={ heat_df.columns[-1]: j }, inplace = True)  
 #   heat_df.set_axis([*heat_df.columns[:-1], j], axis=1, inplace=False)
    

print(heat_df)

heat_df.to_csv('test.csv')

#driver = webdriver.Firefox()
#driver.get("http://www.python.org")