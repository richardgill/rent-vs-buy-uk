def stampDutyFirstHome(houseValue):
  if houseValue > 500000:
    return stampDuty(houseValue)
  else:
    return max(0, houseValue - 300000) * 0.05

def stampDuty(houseValue):
  return max(0, houseValue - 1500000) * 0.12 + min(max(0, (houseValue - 925001)), 1500000 - 925001) * 0.1 + min(max(0, (houseValue - 250001)), 925001 - 250001) * 0.05 + min(max(0, (houseValue - 125001)), 250001 - 125001) * 0.02

def covidStampDuty(houseValue):
  return max(0, houseValue - 1500000) * 0.12 + min(max(0, (houseValue - 925001)), 1500000 - 925001) * 0.1 + min(max(0, (houseValue - 500001)), 925001 - 500001) * 0.05
