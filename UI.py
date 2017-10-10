from tkinter import *
import _thread as thread
import time

onPI = False
if onPI:
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

prev = [False, False, False, False]

# state of program
running = True

# Setup GPIO and Pins
if onPI:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup([fwdPin, rvsPin, lftPin, rgtPin], GPIO.OUT)


def pressedUp(event):
    global prev
    if not prev[0]:
        if onPI:
            GPIO.output(fwdPin, GPIO.HIGH)
        print("UP    - Pressed")
        upBtn['relief'] = "sunken"
        upBtn['bg'] = '#93bc76'
        prev = [True, prev[1], prev[2], prev[3]]


def pressedDown(event):
    global prev
    if not prev[2]:
        if onPI:
            GPIO.output(rvsPin, GPIO.HIGH)
        print("DOWN  - Pressed")
        downBtn['relief'] = "sunken"
        downBtn['bg'] = '#93bc76'
        prev = [prev[0], True, prev[2], prev[3]]


def pressedLeft(event):
    global prev
    if not prev[2]:
        if onPI:
            GPIO.output(lftPin, GPIO.HIGH)
        print("LEFT  - Pressed")
        leftBtn['relief'] = "sunken"
        leftBtn['bg'] = '#93bc76'
        prev = [prev[0], prev[1], True, prev[3]]


def pressedRight(event):
    global prev
    if not prev[3]:
        if onPI:
            GPIO.output(rgtPin, GPIO.HIGH)
        print("RIGHT - Pressed")
        rightBtn['relief'] = "sunken"
        rightBtn['bg'] = '#93bc76'
        prev = [prev[0], prev[1], prev[2], True]


def releaseUp(event):
    global prev
    if prev[0]:
        if onPI:
            GPIO.output(fwdPin, GPIO.LOW)
        print("UP    - Released")
        upBtn['relief'] = "raised"
        upBtn['bg'] = '#BCDDA4'
        prev = [False, prev[1], prev[2], prev[3]]


def releaseDown(event):
    global prev
    if prev[1]:
        if onPI:
            GPIO.output(rvsPin, GPIO.LOW)
        print("DOWN  - Released")
        downBtn['relief'] = "raised"
        downBtn['bg'] = '#BCDDA4'
        prev = [prev[0], False, prev[2], prev[3]]


def releaseLeft(event):
    global prev
    if prev[2]:
        if onPI:
            GPIO.output(lftPin, GPIO.LOW)
        print("LEFT  - Released")
        leftBtn['relief'] = "raised"
        leftBtn['bg'] = '#BCDDA4'
        prev = [prev[0], prev[1], False, prev[3]]


def releaseRight(event):
    global prev
    if prev[3]:
        if onPI:
            GPIO.output(rgtPin, GPIO.LOW)
        print("RIGHT - Released")
        rightBtn['relief'] = "raised"
        rightBtn['bg'] = '#BCDDA4'
        prev = [prev[0], prev[1], prev[2], False]


def on_closing():
    if onPI:
        GPIO.cleanup()
        print("Cleaning GPIO")
    global running
    running = False
    master.destroy()


def loop():
    while running:
        time.sleep(0.01)  # 100 updates per second is more than enough, no need to use more computation power.

        temp = get_directions()

        if temp[0]:
            pressedUp(event=Event)
        else:
            releaseUp(event=Event)

        if temp[1]:
            pressedDown(event=Event)
        else:
            releaseDown(event=Event)

        if temp[2]:
            pressedLeft(event=Event)
        else:
            releaseLeft(event=Event)

        if temp[3]:
            pressedRight(event=Event)
        else:
            releaseRight(event=Event)


def get_directions():
    forward = False
    reverse = False
    left = False
    right = False
    return [forward, reverse, left, right]


master = Tk()
master.protocol("WM_DELETE_WINDOW", on_closing)
master.title("RC car")

f = Frame(master, width=1000, height=750)
f.pack(fill=BOTH)

downBtn = Button(f, text="Reverse", height=10, width=17, bg='#BCDDA4')
downBtn.bind("<1>", pressedDown)
downBtn.bind("<ButtonRelease-1>", releaseDown)
downBtn.grid(row=2, column=1, sticky=W + E + N + S)

leftBtn = Button(f, text="Left", height=10, width=17, bg='#BCDDA4')
leftBtn.bind("<1>", pressedLeft)
leftBtn.bind("<ButtonRelease-1>", releaseLeft)
leftBtn.grid(row=1, column=0, sticky=W + E + N + S)

rightBtn = Button(f, text="Right", height=10, width=17, bg='#BCDDA4')
rightBtn.bind("<1>", pressedRight)
rightBtn.bind("<ButtonRelease-1>", releaseRight)
rightBtn.grid(row=1, column=2, sticky=W + E + N + S)

upBtn = Button(f, text="Forward", height=10, width=17, bg='#BCDDA4')
upBtn.bind("<1>", pressedUp)
upBtn.bind("<ButtonRelease-1>", releaseUp)
upBtn.grid(row=0, column=1, sticky=W + E + N + S)

thread.start_new_thread(loop, ())
mainloop()
