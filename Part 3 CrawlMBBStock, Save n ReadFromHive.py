# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
# Part 1

import requests
import bs4
import json
import datetime
import pandas as pd
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
        #print(DFStock)
        #DFStock.to_csv(r"C:\Users\User\Documents\Data Mining\mbb.csv", sep=";", index=False, header=True)

# Part 2
from sqlalchemy import create_engine

engine = create_engine(f'hive://APP@localhost:10000/datamining')
engine.execute('CREATE TABLE mbb (date string, close string)')
DFStock.to_sql(name='mbb', con=engine, if_exists='append')

# Part 3
DFStock2 = DFStock
with engine.connect as con:
    DFStock2 = pd.read_sql("SELECT * FROM mbb", con)

print(DFStock2.describe)

print(DFStock2.isnull().sum())

print(DFStock2.dtypes)
