#!/usr/bin/python3

import RPi.GPIO as GPIO
import time

relais = 23

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(relais, GPIO.OUT)

GPIO.cleanup()
