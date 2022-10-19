#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 16 17:34:55 2022

@author: johnhope
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
from sklearn import preprocessing, svm
import statsmodels.tsa.api as smt
import statsmodels.api as sm
import pmdarima as pm
import os

os.chdir('/Users/johnhope/Desktop/DS 4002/Project 2')

# Reading in the dataset
data = pd.read_csv('Site Visits by Month.csv')

# Converting the date column to date objects
data['MonthYear']=pd.to_datetime(data['MonthYear'], format = '%Y.%m.%d').dt.date

# Subsetting to Amazon data
amazon_ts = data[data['Site']=='Amazon'][['MonthYear', 'All Devices']]
amazon_ts = amazon_ts['All Devices'].groupby(amazon_ts['MonthYear']).sum()

   
   
rolling_mean = amazon_ts.rolling(window=6).mean()    
rolling_std = amazon_ts.rolling(window=6).std()
plt.figure(figsize=(15,5))  
plt.ticklabel_format(useOffset=False, style='plain')    
plt.plot(amazon_ts[6:]/1000000000, label='Observed Values', color="black")    
plt.plot(rolling_mean/1000000000, 'g', label='Moving Average (MA'+str(6)+')',
             color="red")
plt.legend(loc='best')
plt.xlabel("Time")
plt.ylabel("Page Visits (in billions)")
plt.grid(True)
plt.show()

def find_outliers(ts, perc=0.01, figsize=(15,5)):
    ## fit svm
    scaler = preprocessing.StandardScaler()
    ts_scaled = scaler.fit_transform(ts.values.reshape(-1,1))
    model = svm.OneClassSVM(nu=perc, kernel="rbf", gamma=0.01)
    model.fit(ts_scaled)
    ## dtf output
    dtf_outliers = ts.to_frame(name="ts")
    dtf_outliers["index"] = range(len(ts))
    dtf_outliers["outlier"] = model.predict(ts_scaled)
    dtf_outliers["outlier"] = dtf_outliers["outlier"].apply(lambda
                                              x: 1 if x==-1 else 0)
    ## plot
    fig, ax = plt.subplots(figsize=figsize)
    ax.set(title="Outlier Detection: "
           +str(sum(dtf_outliers["outlier"]==1))+' Outliers Found')
    ax.plot(dtf_outliers["index"], dtf_outliers["ts"],
            color="black")
    ax.ticklabel_format(useOffset=False, style='plain')  
    ax.scatter(x=dtf_outliers[dtf_outliers["outlier"]==1]["index"],
               y=dtf_outliers[dtf_outliers["outlier"]==1]['ts'],
               color='red')
    plt.xlabel("Time")
    plt.ylabel("Page Visits (in billions)")
    ax.grid(True)
    plt.show()
    return dtf_outliers

dtf_outliers = find_outliers(amazon_ts, perc=0.05)

# Find Outliers index position
outliers_index_pos = dtf_outliers[dtf_outliers["outlier"]==1].index

# Drop outliers
amazon_ts=amazon_ts.drop(outliers_index_pos)

# Test Stationarity
adfuller_test = sm.tsa.stattools.adfuller(amazon_ts, maxlag=6,
                                          autolag="AIC")
print('ADF Test Statistics: ', adfuller_test[0])
print('Critical Statistic: ', adfuller_test[4]["5%"])
print('p-Value: ', round(adfuller_test[1],3))

# Not stationary and therefore we should use an AR-I-MA model instead of an ARMA

# Split data into testing and training

def split_train_test(ts, test=0.20, plot=True, figsize=(15,5)):

    if type(test) is float:
        split = int(len(ts)*(1-test))
        perc = test
    elif type(test) is str:
        split = ts.reset_index()[ 
                      ts.reset_index().iloc[:,0]==test].index[0]
        perc = round(len(ts[split:])/len(ts), 2)
    else:
        split = test
        perc = round(len(ts[split:])/len(ts), 2)
    print("--- splitting at index: ", split, "|", 
          ts.index[split], "| test size:", perc, " ---")
    
    ts_train = ts.head(split)
    ts_test = ts.tail(len(ts)-split)
    return ts_train, ts_test

