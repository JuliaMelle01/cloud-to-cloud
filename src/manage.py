import asyncio
from carbon_budget import CurrentCarbonBudget
from fritzbox_api import TrafficCapture
from calculator import Calculator
import json
import fileinput
import threading
# Daily carbon budget per person
DAILY_CARBON_BUDGET = 0.205

# ENERGY_PER_INTERNET_TRAFFIC = 0.39
# CARBON_EMISSION_PER_ENERGY = 0.485
# CO2/kg
CARBON_PER_GB = 0.18915


async def run_artefact(traffic_capture):
    carbon_budget = CurrentCarbonBudget(DAILY_CARBON_BUDGET)
    print(f"Start budget: {carbon_budget.carbon_budget}")
    while True:
        # every hour
        await asyncio.sleep(10)
        used_data = traffic_capture.data
        calculator = Calculator(used_data, CARBON_PER_GB)
        used_data = calculator.traffic_data_to_carbon()
        print(f"Used data: {used_data}")
        carbon_budget.update(used_data)
        print(f"Current budget left: {carbon_budget.carbon_budget}")


def capture_data_traffic(traffic_capture):
    for line in fileinput.input():
        try:
            traffic_capture.update_data(json.loads(line))
        except KeyError:
            continue


def between_callback(args):
    asyncio.run(run_artefact(args))


def main():
    traffic_capture = TrafficCapture()
    threading.Thread(target=capture_data_traffic, args=[traffic_capture]).start()
    threading.Thread(target=between_callback, args=[traffic_capture]).start()


if __name__ == "__main__":
    main()
