import numpy as np
import serial
import RPi.GPIO as GPIO


class Communicator:
    def __init__(self, nav_required = False, arm_required = False):
        self.gpioOutputPin = 12
        self.gpioInputPin = 16
        self.nav_required = nav_required
        self.arm_required = arm_required

    def initComs(self):
        if self.nav_required:
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(self.gpioOutputPin, GPIO.OUT, initial=GPIO.LOW)
            GPIO.setup(self.gpioInputPin, GPIO.IN)
            self._sendStopToNav()
            self.NAV_IS_STOPPED = False
            self.NAV_SHOULD_MOVE = False
        if self.arm_required:
            self.ARM_IS_READY = False
            self.arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=19200, writeTimeout=0, timeout=0)


    def _readSignalFromArm(self):
        byte_input = self.arduino.readline()
        string_input = byte_input.decode()
        string_input = string_input.replace('\r', '')
        string_input = string_input.replace('\n', '')
        if string_input == 'A':
            self.ARM_IS_READY = True


    def _sendCoordsToArm(self, cords):

        if cords is not None:
            value = 'B' + str(int(cords[0])) + ' ' + str(int(cords[1])) + ' ' + str(int(cords[2])) + '\r'
            self.arduino.write(bytes(value, 'utf-8'))
            self.ARM_IS_READY = False

    def _sendStopToNav(self):
        GPIO.output(self.gpioOutputPin, GPIO.HIGH)
        self.NAV_SHOULD_MOVE = False

    def _sendGoToNav(self):
        GPIO.output(self.gpioOutputPin, GPIO.LOW)
        self.NAV_SHOULD_MOVE = True

    def _readNavSignal(self):
        value = GPIO.input(self.gpioInputPin)
        if value == 1:
            self.NAV_IS_STOPPED = True
        elif value == 0:
            self.NAV_IS_STOPPED = False

