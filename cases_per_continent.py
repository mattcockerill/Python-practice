import urllib.request, urllib.parse, urllib.error
import json
import ssl
import time as tm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import matplotlib.ticker as ticker

# covid data url
url = 'https://opendata.ecdc.europa.eu/covid19/casedistribution/json'

# print('Retrieving', url)
uh      = urllib.request.urlopen(url)
data    = uh.read().decode()
# print('Retrieved', len(data), 'characters')

# create dataframe from url data
js      = json.loads(data)
lst     = list(js['records'])
df      = pd.DataFrame.from_dict(lst)

# ensure we have the correct data types and set index
df['dateRep']       =   pd.to_datetime(df['dateRep'], dayfirst = True)
df['day']           =   pd.to_numeric(df['day'])
df['month']         =   pd.to_numeric(df['month'])
df['year']          =   pd.to_numeric(df['year'])
df['cases']         =   pd.to_numeric(df['cases'])
df['deaths']        =   pd.to_numeric(df['deaths'])
df['popData2028']   =   pd.to_numeric(df['popData2018'])

# # Restructure data

df = df.pivot_table(index = 'dateRep', columns = 'continentExp', values = 'deaths', aggfunc=np.sum).cumsum()
covid = df.reset_index('dateRep')
covid.set_index(['dateRep'], inplace=True)

# Creating the Visualization
plot = covid.plot(figsize=(9,6), linewidth=4, legend=True)
plot.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
plot.grid(color='#d4d4d4')
plot.set_xlabel('Date')
plot.set_ylabel('# of Cases')


# Adding Labels
plot.text(x = covid.index[1], y = int(covid.max().max())+50000, s = "COVID-19 Deaths by Continent", fontsize = 16, weight = 'bold', alpha = .75)
plt.subplots_adjust(left = 0.16, bottom = 0.12, right = 0.86)
plt.show()