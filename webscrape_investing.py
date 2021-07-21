# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 17:14:39 2021

@author: Administrator
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import time

invest_list = ['https://www.investing.com/currencies/us-dollar-index-contracts'
#               ,'https://www.investing.com/currencies/gbp-usd-contracts',
#               'https://www.investing.com/currencies/usd-jpy-contracts',
#               'https://www.investing.com/currencies/eur-usd-contracts',
#               'https://www.investing.com/currencies/usd-mxn-contracts',
#               'https://www.investing.com/currencies/aud-usd-contracts',
#               'https://www.investing.com/currencies/nzd-usd-contracts',
#               'https://www.investing.com/currencies/usd-zar-contracts'
               ]

invest_dict = {}

driver = webdriver.Firefox(executable_path=r'C:\Users\Administrator\AppData\Local\Programs\Python\geckodriver\geckodriver.exe')

for i in invest_list:
    driver.get(i)
    wait = WebDriverWait(driver, 5)
    time.sleep(3)
    driver.refresh()
    table = driver.find_element_by_id('BarchartDataTable')
    
    xyz = table.text
    
    xyz = xyz[50:]
    
    xyz = xyz.splitlines()
    
    for i in xyz:
        
        i = i[:-10]
        i = i.split(' ')
        i.remove('')
        
       # i[1:2] = [''.join(map(str,i[1:2]))]
        
        print(i)
        print(type(i))
        print(i[1:9])
        
        
    length = len(xyz)
    
    print(length)