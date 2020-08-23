import numpy as np
import pandas as pd
from functools import reduce

def processSnp500Returns(file):
  dataFrame = pd.read_csv(file)
  dataFrame['snp500Return'] = dataFrame['return'] / 100
  dataFrame = dataFrame.drop(columns=['return'])
  print(dataFrame)
  return dataFrame

def processInflationRates(file):
  dataFrame = pd.read_csv(file)
  dataFrame['inflationRate'] = dataFrame['rate'] / 100
  dataFrame = dataFrame.drop(columns=['rate'])
  return dataFrame

def processRates(file, dateColumn, rateColumn, dateFormat = "%d %b %y"):
  dataFrame = pd.read_csv(file)
  dataFrame = dataFrame.rename(columns={dateColumn: "date", rateColumn: "rate"})
  dataFrame = dataFrame.filter(items=['date', 'rate'])
  dataFrame['date'] = pd.to_datetime(dataFrame['date'], format=dateFormat)
  dataFrame['year'] = dataFrame['date'].dt.year
  dataFrame = dataFrame.set_index('date').groupby(pd.Grouper(freq='Y')).mean()
  dataFrame = dataFrame.reset_index(drop=True)
  return dataFrame

def processMortgageRates():
  mortgageRates = processRates('./data/mortgageRates.csv', 'Date', 'Monthly interest rate of UK monetary financial institutions (excl. Central Bank) sterling 2 year (75% LTV) fixed rate mortgage to households (in percent) not seasonally adjusted              [b] [g] [c] [d]             IUMBV34')
  baseRates = processRates('./data/boeBaseRates.csv', 'Date Changed', 'Rate')
  baseRates['year'] = np.arange(baseRates.iloc[0]['year'], baseRates.iloc[-1]['year'] + 1, dtype=int)
  baseRates['rate'] = baseRates['rate'].bfill()
  rates = baseRates.merge(mortgageRates, how='left', on='year', suffixes=['Boe', 'Mortgage'])
  rates['estimatedFromBoeRate'] = rates['rateBoe'] + 1.37
  rates['diff'] = rates['estimatedFromBoeRate'] - rates['rateMortgage']
  rates['mortgageRate'] = rates['rateMortgage'].fillna(rates['estimatedFromBoeRate']) / 100
  print(rates)
  print('totalDifferenceToRealMortgageRate', rates['diff'].sum())
  return rates

def processHousePrices(file, prefix, dateFormat = "%d/%m/%Y"):
  dataFrame = pd.read_csv(file)
  dataFrame = dataFrame.filter(items=['Pivotable date', 'Average price All property types'])
  dataFrame = dataFrame.rename(columns={"Pivotable date": "date", "Average price All property types": "averagePrice"})
  dataFrame['date'] = pd.to_datetime(dataFrame['date'], format=dateFormat)
  dataFrame = dataFrame[dataFrame['date'].dt.month == 1]
  dataFrame['percentChange'] = dataFrame['averagePrice'].pct_change()
  dataFrame = dataFrame.iloc[1:]
  dataFrame['year'] = dataFrame['date'].dt.year
  dataFrame = dataFrame.drop(columns=['date'])
  dataFrame = dataFrame.rename(columns={"percentChange": f'{prefix}PercentChange', "averagePrice": f'{prefix}AveragePrice'})

  print(dataFrame)
  return dataFrame

if __name__ == "__main__":
  # house prices: https://landregistry.data.gov.uk/app/ukhpi/browse?from=1953-06-01&location=http%3A%2F%2Flandregistry.data.gov.uk%2Fid%2Fregion%2Funited-kingdom&to=2020-06-01
  ukHousePrices = processHousePrices('./data/historicalUkHousePrices.csv', 'uk')
  essexHousePrices = processHousePrices('./data/historicalEssexHousePrices.csv', 'essex', "%Y-%m-%d")
  kentHousePrices = processHousePrices('./data/historicalKentHousePrices.csv', 'kent', "%Y-%m-%d")
  hertfordshireHousePrices = processHousePrices('./data/historicalHertfordshireHousePrices.csv', 'hertfordshire', "%Y-%m-%d")
  londonHousePrices = processHousePrices('./data/historicalLondonHousePrices.csv', 'london', "%Y-%m-%d")

  housePrices = reduce(lambda  left,right: pd.merge(left,right,on=['year'], how='outer'), [ukHousePrices, essexHousePrices, kentHousePrices, hertfordshireHousePrices, londonHousePrices])
  print(housePrices)
  # https://www.bankofengland.co.uk/boeapps/database/FromShowColumns.asp?Travel=NIxAZxI3x&FromCategoryList=Yes&NewMeaningId=RFRM2Y,FR2Y90,FR2Y75&CategId=6&HighlightCatValueDisplay=Fixed%20rate%20mortgage,%202%20year
  # https://www.bankofengland.co.uk/boeapps/database/Bank-Rate.asp
  mortgageRates = processMortgageRates()
  mortgageRates = mortgageRates.drop(columns=['rateBoe','rateMortgage', 'estimatedFromBoeRate',	'diff'])
  # https://www.macrotrends.net/countries/GBR/united-kingdom/inflation-rate-cpi

  inflationRates = processInflationRates('./data/ukInflation.csv')

  # https://www.macrotrends.net/2526/sp-500-historical-annual-returns

  snp500Returns = processSnp500Returns('./data/snp500Returns.csv')
  historical = reduce(lambda  left,right: pd.merge(left,right,on=['year'], how='outer'), [housePrices, mortgageRates, inflationRates, snp500Returns])
  historical = historical[historical['year'] >= 1975][historical['year'] < 2020]
  print(historical)
  historical.to_csv('output/historical.csv', index=False)
