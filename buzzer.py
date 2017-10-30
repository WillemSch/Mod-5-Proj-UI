import RPi.GPIO as GPIO
import time

buzzer_pin = 6  # Change this maybe
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer_pin, GPIO.OUT)


def buzz(seconds, pitch=750):
    period = 1.0/pitch
    delay = period/2.0
    cycles = int(seconds * pitch)

    for _ in cycles:
        GPIO.output(buzzer_pin, True)
        time.sleep(delay)
        GPIO.output(buzzer_pin, True)
        time.sleep(delay)
