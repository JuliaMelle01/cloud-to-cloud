import asyncio
import datetime
from carbon_budget import CurrentCarbonBudget
from fritzbox_api import RESTConnection
from calculator import Calculator
# Daily carbon budget per person
DAILY_CARBON_BUDGET = 0.205

# ENERGY_PER_INTERNET_TRAFFIC = 0.39
# CARBON_EMISSION_PER_ENERGY = 0.485
# CO2/kg
CARBON_PER_GB = 0.18915

NTOPNG_USER = "admin"
NTOPNG_PASSWORD = "admin_julia"


async def run_artefact():
    #loop = asyncio.get_running_loop()
    rest_connection = RESTConnection(NTOPNG_USER, NTOPNG_PASSWORD)
    carbon_budget = CurrentCarbonBudget(DAILY_CARBON_BUDGET)
    print(f"Start budget: {carbon_budget.carbon_budget}")
    while True:
        # every hour
        await asyncio.sleep(10)
        used_data = rest_connection.get_data()
        calculator = Calculator(used_data, CARBON_PER_GB)
        used_data = calculator.traffic_data_to_carbon()
        print(f"Used data: {used_data}")
        carbon_budget.update(used_data)
        print(f"Current budget left: {carbon_budget.carbon_budget}")



def main():
    asyncio.run(run_artefact())


if __name__ == "__main__":
    main()
