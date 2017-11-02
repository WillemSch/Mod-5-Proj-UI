import socket
import struct
from parse_data import *
from enum import Enum
import buzzer
import time
import RPi.GPIO as GPIO

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 8845
MCAST_SEND_PORT = 8846

GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
for pin in range(5, 9):
    GPIO.setup(pin, GPIO.OUT)

GPIO.setup(18, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)

accelerate_pwm = GPIO.PWM(18, 500)
decelerate_pwm = GPIO.PWM(23, 500)

accelerate_pwm.start(0)
decelerate_pwm.start(0)

send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
send_sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', MCAST_PORT))  # use MCAST_GRP instead of '' to listen only
                             # to MCAST_GRP, not all groups on MCAST_PORT
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)

sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

state = {"accel": False, "decel": False, "left": False, "right": False}

# -1: left, 0: straight, 1: right
steer_state = 0

# Index of speeds list
STOP_SPEED_STATE = 3
speed_state = STOP_SPEED_STATE
speeds = [-1.0, -0.3, -0.1, 0.0, 0.1, 0.5, 1.0]

Y_DEADZONE = 9
X_DEADZONE = 9

skiprate = 1
count = 0

prev_accel = { 'x': 0, 'y': 0, 'z': 0 }
prev_steer_state = steer_state
prev_speed_state = speed_state

panic_time = -1

while True:
    raw_data = sock.recv(10240)
    count += 1

    if panic_time != -1 and count - panic_time < 30:
        time.sleep(1/30.0)
        steer_state = 0
        speed_state = STOP_SPEED_STATE
        continue

    gyro = parse_gyro(raw_data)
    accel = parse_accel(raw_data)

    panic = True
    for v in gyro:
        panic = panic and (int(abs(gyro[v])) == 250)

    if panic:
        print("PANIC")
        steer_state = 0
        speed_state = STOP_SPEED_STATE
        panic_time = count

    if prev_accel['y'] > Y_DEADZONE and accel['y'] <= Y_DEADZONE:
        if steer_state == -1:
            steer_state = 0
        elif steer_state == 0:
            steer_state = 1
    elif prev_accel['y'] < -Y_DEADZONE and accel['y'] >= -Y_DEADZONE:
        if steer_state == 1:
            steer_state = 0
        elif steer_state == 0:
            steer_state = -1


    if prev_accel['x'] > X_DEADZONE and accel['x'] <= X_DEADZONE:
        if speed_state > 0:
            speed_state -= 1
    if prev_accel['x'] < -X_DEADZONE and accel['x'] >= -X_DEADZONE:
        if speed_state < len(speeds) - 1:
            speed_state += 1

    state['left'] = steer_state == -1
    state['right'] = steer_state == 1
    state['accel'] = speeds[speed_state] > 0
    state['decel'] = speeds[speed_state] < 0


    GPIO.output(5, state['left'])
    GPIO.output(6, state['right'])
    # GPIO.output(7, state['accel'])
    # GPIO.output(8, state['decel'])

    if state['accel']:
        accelerate_pwm.ChangeDutyCycle(100 * speeds[speed_state])
        decelerate_pwm.ChangeDutyCycle(0)
    elif state['decel']:
        decelerate_pwm.ChangeDutyCycle(100 * abs(speeds[speed_state]))
        accelerate_pwm.ChangeDutyCycle(0)
    if not state['accel'] and not state['decel']:
        accelerate_pwm.ChangeDutyCycle(0)
        decelerate_pwm.ChangeDutyCycle(0)


    # if prev_steer_state != steer_state or prev_speed_state != speed_state:
    #     buzzer.buzz(0.2)

    # print("Left: " + str(int(state['left'])) + \
    #      " Right: " + str(int(state['right']))+ \
    #      " Accel: " + str(int(state['accel'])) + \
    #      " Decel: " + str(int(state['decel'])))
    print("steer_state: " + str(steer_state) + \
          " speed_state: " + str(speeds[speed_state]))

    prev_accel = accel
    prev_steer_state = steer_state
    prev_speed_state = speed_state

    data = str(steer_state) + " " + str(speeds[speed_state])
    print("Trying to send data: steer_state = " + str(steer_state))
    send_sock.sendto(data.encode(encoding="UTF-8"), (MCAST_GRP, MCAST_SEND_PORT))
