import json
import fileinput
import asyncio
from settings import CARBON_PER_GB, DAILY_CARBON_BUDGET, ANGLE_PER_CARBON, GPIO_PIN_MOTOR, PATH_TO_AUDIO
from carbon_budget import CurrentCarbonBudget
from calculator import Calculator
from artefact_interface import Artefact


class TrafficCapture:

    def __init__(self):
        self.data = 0

    def update_data(self, json_packet):
        bytes_sent = json_packet["layers"]["ip"]["ip_ip_len"]
        self.data += int(bytes_sent)

    def capture_data_traffic(self):
        for line in fileinput.input():
            try:
                self.update_data(json.loads(line))
            except KeyError:
                continue


class RunArtefact:
    """
    ...
    """
    def __init__(self, traffic_capture):
        self.hours_since_reset = 0
        self.traffic_capture = traffic_capture
        self.carbon_budget = CurrentCarbonBudget(DAILY_CARBON_BUDGET)
        self.artefact = Artefact(GPIO_PIN_MOTOR, PATH_TO_AUDIO)

    def between_callback(self):
        asyncio.run(self.run_artefact())

    async def run_artefact(self):
        self.artefact.reset()
        while True:
            # every minute
            await asyncio.sleep(60)
            self.hours_since_reset += 1
            if self.hours_since_reset == 24:
                self.reset()
            else:
                self.update()

    def update(self):
        used_data = self.traffic_capture.data
        calculator = Calculator(used_data, CARBON_PER_GB, ANGLE_PER_CARBON)
        self.carbon_budget.update(calculator.used_carbon)
        self.artefact.update(calculator.degrees_to_turn)

    def reset(self):
        self.hours_since_reset = 0
        self.carbon_budget.reset()
        self.artefact.reset()
