import matplotlib.pyplot as plt
import math

from scenarios import baseScenario, debug, goodMortgageRateScenario, badMortgageRateScenario, veryBadHouseReturnsScenario, badHouseReturnsScenario, okHouseReturnsScenario, goodHouseReturnsScenario, flatHouseReturnsScenario, negativeHouseReturnsScenario, stretchDepositScenario, veryGoodStockReturnsScenario, mildStockReturnsScenario, badStockReturnsScenario, veryBadStockReturnsScenario, flatStockReturnsScenario, slightlyNegativeStockReturnsScenario, wagesPlateauSoonScenario, wagesGoBigScenario, wagesGoHomeScenario, oneIncomeWagesScenario
from scenarioRunner import runScenario, plotResults
from plotHelpers import getAx

def main():
  scenarios = [
    baseScenario(),
    badMortgageRateScenario(),
    goodMortgageRateScenario(),
    veryBadHouseReturnsScenario(),
    badHouseReturnsScenario(),
    okHouseReturnsScenario(),
    goodHouseReturnsScenario(),
    flatHouseReturnsScenario(),
    negativeHouseReturnsScenario(),
    stretchDepositScenario(),
    veryGoodStockReturnsScenario(),
    mildStockReturnsScenario(),
    badStockReturnsScenario(),
    veryBadStockReturnsScenario(),
    flatStockReturnsScenario(),
    slightlyNegativeStockReturnsScenario()
    # wagesGoBigScenario(),
    # wagesPlateauSoonScenario(),
    # wagesGoHomeScenario(),
    # oneIncomeWagesScenario(),
    # debug()
  ]
  columns = 2
  rows = max(math.ceil(len(scenarios) / columns), 2)
  fig, axs = plt.subplots(ncols=columns, nrows=rows)
  for i, s in enumerate(scenarios):
    result = runScenario(s)
    result.to_csv(f"output/results{s['name']}.csv")
    ax = getAx(axs, i, columns)
    ax.set_title(s['name'])
    ax.set(xlabel='Year', ylabel='Value (£mm)')

    plotResults(result, s, ax)

  fig.subplots_adjust(wspace=0.1, hspace=2, left=0.05, right=0.97, top=0.95, bottom=0.05)
  axs.flatten()[0].legend(loc='upper center', bbox_to_anchor=(0.5, -0.62), ncol=3)

  fig.show()
  plt.show(block=True)

if __name__ == "__main__":
    main()
