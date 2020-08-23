import numpy as np
from helpers import stampDuty, covidStampDuty


years = 15

londonAverageHouseReturn = 0.09
ukAverageHouseReturn = 0.078
goodMortgageRate = np.repeat(0.011, years)
okMortgageRate = np.concatenate([np.arange(0.01, 0.03, 0.005), np.repeat(0.03, 100)])[:years]
badMortgageRate = np.concatenate([np.arange(0.01, 0.07, 0.005), np.repeat(0.07, 100)])[:years]

goodHouseReturns = np.cumsum(np.repeat(londonAverageHouseReturn,  years))
okHouseReturns = np.cumsum(np.repeat(ukAverageHouseReturn, years))
badHouseReturns = np.cumsum(np.repeat(0.04, years))
veryBadHouseReturns = np.cumsum(np.repeat(0.01, years))
flatHouseReturns = np.cumsum(np.repeat(0, years))
negativeHouseReturns = np.cumsum(np.repeat(-0.02, years))

snp500AverageReturns = np.repeat(0.1, years)

# last 10 years average
ukInflationAverage = 0.02

inflation = np.insert(np.cumprod(np.repeat(1 + ukInflationAverage, years - 1)), 0, 1)

wages = inflation * np.repeat(200000, years)

wagesPlateauSoon = inflation * np.concatenate([np.arange(100000, 150000, 5000), np.repeat(150000, 100)])[:years]

wagesGoBig = inflation * np.concatenate([np.arange(100000, 190000, 7000), np.repeat(190000, 100)])[:years]

# Remote working / part time?
wagesGoHome = inflation * np.concatenate([np.repeat(100000, 2), np.repeat(90000, years - 2)])

oneIncomeWages = inflation * np.concatenate([np.repeat(100000, 2), np.repeat(60000, years - 2)])

startIsa = 150000
startTaxable = 50000

def baseScenario():
  yearlyHouseReturn = 0.078

  return {
    'name': 'baseScenario',
    'takeHomePay': wages,
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
    # https://www.slickcharts.com/sp500/returns
    'stockReturnPercent': snp500AverageReturns,
    'yearlyMortgagePercents': okMortgageRate,
    # https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&ved=2ahUKEwjwxfzXkMjqAhWdQkEAHXJUChYQFjADegQIAxAB&url=https%3A%2F%2Fwww.nationwide.co.uk%2F-%2Fmedia%2FMainSite%2Fdocuments%2Fabout%2Fhouse-price-index%2Fdownloads%2Fuk-house-price-since-1952.xls&usg=AOvVaw2ZH1bqkJQpZXuaKLk6YytK
    'houseReturnsCumulativePercent': goodHouseReturns,
    'mortgageLengthYears': 25,
    'years': years
  }

def badMortgageRateScenario():
  scenario = baseScenario()
  scenario['name'] = 'Bad Mortgage Rates\n1% -> 7% in 0.5% increments each year'
  scenario['yearlyMortgagePercents'] = badMortgageRate
  return scenario

def goodMortgageRateScenario():
  scenario = baseScenario()
  scenario['name'] = 'Good Mortgage Rates\n1.1% forever'
  scenario['yearlyMortgagePercents'] = goodMortgageRate
  return scenario

def veryBadHouseReturnsScenario():
  scenario = baseScenario()
  scenario['name'] = 'Very Bad House Returns\n1% forever'
  scenario['houseReturnsCumulativePercent'] = veryBadHouseReturns
  return scenario

def badHouseReturnsScenario():
  scenario = baseScenario()
  scenario['name'] = 'Bad House Returns\n4%'
  scenario['houseReturnsCumulativePercent'] = badHouseReturns
  return scenario

def okHouseReturnsScenario():
  scenario = baseScenario()
  scenario['name'] = 'Historical UK house Returns'
  scenario['houseReturnsCumulativePercent'] = okHouseReturns
  return scenario

def goodHouseReturnsScenario():
  scenario = baseScenario()
  scenario['name'] = 'Historical London house Returns'
  scenario['houseReturnsCumulativePercent'] = goodHouseReturns
  return scenario


def flatHouseReturnsScenario():
  scenario = baseScenario()
  scenario['name'] = 'Flat House Returns (0%)'
  scenario['houseReturnsCumulativePercent'] = flatHouseReturns
  return scenario

def negativeHouseReturnsScenario():
  scenario = baseScenario()
  scenario['name'] = "Negative House Returns\n-2% a year"
  scenario['houseReturnsCumulativePercent'] = negativeHouseReturns
  return scenario

def stretchDepositScenario():
  scenario = baseScenario()
  houseDeposit = startIsa + startTaxable - 50000
  scenario['name'] = f'Stretch For House\nDeposit = £{houseDeposit}, House value = £900k'
  scenario['houseDeposit'] = startIsa + startTaxable - 50000
  scenario['houseValue'] = 900000
  return scenario


def veryGoodStockReturnsScenario():
  scenario = baseScenario()
  scenario['name'] = 'Above Average Stock Returns'
  scenario['stockReturnPercent'] = snp500AverageReturns + 0.02
  return scenario

def mildStockReturnsScenario():
  scenario = baseScenario()
  stockPercent = snp500AverageReturns - 0.02
  scenario['name'] = f'Below Average Stock Returns\n{int(stockPercent[0] * 100)}%'
  scenario['stockReturnPercent'] = stockPercent
  return scenario

def badStockReturnsScenario():
  scenario = baseScenario()
  stockReturns = snp500AverageReturns - 0.05
  scenario['name'] = f'Bad Stock Returns\n{int(stockReturns[0] * 100)}%'
  scenario['stockReturnPercent'] = stockReturns
  return scenario

def veryBadStockReturnsScenario():
  scenario = baseScenario()
  stockReturns = snp500AverageReturns - 0.08
  scenario['name'] = f'Very Bad Stock Returns\n{int(stockReturns[0] * 100)}%'
  scenario['stockReturnPercent'] = stockReturns
  return scenario

def flatStockReturnsScenario():
  scenario = baseScenario()
  np.repeat(0, years)
  scenario['name'] = 'Flat Stock Returns\n0%'
  scenario['stockReturnPercent'] = np.repeat(0, years)
  return scenario

def slightlyNegativeStockReturnsScenario():
  scenario = baseScenario()
  scenario['name'] = 'Slightly Negative Stock Returns\n-2%'
  scenario['stockReturnPercent'] = np.repeat(-0.02, years)
  return scenario

def wagesGoBigScenario():
  scenario = baseScenario()
  scenario['name'] = 'wagesGoBig'
  scenario['takeHomePay'] = wagesGoBig
  return scenario

def wagesPlateauSoonScenario():
  scenario = baseScenario()
  scenario['name'] = 'wagesPlateauSoon'
  scenario['takeHomePay'] = wagesPlateauSoon
  return scenario

def wagesGoHomeScenario():
  scenario = baseScenario()
  scenario['name'] = 'wagesGoHome'
  scenario['takeHomePay'] = wagesGoHome
  return scenario

def oneIncomeWagesScenario():
  scenario = baseScenario()
  scenario['name'] = 'oneIncomeWages'
  scenario['takeHomePay'] = oneIncomeWages
  return scenario



def debug():
  scenario = baseScenario()
  scenario['name'] = 'debug'
  scenario['startIsa'] = 300000
  scenario['startTaxable'] = 50000
  scenario['houseDeposit'] = 300000
  scenario['houseValue'] = 800000
  return scenario
