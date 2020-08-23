import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

from scenarios import baseScenario
from scenarioRunner import runScenario, plotResults
from helpers import stampDuty, covidStampDuty
from plotHelpers import getAx

startIsa = 150000
startTaxable = 50000

def scenario(historicalData):
  years = len(historicalData)
  inflation = np.cumprod(historicalData['inflationRate'].to_numpy() + 1)
  print('inflation: ', inflation)
  houseReturnsCumulativePercent = np.cumprod(historicalData['ukPercentChange'].to_numpy() + 1)
  print('houseReturnsCumulativePercent: ', houseReturnsCumulativePercent)
  return {
    'name': 'historical',
    'takeHomePay': inflation * np.repeat(200000, years),
    'rentPayments': inflation * np.repeat(2000 * 12, years),
    'otherOutgoings': inflation * np.repeat(4000 * 12, years),
    'yearlyHouseFixedCosts': inflation * np.repeat(2000, years),
    'isaLimits': inflation * np.repeat(40000, years),
    'startIsa': startIsa,
    'startTaxable': startTaxable,
    'houseValue': 700000,
    'buyHouseCosts': 3000,
    'stampDutyFunction': stampDuty,
    'houseDeposit': 165000,
    'stockReturnPercent': historicalData['snp500Return'].to_numpy(),
    'yearlyMortgagePercents': historicalData['mortgageRate'].to_numpy(),
    'houseReturnsCumulativePercent': houseReturnsCumulativePercent,
    'mortgageLengthYears': 25,
    'years': years
  }

def main():
  historicalData = pd.read_csv('./output/historical.csv')
  historicalData = historicalData.sort_values(by=['year'])
  firstYear = historicalData.head(1)['year'][0]
  years = 20

  periodCount = len(historicalData) - years
  periods = [historicalData.iloc[i:].head(years) for i in np.arange(0, periodCount)]

  scenarios = [scenario(period) for period in periods]
  columns = 2
  rows = math.ceil(periodCount / columns) + 1
  fig, axs = plt.subplots(ncols=columns, nrows=rows)
  mortgageRateAx = getAx(axs, 0, columns)
  mortgageRateAx.plot(historicalData.year, historicalData.mortgageRate, label='Mortgage interest rate')
  mortgageRateAx.set_title('Mortgage Rate')

  mortgageRateAx = getAx(axs, 1, columns)
  mortgageRateAx.plot(historicalData.year, np.cumprod(historicalData.ukPercentChange + 1), label='UK house prices')
  mortgageRateAx.set_title('UK house prices')

  mortgageRateAx = getAx(axs, 2, columns)
  mortgageRateAx.plot(historicalData.year, np.cumprod(historicalData.snp500Return + 1), label='SnP500 returns')
  mortgageRateAx.set_title('SnP500 returns')
  for i, s in enumerate(scenarios):
    result = runScenario(s)
    result.to_csv(f'output/resultsYear{i}.csv')
    ax = getAx(axs, i + 3, columns)
    yearStart = firstYear + i
    ax.set_title(f"{yearStart} - {yearStart + years}")
    ax.set(xlabel='Year', ylabel='Value (£mm)')
    plotResults(result, s, ax)

  fig.subplots_adjust(wspace=0.1, hspace=2, left=0.06, right=0.97, top=0.95, bottom=0.05)

  fig.show()

  axs.flatten()[3].legend(loc='upper center', bbox_to_anchor=(0.5, -0.62), ncol=3)
  figure = plt.gcf() # get current figure
  figure.set_size_inches(14, 24)

  plt.savefig("myplot.png", dpi = 200)


if __name__ == "__main__":
    main()
