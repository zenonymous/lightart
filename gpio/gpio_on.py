#!/usr/bin/python3

import RPi.GPIO as GPIO
import time

relais = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(relais, GPIO.OUT)
GPIO.output(relais, GPIO.HIGH)
