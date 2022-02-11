import json
import fileinput
import asyncio
from settings import (
    CARBON_PER_GB,
    DAILY_CARBON_BUDGET,
    DEGREE_PER_CARBON,
    GPIO_PIN_MOTOR,
    PATH_TO_AUDIO,
)
from carbon_budget import CurrentCarbonBudget
from calculator import Calculator
from artefact_interface import Artefact


class TrafficCapture:
    """
    Ongoing process to capture data traffic piped in via stdin.
    """

    def __init__(self):
        #: Capture data in bytes
        self.data = 0

    def update_data(self, json_packet):
        """
        Reads out the amount of data sent by a package and updates
        data value.

        :param json_packet: A tshark packet JSON
        """
        bytes_sent = json_packet["layers"]["ip"]["ip_ip_len"]
        print(f"bytes: {bytes_sent}")
        self.data += int(bytes_sent)

    def capture_data_traffic(self):
        """
        Captures ongoing stdin input stream from a pipe and
        converts it to a python JSON object.
        """
        # catches stdin input stream
        for line in fileinput.input():
            try:
                self.update_data(json.loads(line))
            except KeyError:
                continue


class RunArtefact:
    """
    Ongoing process which updates the artefacts state depending on the
    amount of captured data.
    """

    def __init__(self, traffic_capture):
        #: Hours since the artefact was reset (0-24)
        self.hours_since_reset = 0
        #: A TrafficCapture object from whom to read the amount of
        # data from
        self.traffic_capture = traffic_capture
        #: A CurrentCarbonBudget object to save the current carbon budget
        self.carbon_budget = CurrentCarbonBudget(DAILY_CARBON_BUDGET)
        #: An Artefact object to have an interface with the artefact
        self.artefact = Artefact(GPIO_PIN_MOTOR, PATH_TO_AUDIO)

    def between_callback(self):
        """
        Helper function to use asyncio module.
        """
        asyncio.run(self.run_artefact())

    async def run_artefact(self):
        """
        A method for controlling the artefact. It is called every hour and
        updates the artefact according to the used data.
        """
        self.artefact.reset()
        print("init")
        while True:
            # every minute
            await asyncio.sleep(60)
            self.hours_since_reset += 1
            print(f"hours: {self.hours_since_reset}")
            if self.hours_since_reset == 24:
                self.reset()
            else:
                self.update()

    def update(self):
        """
        A method which updates the carbon budget and artefact according to
        the used data.
        """
        used_data = self.traffic_capture.data
        print(f"used data: {used_data}")
        self.traffic_capture.data = 0
        calculator = Calculator(used_data, CARBON_PER_GB, DEGREE_PER_CARBON)
        self.carbon_budget.update(calculator.used_carbon)
        self.artefact.update(calculator.degrees_to_turn)
        print(f"budget: {self.carbon_budget.carbon_budget}")

    def reset(self):
        """
        A method resetting the hours_since_reset, the carbon budget and the
        state of the artefact.
        """
        self.hours_since_reset = 0
        self.carbon_budget.reset()
        self.artefact.reset()
