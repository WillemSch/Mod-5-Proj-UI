from Tkinter import *
import RPi.GPIO as GPIO

# Declare pins
fwdPin = 22
rvsPin = 23
lftPin = 24
rgtPin = 25

# directions
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

# Setup GPIO and Pins
GPIO.setmode(GPIO.BCM)
GPIO.setup([fwdPin, rvsPin, lftPin, rgtPin], GPIO.OUT)


def pressedUp(event):
    GPIO.output(fwdPin, GPIO.HIGH)
    print("UP")


def pressedDown(event):
    GPIO.output(rvsPin, GPIO.HIGH)
    print("DOWN")


def pressedLeft(event):
    GPIO.output(lftPin, GPIO.HIGH)
    print("LEFT")


def pressedRight(event):
    GPIO.output(rgtPin, GPIO.HIGH)
    print("RIGHT")


def releaseUp(event):
    GPIO.output(fwdPin, GPIO.LOW)
    print("UP - Released")


def releaseDown(event):
    GPIO.output(rvsPin, GPIO.LOW)
    print("DOWN - Released")


def releaseLeft(event):
    GPIO.output(lftPin, GPIO.LOW)
    print("LEFT - Released")


def releaseRight(event):
    GPIO.output(rgtPin, GPIO.LOW)
    print("RIGHT - Released")


master = Tk()

f = Frame(master, width=1000, height=750)
f.pack()

downBtn = Button(f, text="down")
downBtn.bind("<1>", pressedDown)
downBtn.bind("<ButtonRelease-1>", releaseDown)
downBtn.pack()

leftBtn = Button(f, text="left")
leftBtn.bind("<1>", pressedLeft)
leftBtn.bind("<ButtonRelease-1>", releaseLeft)
leftBtn.pack()

rightBtn = Button(f, text="right")
rightBtn.bind("<1>", pressedRight)
rightBtn.bind("<ButtonRelease-1>", releaseRight)
rightBtn.pack()

upBtn = Button(f, text="up")
upBtn.bind("<1>", pressedUp)
upBtn.bind("<ButtonRelease-1>", releaseUp)
upBtn.pack()