#import playsound
import RPi.GPIO as GPIO
import math
import vlc


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
        self.current_position = 0  # TODO: check what is start setting
        #: Bool for ensuring just one warning for 10 percent
        # left
        self.not_warned_10_percent = True
        #: Bool for ensuring just one warning for budget
        # used up
        self.not_warned_used_up = True

    def init_motor(self):
        """
        Initializes the GPIO pins and connects the raspberry pi with
        the motor. Turns motor to the start position.

        :return: A PWM instance
        """
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.motor_pin, GPIO.OUT)
        p = GPIO.PWM(self.motor_pin, 50)  # GPIO motor_pin als PWM mit 50Hz
        return p

    def update(self, degrees_to_turn):
        """
        Updates the artefact by calling the according update methods for changing
        the position of the motor and in case the remaining budget - the motor has
        turned 15 times - is 0 or just 10% percent left a sound is played.

        :param degrees_to_turn: int describing how many degrees to turn
        """
        # updates motor position (artefact shrinking)
        self.update_position(degrees_to_turn)
        # warning sound if just 10% of the budget left
        if self.current_position <= 380 & self.not_warned_10_percent:
            self.make_sound()
            self.not_warned_10_percent = False
        # warning sound  if budget us used up
        if self.current_position <= 0 & self.not_warned_10_percent:
            self.make_sound()
            self.make_sound()
            self.current_position = 0
            self.not_warned_used_up = False

    def update_position(self, degrees_to_turn):
        """
        Updates the artefact motor by changing the position of the motor
        and adapts the current postion.

        :param degrees_to_turn: int describing how many degrees to turn
        """
        self.p.start(0)  # Initialisierung
        number_of_circles = math.floor(degrees_to_turn / 15)
        for n in range(number_of_circles):
            self.p.ChangeDutyCycle(
                100
            )  # TODO: test if this is full circle and counter clockwise
        self.p.ChangeDutyCycle(degrees_to_turn % 15)
        self.p.stop()
        self.current_position -= degrees_to_turn

    def reset(self):
        """
        Resets the artefact motor by changing the position of the motor
        and resets the current position to zero.
        """
        self.update_position(self.current_position)
        for n in range(15):
            self.p.ChangeDutyCycle(100)  # TODO:change value
        self.current_position = 0  # TODO total value
        self.not_warned_10_percent = True
        self.not_warned_used_up = True

    def make_sound(self):
        """
        Plays a mp3 audio file via a speaker.
        """
        p = vlc.MediaPlayer(self.audio_file)
        p.play()
