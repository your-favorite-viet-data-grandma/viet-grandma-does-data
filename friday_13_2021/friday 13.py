#!/usr/bin/env python
# coding: utf-8

# In[3]:


# Import yfinance package
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from meteostat import Stations, Daily
from wwo_hist import retrieve_hist_data
from datetime import date


# In[4]:



# Read and print the stock tickers that make up S&P500
tickers = pd.read_html(
    'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
print(tickers.head())


# In[4]:


tickers.pivot_table(index=['GICS Sector'],aggfunc={'Symbol':len})


# In[5]:


tickers[tickers['GICS Sector']=='Energy']


# In[42]:



# Get the data for this tickers from yahoo finance
data = yf.download(tickers.Symbol.to_list(),'1999-12-31','2021-8-8', auto_adjust=True)['Close']
print(data.head())


# In[43]:



# Get the data for this tickers from yahoo finance
data_vol = yf.download(tickers.Symbol.to_list(),'1999-12-31','2021-8-8', auto_adjust=True)['Volume']
print(data_vol.head())


# In[39]:


data_vol_reset=data_vol.reset_index()
# stock_price
stock_volume=pd.melt(data_vol_reset, id_vars=['Date'], var_name='ticker', value_name='value')
stock_volume.head()


# In[44]:


stock_price=data.reset_index()
# stock_price
transpose_stock_price=pd.melt(stock_price, id_vars=['Date'], var_name='ticker', value_name='value')


# In[45]:


transpose_stock_price['DoW']=transpose_stock_price['Date'].dt.day_name()
transpose_stock_price['Day']=transpose_stock_price['Date'].dt.day
transpose_stock_price.head()


# In[46]:


# stock_price[(stock_price['DoW']=='Friday')& (stock_price['Day']==13)]
transpose_stock_price['Friday_13']=False
transpose_stock_price.loc[(transpose_stock_price['DoW']=='Friday')& (transpose_stock_price['Day']==13),'Friday_13']=True
transpose_stock_price['Friday']=False
transpose_stock_price.loc[(transpose_stock_price['DoW']=='Friday'),'Friday']=True


# In[47]:


stock_price_by_type=transpose_stock_price.merge(tickers[['Symbol','GICS Sector']],
                                                left_on=['ticker'],right_on=['Symbol'])
stock_price_by_type.sample(20)


# In[48]:


stock_price_by_type.pivot_table(index=['Date'],columns=['GICS Sector'],
                                aggfunc={'value':np.mean}).reset_index().to_csv('stock_price.csv')


# In[ ]:


# Get weather stations ordered by distance to Vancouver, BC
stations = Stations(lat = 49.2497, lon = -123.1193, daily = datetime(2018, 1, 1))
# Fetch closest station (limit = 1)
station = stations.fetch(1)
# Get daily data for 2018 at the selected weather station
data = Daily(station, start = datetime(2018, 1, 1), end = datetime(2018, 12, 31))
# Fetch Pandas DataFrame
data = data.fetch()


# In[ ]:


frequency = 24
start_date = '01-JAN-2001'
end_date = '11-MAR-2019'
api_key = 'YOUR_API_KEY'
location_list = ['singapore','chicago']
hist_weather_data = retrieve_hist_data(api_key,
                                location_list,
                                start_date,
                                end_date,
                                frequency,
                                location_label = False,
                                export_csv = True,
                                store_df = True)


# In[49]:



# Set the start and end date
start_date = '2021-07-01'
end_date = '2021-07-12'

# Set the ticker
ticker = 'AMZN'

# Get the data
data = yf.download(ticker, start_date, end_date)
data = data.reset_index()
# Print 5 rows
data.tail()


# In[52]:


yf.Ticker('PFE').history(start="2010-01-01",  end='2020-07-21')


# In[84]:


datelist = pd.date_range(date(2000,1,1), periods=40000).tolist()
date_df=pd.DataFrame()


# In[85]:


date_df['Date']=datelist
date_df['Year']=date_df['Date'].dt.year
date_df['Week']=date_df['Date'].dt.week
date_df['ISO-Week'] = date_df['Date'] - pd.to_timedelta(date_df['Date'].dt.weekday, unit='D')
date_df['FridayOfWeek'] = date_df['ISO-Week'] + pd.to_timedelta(4, unit='D') 
date_df['WeekofFriday13']=0
date_df.loc[date_df['FridayOfWeek'].dt.day==13,'WeekofFriday13']=1


# In[97]:


date_df.pivot_table(index=['Year'],columns=['Week'],aggfunc={'WeekofFriday13':max}).reset_index().to_csv("years_and_fridays13.csv")


# In[102]:


date_df[(date_df['WeekofFriday13']==1)&(date_df['FridayOfWeek'].dt.day==13)&(date_df['Year']==2000)]


# In[ ]:




