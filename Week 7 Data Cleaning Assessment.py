# -*- coding: utf-8 -*-
"""
Created on Fri May  8 20:15:22 2020

@author: User
"""

import requests
import bs4
import json
import datetime
import pandas as pd
import re
page = requests.get("https://finance.yahoo.com/quote/1155.KL/history?period1=946857600&period2=1583539200&interval=1d&filter=history&frequency=1d")
DFStock = pd.DataFrame(columns=['date','close'])

from bs4 import BeautifulSoup
soup = BeautifulSoup(page.content, 'html.parser')
#print(soup.prettify())

listScript = soup.find_all("script")
for script in listScript:
    txtScript = script.string
    if type(txtScript) is bs4.element.NavigableString and txtScript.find('HistoricalPriceStore') != -1:
        txtInfo = txtScript[txtScript.find('HistoricalPriceStore'):txtScript.find('}],"isPending":false,"firstTradeDate":')]
        txtInfo = "{\"" + txtInfo + "}]}}"
        objJson = json.loads(txtInfo)
        for price in objJson['HistoricalPriceStore']['prices']:
            txtDate = ""
            txtClose = ""
            for attr,val in price.items():
                if attr == "date" and val != None:
                    txtDate = datetime.datetime.fromtimestamp(val).strftime('%Y-%m-%d')
                if attr == "close" and val != None:
                    txtClose = float(val)
            if txtDate != "" and txtClose != "":
                DFStock = DFStock.append({"date":txtDate, "close":txtClose}, ignore_index=True)

print(DFStock.info)
                
print(DFStock.describe())

print(DFStock.isnull().sum())

print(type(DFStock['date'][0]))
        
invalid_count = 0
for dt in DFStock['date']:
    if (not re.search("^[\d]{4}[\-]{1}[\d]{2}[\-]{1}[\d]{2}$", dt)):
        invalid_count += 1
print(invalid_count)
                
print(type(DFStock['close'][0]))