ts_train, ts_test = split_train_test(amazon_ts)

# Create initial model to find ARIMA parameters
model = pm.auto_arima(amazon_ts, start_p=1, start_q=1, start_P=1, start_Q=1,
                     max_p=10, max_q=10, max_P=10, max_Q=10, m=12, seasonal=True,
                     stepwise=True, suppress_warnings=True, D=1, max_D=3,
                     error_action='ignore')


# Train Model with orders found
model = smt.SARIMAX(ts_train, order=(1,1,1),
                    seasonal_order=(1,1,1,12), 
                    exog=None, enforce_stationarity=False,
                    enforce_invertibility=False).fit()

dtf_train = ts_train.to_frame(name="ts")
dtf_train["model"] = model.fittedvalues
    
# Forecast to test data
dtf_test = ts_test.to_frame(name="ts")
forecast_vals = model.predict(start=len(ts_train), end=len(ts_train)+len(ts_test)-1, 
                              exog=None)
forecast_vals.index = ts_test.index
dtf_test["forecast"] = forecast_vals
dtf = dtf_train.append(dtf_test)


# Evaluating the model
dtf["residuals"] = dtf["ts"] - dtf["model"]
dtf["error"] = dtf["ts"] - dtf["forecast"]
dtf["error_pct"] = dtf["error"] / dtf["ts"]

## kpi
residuals_mean = dtf["residuals"].mean()
residuals_std = dtf["residuals"].std()
error_mean = dtf["error"].mean()
error_std = dtf["error"].std()
mae = dtf["error"].apply(lambda x: np.abs(x)).mean()
mape = dtf["error_pct"].apply(lambda x: np.abs(x)).mean()  
mse = dtf["error"].apply(lambda x: x**2).mean()
rmse = np.sqrt(mse)  #root mean squared error

## intervals
dtf["conf_int_low"] = dtf["forecast"] - 1.96*residuals_std
dtf["conf_int_up"] = dtf["forecast"] + 1.96*residuals_std
dtf["pred_int_low"] = dtf["forecast"] - 1.96*error_std
dtf["pred_int_up"] = dtf["forecast"] + 1.96*error_std



# Creating plots and evaluations
fig = plt.figure(figsize=(20,13))
fig.suptitle('SARIMA (1,1,1) x (1,1,1,12)', fontsize=20)   
ax1 = fig.add_subplot(2,2, 1)
ax2 = fig.add_subplot(2,2, 2, sharey=ax1)
ax3 = fig.add_subplot(2,2, 3)
ax4 = fig.add_subplot(2,2, 4)

### training
dtf[pd.notnull(dtf["model"])][["ts","model"]].plot(color=["black","green"], title="Model", grid=True, ax=ax1)      
ax1.set(xlabel=None)
### test
dtf[pd.isnull(dtf["model"])][["ts","forecast"]].plot(color=["black","red"], title="Forecast", grid=True, ax=ax2)
ax2.fill_between(x=dtf.index, y1=dtf['pred_int_low'], y2=dtf['pred_int_up'], color='b', alpha=0.2)
ax2.fill_between(x=dtf.index, y1=dtf['conf_int_low'], y2=dtf['conf_int_up'], color='b', alpha=0.3)     
ax2.set(xlabel=None)
### residuals
dtf[["residuals","error"]].plot(ax=ax3, color=["green","red"], title="Residuals", grid=True)
ax3.set(xlabel=None)
### residuals distribution
dtf[["residuals","error"]].plot(ax=ax4, color=["green","red"], kind='kde', title="Residuals Distribution", grid=True)
ax4.set(ylabel=None)
plt.show()
print("Training --> Residuals mean:", np.round(residuals_mean), " | std:", np.round(residuals_std))
print("Test --> Error mean:", np.round(error_mean), " | std:", np.round(error_std),
      " | mae:",np.round(mae), " | mape:",np.round(mape*100), "%  | mse:",np.round(mse), " | rmse:",np.round(rmse))


# Forecasting the future
forecast2 = model.predict(start=len(amazon_ts), end=len(amazon_ts)+11, 
                              exog=None)