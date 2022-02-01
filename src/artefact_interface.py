from playsound import playsound
import RPi.GPIO as GPIO
import numpy as np


class Artefact:

    def __init__(self, gpip_pin_motor, path_to_audio):
        self.motor_pin = gpip_pin_motor
        self.audio_file = path_to_audio
        self.p = self.init_motor()
        self.current_position = 0 #TODO: check what is start setting

    def init_motor(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.motor_pin, GPIO.OUT)
        p = GPIO.PWM(self.motor_pin, 50)  # GPIO 17 als PWM mit 50Hz
        return p

    def update(self, degrees_to_turn):
        self.update_position(degrees_to_turn)
        if self.current_position <= 0:
            self.make_sound()
            self.current_position = 0

    def update_position(self, degrees_to_turn):
        self.p.start(0)  # Initialisierung
        number_of_circles = np.floor(degrees_to_turn/15)
        for n in range(number_of_circles):
            self.p.ChangeDutyCycle(100) #TODO: test if this is full circle and counter clockwise
        self.p.ChangeDutyCycle(degrees_to_turn % 15)
        self.p.stop()
        self.current_position -= degrees_to_turn

    def reset(self):
        self.update_position(self.current_position)
        for n in range(15):
            self.p.ChangeDutyCycle(-100)
        self.current_position = 0#TODO total value

    def make_sound(self):
        playsound(self.audio_file)
