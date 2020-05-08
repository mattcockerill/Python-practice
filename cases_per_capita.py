import urllib.request
import urllib.parse
import urllib.error
import json
import ssl
import time as tm
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import seaborn as sns

# covid data url
url = 'https://opendata.ecdc.europa.eu/covid19/casedistribution/json'

# print('Retrieving', url)
uh = urllib.request.urlopen(url)
data = uh.read().decode()
# print('Retrieved', len(data), 'characters')

# create dataframe from url data
js = json.loads(data)
lst = list(js['records'])
df = pd.DataFrame.from_dict(lst)

# get data into format we want
df = df[['countriesAndTerritories', 'cases', 'deaths', 'popData2018']]
df['cases'] = pd.to_numeric(df['cases'])
df['deaths'] = pd.to_numeric(df['deaths'])
df = df.groupby(['countriesAndTerritories', 'popData2018']).sum()
df.reset_index(inplace=True)

df['popData2018'] = pd.to_numeric(df['popData2018'])
df['cases'] = pd.to_numeric(df['cases'])
df['deaths'] = pd.to_numeric(df['deaths'])

df['casesPerCapita'] = df['cases']/df['popData2018']
df['deathsPerCapita'] = df['deaths']/df['popData2018']

# plot data
df.sort_values(by=['deathsPerCapita'], ascending=False)[:10].plot.bar(
    x='countriesAndTerritories', y='deathsPerCapita')
plt.xlabel("Country")
plt.ylabel("Deaths per capita")
plt.title("Top 10 Countries - Covid-19 deaths per capita")
plt.subplots_adjust( bottom=0.20)
plt.show()
