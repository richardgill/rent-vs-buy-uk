run:
	poetry run python src/main.py

processHistoricalData:
	poetry run python src/historicalData.py

historicalScenarios:
	poetry run python src/historicalScenarioRunner.py

install:
	poetry install
