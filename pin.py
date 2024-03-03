import RPi.GPIO as GPIO
import time


gpio_pins = [4, 17, 22, 27]

GPIO.setmode(GPIO.BCM)
for pin_num in gpio_pins:
    GPIO.setup(pin_num, GPIO.OUT)
    GPIO.output(pin_num, GPIO.LOW)


def pin_on(pin_num):
    GPIO.output(pin_num, GPIO.HIGH)


def pin_off(pin_num):
    GPIO.output(pin_num, GPIO.LOW)


def pin_cycle(pin_num, duration=0.001):
    GPIO.output(pin_num, GPIO.HIGH)
    time.sleep(duration)
    GPIO.output(pin_num, GPIO.LOW)


def cleanup():
    for pin_num in gpio_pins:
        GPIO.setup(pin_num, GPIO.OUT)
        GPIO.output(pin_num, GPIO.LOW)
    GPIO.cleanup()

