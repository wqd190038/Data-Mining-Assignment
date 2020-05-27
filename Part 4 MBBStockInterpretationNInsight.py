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

page = requests.get("https://finance.yahoo.com/quote/%5EKLSE%3FP%3D%5EKLSE/history?period1=946857600&period2=1583539200&interval=1d&filter=history&frequency=1d")
DFBursa = pd.DataFrame(columns=['date','close'])

soup = BeautifulSoup(page.content, 'html.parser')

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
                DFBursa = DFBursa.append({"date":txtDate, "close":txtClose}, ignore_index=True)

# Part 4
import matplotlib.pyplot as plt

# Explore data
print(DFStock.describe)

print(DFStock.isnull().sum())

print(DFStock.dtypes)

# Trend Analysis
DFa = pd.DataFrame(columns=['date','close'])
DFa['date'] = pd.to_datetime(DFStock['date'], format='%Y-%m-%d')
DFa['close'] = DFStock['close']

plt.figure(figsize=(27,8))
plt.plot(DFa['date'], DFa['close'], label='Close Price')
plt.ylim(2,12)
plt.xlabel('Date (Year)')
plt.ylabel('Stock Price (RM)')
plt.title('Maybank Stock Price Trend (2000 - 2018)')
plt.show()

# Statistics
import numpy as np
print("Mean : {}".format(np.mean(DFa['close'])))
print("Min. : {}".format(np.nanmin(DFa['close'])))
print("Max. : {}".format(np.nanmax(DFa['close'])))
percentile = [0, 25, 50, 75, 90, 100]
for perc in percentile:
    print("{} : {}".format(perc, np.percentile(DFa['close'], perc)))

# Long Short Term Memory
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM

temp = DFStock.sort_index(ascending=True, axis=0)
DFB = pd.DataFrame(index=range(0,len(DFStock)), columns=['date','close'])
for i in range(0, len(temp)):
    DFB['date'][i] = temp['date'][i]
    DFB['close'][i] = temp['close'][i]

DFB.index = DFB.date
DFB.drop('date', axis=1, inplace=True)

dataset = DFB.values
train = dataset[0:int(len(temp)*0.6),:]
valid = dataset[int(len(temp)*0.6):,:]

scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(dataset)

XTrain, YTrain = [], []
for i in range(60, len(train)):
    XTrain.append(scaled_data[i-60:i,0])
    YTrain.append(scaled_data[i,0])
XTrain, YTrain = np.array(XTrain), np.array(YTrain)
XTrain = np.reshape(XTrain, (XTrain.shape[0], XTrain.shape[1], 1))

model = Sequential()
model.add(LSTM(units=50, return_sequences=True, input_shape=(XTrain.shape[1],1)))
model.add(LSTM(units=50))
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer='adam')
model.fit(XTrain, YTrain, epochs=1, batch_size=1, verbose=2)

inputs = DFB[len(DFB) - len(valid) - 60:].values
inputs = inputs.reshape(-1,1)
inputs = scaler.transform(inputs)

XTest = []
for i in range(60, inputs.shape[0]):
    XTest.append(inputs[i-60:i,0])
XTest = np.array(XTest)
XTest = np.reshape(XTest, (XTest.shape[0], XTest.shape[1], 1))

close_price = model.predict(XTest)
close_price = scaler.inverse_transform(close_price)

train = DFB[:int(len(temp)*0.6)]
valid = DFB[int(len(temp)*0.6):]
valid['prediction'] = close_price

plt.figure(figsize=(27,8))
plt.plot(train['close'])
plt.plot(valid[['close','prediction']])
plt.xlabel('Date (Year)')
plt.ylabel('Stock Price (RM)')
plt.title('Maybank Stock Price Trend with LSTM (2000 - 2018)')

# 2 trends in same graph
fig,ax = plt.subplots(figsize=(27,8))
ax.plot(DFStock['date'], DFStock['close'], color="red")
ax.set_xlabel("date")
ax.set_ylabel("MBB close")
ax2 = ax.twinx()
ax2.plot(DFBursa['date'], DFBursa['close'], color="blue")
ax2.set_ylabel("KLSE close")
plt.show()

# Correlation between MBB stock price and KLSE index
DFAll = DFStock.merge(DFBursa, on="date", suffixes=("mbb","klse"))
print(DFAll.corr(method="pearson"))

# Scatter Plot
plt.figure(figsize=(17,8))
plt.scatter(DFAll.closembb, DFAll.closeklse)
