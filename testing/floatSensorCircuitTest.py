
import RPi.GPIO as gpio
import time
gpio.cleanup()
gpio.setmode(gpio.BCM)
gpio.setup(2,gpio.IN)
gpio.setup(3,gpio.IN)
gpio.setup(4,gpio.IN)

while True:
    print(gpio.input(2),"  ",gpio.input(3),"   ",gpio.input(4))
    time.sleep(1)

