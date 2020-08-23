import math

def rowIndex(i, columns):
  return math.floor(i / columns)

def columnIndex(i, columns):
  return i % columns

def getAx(axs, i, columns):
  return axs[rowIndex(i, columns)][columnIndex(i, columns)]
