import urllib.request, urllib.parse, urllib.error
import json
import ssl
import time as tm
import pandas as pd
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

countries = ['India', 'Germany', 'United_Kingdom', 'United_States_of_America', 'France', 'China']
df = df[df['countriesAndTerritories'].isin(countries)]
df = df.pivot(index = 'dateRep', columns = 'countriesAndTerritories', values = 'cases').cumsum()
countries = list(df.columns)
covid = df.reset_index('dateRep')
covid.set_index(['dateRep'], inplace=True)
covid.columns = countries
covid.rename(columns = {'United_Kingdom':'UK','United_States_of_America':'USA'}, inplace = True)

# Generating Colours and Style
colors = {'China':'#089099', 'France':'#7CCBA2', 'Germany':'#FCDE9C', 'India':'#045275', 'UK':'#7C1D6F', 'USA':'#DC3977'}
plt.style.use('fivethirtyeight')

# Section 7 - Creating the Visualization
plot = covid.plot(figsize=(9,6), color=list(colors.values()), linewidth=2, legend=False)
plot.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
plot.grid(color='#d4d4d4')
plot.set_xlabel('Date')
plot.set_ylabel('# of Cases')

# Assigning Colour
for country in list(colors.keys()):
    print(covid.index[-1], covid[country].max(), colors[country])
    plot.text(x = covid.index[-1], y = covid[country].max(), color = colors[country], s = country, fontsize = 8, weight = 'bold')

# Adding Labels
plot.text(x = covid.index[1], y = int(covid.max().max())+150000, s = "COVID-19 Cases by Country", fontsize = 16, weight = 'bold', alpha = .75)
plot.text(x = covid.index[1], y = int(covid.max().max())+15000, s = "For the USA, China, Germany, France, United Kingdom, and India\nIncludes Current Cases, Recoveries, and Deaths", fontsize = 11, alpha = .75)
plt.subplots_adjust(left = 0.16, bottom = 0.12, right = 0.86)
plt.show()
