import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from analysis import calculateRentingStockReturns, calculateBuyHouseStockReturns

def runScenario(scenario):
  print('name: ', scenario['name'])
  print('\ntakeHomePay: ', scenario['takeHomePay'])
  print('\nrentPayments: ', scenario['rentPayments'])
  print('\notherOutgoings: ', scenario['otherOutgoings'])
  print('\nisaLimits: ', scenario['isaLimits'])
  print('\nstartIsa: ', scenario['startIsa'])
  print('\nstartTaxable: ', scenario['startTaxable'])
  print('\nhouseValue: ', scenario['houseValue'])
  print('\nbuyHouseCosts: ', scenario['buyHouseCosts'])
  print('\nstampDutyFunction: ', scenario['stampDutyFunction'])
  print('\nhouseDeposit: ', scenario['houseDeposit'])
  print('\nstockReturnPercent: ', scenario['stockReturnPercent'])
  print('\nyearlyHouseFixedCosts: ', scenario['yearlyHouseFixedCosts'])
  print('\nyearlyMortgagePercents: ', scenario['yearlyMortgagePercents'])
  print('\nhouseReturnsCumulativePercent: ', scenario['houseReturnsCumulativePercent'])
  print('\nmortgageLengthYears: ', scenario['mortgageLengthYears'])

  rentResults = calculateRentingStockReturns(scenario['startIsa'], scenario['startTaxable'], scenario['isaLimits'], scenario['stockReturnPercent'], scenario['takeHomePay'], scenario['rentPayments'], scenario['otherOutgoings'], scenario['years'])
  buyResults = calculateBuyHouseStockReturns(scenario['startIsa'], scenario['startTaxable'], scenario['isaLimits'], scenario['houseDeposit'], scenario['stampDutyFunction'], scenario['buyHouseCosts'], scenario['houseValue'], scenario['yearlyMortgagePercents'], scenario['houseReturnsCumulativePercent'], scenario['stockReturnPercent'], scenario['yearlyHouseFixedCosts'], scenario['takeHomePay'], scenario['otherOutgoings'], scenario['mortgageLengthYears'], scenario['years'])

  return rentResults.copy().add_prefix('rent_').merge(buyResults.add_prefix('buy_'), left_index=True, right_index=True)

# results.to_csv('output/results.csv')

def plotResults(results, scenario, plot = plt):
  print(results)
  start = scenario['startIsa'] + scenario['startTaxable']

  plot.plot(pd.concat([pd.Series([0]), results['buy_year']]), np.concatenate(([start], results['buy_totalValue'])) / 1000000, label='Buy house')
  plot.plot(pd.concat([pd.Series([0]), results['rent_year']]), np.concatenate(([start], results['rent_stockValue'])) / 1000000, label='Rent house')

  return plot

def showPlot(results, scenario):
  plot = plotResults(results, scenario)
  plot.xlabel('Year')
  plot.ylabel('Value (£mm)')
  plot.legend()
  plot.show(block=True)
