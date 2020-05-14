'''
sensors read true when disconnected
tank sensor:
    want to read true when overfloawing
    in the correctnorientation now
sump sensor should be true when doesn't need to be filled
ato sensor should be true when needs to be filled


'''
import RPi.GPIO as gpio
import time
gpio.cleanup()
gpio.setmode(gpio.BCM)
gpio.setup(2,gpio.IN)
gpio.setup(27,gpio.IN)
gpio.setup(22,gpio.IN)

while True:
    print("ato: ",gpio.input(2)," tank: ",gpio.input(27),"  sump sensor ",gpio.input(22))
    time.sleep(1)

