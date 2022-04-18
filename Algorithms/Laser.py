import RPi.GPIO as GPIO
import time

GPIO_LASER = 17 # --> PIN11/GPIO17

def first_laser_use():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_LASER, GPIO.OUT)
    GPIO.output(GPIO_LASER, GPIO.HIGH)

# turn on the laser
def turn_laser_on_off(is_on):
    if is_on:
        GPIO.output(GPIO_LASER, 0)
    else:
        GPIO.output(GPIO_LASER, 1)
    time.sleep(0.25)


# turn off the laser
def turn_laser_off():
    # turn on the laser and configure the servos
    GPIO.output(GPIO_LASER, 0)
    time.sleep(0.25)


# turn on the laser
def turn_laser_on():
    # turn on the laser and configure the servos
    GPIO.output(GPIO_LASER, 1)
    time.sleep(0.25)


def laser_destroy():
    GPIO.cleanup()