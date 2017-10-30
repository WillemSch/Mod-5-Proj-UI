import RPi.GPIO as GPIO
import time

def buzz(seconds, pitch=750):
    GPIO.cleanup()
    buzzer_pin = 21  # Change this maybe
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(buzzer_pin, GPIO.OUT)

    period = 1.0/pitch
    delay = period/2.0
    cycles = int(seconds * pitch)

    for _ in range(0, cycles):
        GPIO.output(buzzer_pin, True)
        time.sleep(delay)
        GPIO.output(buzzer_pin, False)
        time.sleep(delay)

    GPIO.cleanup()
