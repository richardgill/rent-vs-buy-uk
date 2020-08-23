import numpy as np
import pandas as pd

capitalGainsTaxRate = 0.2

def calculateRentingStockReturns(startIsa, startTaxable, isaLimits, yearlyReturnPercents, takeHomePay, rentPayments, otherOutgoings, years):
  dataFrame = pd.DataFrame({
     'yearlyReturnPercent': yearlyReturnPercents,
     'takeHomePay': takeHomePay,
     'rentPayment': rentPayments,
     'otherOutgoings': otherOutgoings,
     'isaLimit': isaLimits,
  })
  dataFrame['toInvest'] = dataFrame['takeHomePay'] - (dataFrame['rentPayment'] + dataFrame['otherOutgoings'])
  return calculateStockReturns(startIsa, startTaxable, dataFrame, years)

def principleRepayment(mortgagePercent, mortgageYearsRemaining, mortgageDebtRemaining):
  if mortgageYearsRemaining > 0 and mortgageDebtRemaining > 0:
    return -1 * np.ppmt(mortgagePercent, np.arange(mortgageYearsRemaining) + 1, mortgageYearsRemaining, mortgageDebtRemaining)[0]
  else:
    return 0

def interestRepayment(mortgagePercent, mortgageYearsRemaining, mortgageDebtRemaining):
  if mortgageYearsRemaining > 0 and mortgageDebtRemaining > 0:
    return -1 * np.ipmt(mortgagePercent, np.arange(mortgageYearsRemaining) + 1, mortgageYearsRemaining, mortgageDebtRemaining)[0]
  else:
    return 0

def calculateBuyHouseStockReturns(startIsa, startTaxable, isaLimits, deposit, stampDutyFunction, buyHouseCosts, houseValue, yearlyMortgagePercents, houseReturnsCumulativePercent, yearlyReturnPercents, yearlyHouseFixedCosts, takeHomePay, otherOutgoings, mortgageLengthYears, years):
  dataFrame = pd.DataFrame({
     'yearlyMortgagePercent': yearlyMortgagePercents,
     'houseReturnsCumulativePercent': houseReturnsCumulativePercent,
     'yearlyReturnPercent': yearlyReturnPercents,
     'yearlyHouseFixedCost': yearlyHouseFixedCosts,
     'takeHomePay': takeHomePay,
     'otherOutgoings': otherOutgoings,
     'isaLimit': isaLimits,
  })

  for row in dataFrame.itertuples():
    if row.Index == 0:
      housePrinciple = deposit
      mortgageDebtRemaining = houseValue - deposit
    else:
      previousRow = dataFrame.loc[row.Index - 1]
      mortgageDebtRemaining = previousRow.mortgageDebtRemaining
      housePrinciple = previousRow.housePrinciple
    mortgageYearsRemaining = mortgageLengthYears - row.Index
    mortgagePrincipleRepayment = principleRepayment(row.yearlyMortgagePercent, mortgageYearsRemaining, mortgageDebtRemaining)
    mortgageInterestRepayment = interestRepayment(row.yearlyMortgagePercent, mortgageYearsRemaining, mortgageDebtRemaining)
    mortgageRepayment = mortgageInterestRepayment + mortgagePrincipleRepayment
    dataFrame.at[row.Index, 'mortgagePrincipleRepayment'] = np.int64(mortgagePrincipleRepayment)
    dataFrame.at[row.Index, 'mortgageInterestRepayment'] = np.int64(mortgageInterestRepayment)
    dataFrame.at[row.Index, 'mortgageRepayment'] = np.int64(mortgageRepayment)
    dataFrame.at[row.Index, 'mortgageDebtRemaining'] = np.int64(mortgageDebtRemaining - mortgagePrincipleRepayment)
    dataFrame.at[row.Index, 'housePrinciple'] = np.int64(housePrinciple + mortgagePrincipleRepayment)

  dataFrame['percentOfHouseOwned'] = dataFrame['housePrinciple'] / houseValue
  dataFrame['currentHouseValue'] = houseValue * ( 1 + dataFrame['houseReturnsCumulativePercent'])
  dataFrame['currentHouseValueOwned'] = dataFrame['currentHouseValue'] * dataFrame['percentOfHouseOwned']
  dataFrame['toInvest'] = dataFrame['takeHomePay'] - (dataFrame['mortgageRepayment'] + dataFrame['otherOutgoings'] + dataFrame['yearlyHouseFixedCost'])
  print('stampDuty: ', stampDutyFunction(houseValue))
  spent = deposit + stampDutyFunction(houseValue) + buyHouseCosts
  print('spent', spent)
  if spent > (startTaxable + startIsa):
    raise "You went bankrupt :("
  startTaxableAmount = max(0, startTaxable - spent)
  startIsaAmount = max(0, startIsa - (spent - startTaxable))
  print('startTaxableAmount', startTaxableAmount)
  print('startIsaAmount', startIsaAmount)
  dataFrame = calculateStockReturns(startIsaAmount, startTaxableAmount, dataFrame, years)
  dataFrame['totalValue'] = dataFrame['currentHouseValueOwned'] + dataFrame['stockValue']
  return dataFrame

def calculateStockReturns(startIsaAmount, startTaxableAmount, inputDataFrame, years):
  dataFrame = inputDataFrame.head(years)
  dataFrame['year'] = np.arange(1, years + 1)
  dataFrame['toInvestIsa'] = dataFrame[['toInvest', 'isaLimit']].min(axis=1)
  dataFrame['toInvestTaxable'] = (dataFrame['toInvest'] - dataFrame['isaLimit']).clip(lower=0)#.apply(lambda toInvest: max(toInvest - 20000, 0))
  for row in dataFrame.itertuples():
    interestPercent = row.yearlyReturnPercent
    if row.Index == 0:
      isaInterest = startIsaAmount * interestPercent
      isaStockValue = startIsaAmount + row.toInvestIsa + isaInterest
      taxableInterest = startTaxableAmount * (interestPercent * (1 - capitalGainsTaxRate))
      taxableStockValue = startTaxableAmount + row.toInvestTaxable + taxableInterest
    else:
      previousRow = dataFrame.loc[row.Index - 1]
      isaInterest = previousRow.isaStockValue * row.yearlyReturnPercent
      isaStockValue = previousRow.isaStockValue + previousRow.toInvestIsa + isaInterest
      taxableInterest = previousRow.taxableStockValue * (row.yearlyReturnPercent * (1 - capitalGainsTaxRate))
      taxableStockValue = previousRow.taxableStockValue + previousRow.toInvestTaxable + taxableInterest

    dataFrame.at[row.Index, 'isaInterest'] = np.int64(isaInterest)
    dataFrame.at[row.Index, 'isaStockValue'] = np.int64(isaStockValue)
    dataFrame.at[row.Index, 'taxableInterest'] = np.int64(taxableInterest)
    dataFrame.at[row.Index, 'taxableStockValue'] = np.int64(taxableStockValue)
  dataFrame['stockValue'] = dataFrame['isaStockValue'] + dataFrame['taxableStockValue']
  return dataFrame
