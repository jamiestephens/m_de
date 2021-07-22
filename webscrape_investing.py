# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 17:14:39 2021

@author: Administrator
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import time
import pandas as pd
import sqlalchemy
from selenium.webdriver.firefox.options import Options
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
gbl = globals()

invest_dict = {'https://www.investing.com/currencies/us-dollar-index-contracts':'USD',
               'https://www.investing.com/currencies/gbp-usd-contracts':'GBP',
               'https://www.investing.com/currencies/usd-jpy-contracts':'JPY',
               'https://www.investing.com/currencies/eur-usd-contracts':'EUR',
               'https://www.investing.com/currencies/usd-mxn-contracts':'MXN',
               'https://www.investing.com/currencies/aud-usd-contracts':'AUD',
               'https://www.investing.com/currencies/nzd-usd-contracts':'NZD',
               'https://www.investing.com/currencies/usd-zar-contracts':'ZAR'
               }

investing_df = pd.DataFrame()

opts = Options()
opts.set_headless()
assert opts.headless

driver = webdriver.Firefox(executable_path=r'C:\Users\Administrator\AppData\Local\Programs\Python\geckodriver\geckodriver.exe', options=opts)

engine = create_engine('sqlite:///forex.db')
meta = MetaData()

for k,r in invest_dict.items():
    driver.get(k)
    wait = WebDriverWait(driver, 5)
    time.sleep(3)
    driver.refresh()
    table = driver.find_element_by_id('BarchartDataTable')
    
    xyz = table.text
    
    xyz = xyz[50:]
    
    xyz = xyz.splitlines()
    
    df_name = "futures_"+str(r)

    temp_df = pd.DataFrame(columns=['Expiration','Last',
                                                   'Change','Open','High',
                                                   'Low','Volume','Time'])
    
    counter = 0
    for i in xyz:
        i = i[:-10]
        j = i.split(' ')
        j.remove('')
        
        if counter > 0:
            new_j0 = str(j[0]) + " " + str(j[1])
            del j[:2]
            j.insert(0,new_j0)
        
        counter += 1
        j_series = pd.Series(j, index = temp_df.columns)
        temp_df = temp_df.append(j_series,ignore_index=True)
        
    
    
    gbl[df_name] = temp_df.copy()
    print(gbl["futures_"+str(r)])
    gbl[df_name].to_sql(df_name,engine,if_exists='replace')
    
