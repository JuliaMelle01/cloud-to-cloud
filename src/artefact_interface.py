from playsound import playsound
import RPi.GPIO as GPIO
import math


class Artefact:
    """
    The artefact class is for describing and updating the state of the
    artefact. 
    """

    def __init__(self, gpio_pin_motor, path_to_audio):
        #: The source gpio pin the motor is connected to  
        self.motor_pin = gpio_pin_motor
        #: Path to the played audio file
        self.audio_file = path_to_audio
        #: Initializing of the connection to the motor
        self.p = self.init_motor()
        #: Current position of the motor
        self.current_position = 0 #TODO: check what is start setting

    def init_motor(self):
        """
        Initializes the GPIO pins and connects the raspberry pi with 
        the motor. Turns motor to the start postion.
        
        :return: 
        """
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.motor_pin, GPIO.OUT)
        p = GPIO.PWM(self.motor_pin, 50)  # GPIO 17 als PWM mit 50Hz
        return p

    def update(self, degrees_to_turn):
        """
        Updates the artefact by calling the according update methods for changing
        the position of the motor and in case the remaining budget - the motor has 
        turned 15 times - is 0 or just 10% percent left a sound is played.
        
        :param degrees_to_turn: int describing how many degrees to turn 
        """
        self.update_position(degrees_to_turn)
        if self.current_psotion <= 10:
            self.make_sound()
        if self.current_position <= 0:
            self.make_sound()
            self.make_sound()
            self.current_position = 0

    def update_position(self, degrees_to_turn):
        """
        Updates the artefact motor by changing the position of the motor
        and adapts the current postion.
        
        :param degrees_to_turn: int describing how many degrees to turn 
        """
        self.p.start(0)  # Initialisierung
        number_of_circles = math.floor(degrees_to_turn/15)
        for n in range(number_of_circles):
            self.p.ChangeDutyCycle(100) #TODO: test if this is full circle and counter clockwise
        self.p.ChangeDutyCycle(degrees_to_turn % 15)
        self.p.stop()
        self.current_position -= degrees_to_turn

    def reset(self):
        """
        Resets the artefact motor by changing the position of the motor
        and resets the current postion to zero.
        """
        self.update_position(self.current_position)
        for n in range(15):
            self.p.ChangeDutyCycle(100) #TODO:change value
        self.current_position = 0 #TODO total value

    def make_sound(self):
        """
        Plays an mp3 audio file via a speaker.
        """
        playsound(self.audio_file)
