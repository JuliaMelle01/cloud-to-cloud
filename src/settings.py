import numpy as np

# Path to played audio file
PATH_TO_AUDIO = 'audio.mp3'

# Pin of raspberry pi for the motor
GPIO_PIN_MOTOR = 19

# Daily carbon budget per person
DAILY_CARBON_BUDGET = 0.205 / 60

# ENERGY_PER_INTERNET_TRAFFIC = 0.39
# CARBON_EMISSION_PER_ENERGY = 0.485
# CO2/kg
CARBON_PER_GB = 0.00485#0.18915

# Number of turns of the artefact per carbon use
# TODO: Check unit - degrees or position
ANGLE_PER_CARBON = np.floor(DAILY_CARBON_BUDGET / (15*360))
