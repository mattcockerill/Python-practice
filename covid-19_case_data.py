import urllib.request, urllib.parse, urllib.error
import json
import ssl
import time as tm
import pandas as pd
import matplotlib, matplotlib.pyplot as plt
import seaborn as sns

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

df.set_index('dateRep')

# plot some graphs

# 10 largest countries by cases
# df.groupby('countriesAndTerritories')['cases'].sum().nlargest(10, 'first').plot(kind='bar')
# plt.show()
#
# 10 largest countries by deaths
# df.groupby('countriesAndTerritories')['deaths'].sum().nlargest(10, 'first').plot(kind='bar')
# plt.show()
# df.groupby('countriesAndTerritories').plot()

uk      = df[df['countriesAndTerritories'] == 'United_Kingdom'].sort_values(by = 'dateRep')
italy   = df[df['countriesAndTerritories'] == 'Italy'].sort_values(by = 'dateRep')

# cases
# uk.plot(x='dateRep', y='cases')
# italy.plot(x='dateRep', y='cases')
# plt.show()

# deaths
# uk.plot(x='dateRep', y='deaths')
# italy.plot(x='dateRep', y='deaths')
# plt.show()

# cumulative deaths and cases
# plt.plot(uk['dateRep'],uk['cases'].cumsum(), 'g-', label = 'UK - Cases')
# plt.plot(italy['dateRep'],italy['cases'].cumsum(), 'r-', label = 'Italy - Cases')
# plt.plot(uk['dateRep'],uk['deaths'].cumsum(), 'g--', label = 'UK - Deaths')
# plt.plot(italy['dateRep'],italy['deaths'].cumsum(), 'r--', label = 'Italy - Deaths')
# plt.legend()
# plt.show()

# cases divided by deaths
plt.plot(uk['dateRep'],uk['deaths']/uk['cases'])
plt.show()
