import numpy as np
import serial
import RPi.GPIO as GPIO


class Communicator:
    def __init__(self):
        self.gpioOutputPin = 12
        self.gpioInputPin = 16

    def initComs(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.gpioOutputPin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.gpioInputPin, GPIO.IN)
        self.ARM_IS_READY = False
        self.NAV_IS_STOPPED = False
        self.arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=19200, writeTimeout=0, timeout=0)

    def updateArmOnly(self, spear):
        armInput = self._readSignalFromArm()

        if armInput == 'A':
            self.ARM_IS_READY = True

        if np.any(spear):
            self._sendCoordsToArm(spear)


    def updateNavOnly(self, spear):
        armInput = self._readSignalFromArm()
        self.NAV_IS_STOPPED = self._readNavSignal()
        if armInput == 'A':
            self.ARM_IS_READY = True
        if np.any(spear):
            self._sendStopToNav()
            if self.NAV_IS_STOPPED:
                self._sendCoordsToArm(spear)
        else:
            self._sendGoToNav()

    def _readSignalFromArm(self):
        byte_input = self.arduino.readline()
        string_input = byte_input.decode()
        string_input = string_input.replace('\r', '')
        string_input = string_input.replace('\n', '')
        return string_input

    def _sendCoordsToArm(self, cords):

        if cords is not None:

            value = 'B' + str(int(cords[0])) + ' ' + str(int(cords[1])) + ' ' + str(int(cords[2])) + '\r'
            self.arduino.write(bytes(value, 'utf-8'))
            self.ARM_IS_READY = False

    def _sendStopToNav(self):
        GPIO.output(self.gpioOutputPin, GPIO.HIGH)
        self.NAV_IN_MOVE = False

    def _sendGoToNav(self):
        GPIO.output(self.gpioOutputPin, GPIO.LOW)

    def _readNavSignal(self):
        value = GPIO.input(self.gpioInputPin)
        return value
