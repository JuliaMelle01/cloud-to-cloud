import asyncio
import datetime
from carbon_budget import CurrentCarbonBudget
from fritzbox_api import TrafficCapture
from calculator import Calculator
import dpkt
import fileinput
import threading
# Daily carbon budget per person
DAILY_CARBON_BUDGET = 0.205

# ENERGY_PER_INTERNET_TRAFFIC = 0.39
# CARBON_EMISSION_PER_ENERGY = 0.485
# CO2/kg
CARBON_PER_GB = 0.18915

#NTOPNG_USER = "admin"
#NTOPNG_PASSWORD = "admin_julia"


async def run_artefact(traffic_capture):
    #loop = asyncio.get_running_loop()
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
    for line in fileinput.input(mode='rb'):
        try:
            traffic_capture.update_data(len(dpkt.ethernet.Ethernet(line).data))
        except dpkt.dpkt.NeedData:
            print("Warning: ")


def between_callback(args):
    asyncio.run(run_artefact(args))


def main():
    traffic_capture = TrafficCapture()
    threading.Thread(target=capture_data_traffic, args=[traffic_capture]).start()
    threading.Thread(target=between_callback, args=[traffic_capture]).start()


if __name__ == "__main__":
    main()
