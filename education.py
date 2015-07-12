from bs4 import BeautifulSoup
import requests
import sqlite3 as lite
import numpy as np

url = "http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm"

r = requests.get(url)

soup = BeautifulSoup(r.content)

# select records from correct web table, table 6
content_table = soup('table')[6].find_all("tr", class_="tcont")

# select only populated records
populated_table = [x for x in content_table if len(x)==25]

# create empty list to hold country and school life expectancy
countries = []

# select only populated rows from populated table and label
for rows in populated_table:
    col = rows.findAll('td')
    country = col[0].string
    year = col[1].string
    total = col[4].string
    men = col[7].string
    women = col[10].string
    record = (country, year, total, men, women)
    countries.append(record)

# name columns in pandas DataFrame
column_name = ['Country', 'Year', 'Total', 'Men', 'Women']

# create table and pair complete countries list with column names
education_table = pd.DataFrame(countries, columns = column_name)

# access GDP data from CSV file
dfComplete = pd.read_csv('ny.gdp.mktp.cd_Indicator_en_csv_v2.csv', skiprows=2)

# select columns for use in pandas DataFrame
# school life expectancy data only has data for years 1999 to 2010
# only select data for the appropriate period, 1999 to 2010
columns = ['Country Name','1999','2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010']

# create a new DataFrame that only displays data for the reduced period
dfReduced = pd.read_csv('ny.gdp.mktp.cd_Indicator_en_csv_v2.csv', skiprows=2, usecols=columns)

# drop any values without a country name
table.set_index('Country', inplace=True)
dfReduced.set_index('Country Name', inplace=True)

# merge the two DataFrames
combined_sets = pd.merge(table, dfReduced, how='inner', left_index=True, right_index=True)

# create new columns to match the year of the school life expectancy and GDP for that year
combined_sets['DataYear'] = combined_sets.apply(lambda x: x['Year'], axis=1)
combined_sets['GDP'] = combined_sets.apply(lambda x: x[x['Year']], axis=1)

# create a new column for log of GDP
finalDataFrame['logGDP'] = np.log(finalDataFrame['GDP'])
finalDataFrame.sort('GDP', ascending=True, inplace=True)

# plot school life expectancy against log of GDP
finalDataFrame.plot('Total', 'logGDP')
finalDataFrame.plot('Men', 'logGDP')
finalDataFrame.plot('Women', 'logGDP')
# plots indicate that school life expectancy increases as GDP increases

finalDataFrame.median()
# Total: 12, Men: 12, Women: 13
# Somewhat surprising given low school life expectancy in some regions
# Reflects that in high GDP countries women often have more education than men

finalDataFrame.std()
# Total: 3.11, Men: 2.79, Women: 3.80
# Reflects variation between high and low GDP countries
# Not surprising that women have a greater range then men
