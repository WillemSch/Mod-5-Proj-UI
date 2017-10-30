import socket
import struct
from parse_data import *


MCAST_GRP = '224.1.1.1'
MCAST_PORT = 8845

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', MCAST_PORT))  # use MCAST_GRP instead of '' to listen only
                             # to MCAST_GRP, not all groups on MCAST_PORT
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)

sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

state = {"accel": False, "decel": False,"left": False, "right": False}

DEADZONE = 120

skiprate = 1
count = 0

while True:
    raw_data = sock.recv(10240)
    count += 1
    if count % skiprate != 0:
        continue
    gyro = parse_gyro(raw_data)

    if gyro['x'] < -DEADZONE:
        if state['right']:
            state['right'] = False
        else:
            state['left'] = True
    if gyro['x'] > DEADZONE:
        if state['left']:
            state['left'] = False
        else:
            state['right'] = True

    if gyro['y'] < -DEADZONE:
        if state['accel']:
            state['accel'] = False
        else:
            state['decel'] = True
    if gyro['y'] > DEADZONE:
        if state['decel']:
            state['decel'] = False
        else:
            state['accel'] = True

    print("Left: " + str(int(state['left'])) + \
         " Right: " + str(int(state['right']))+ \
         " Accel: " + str(int(state['accel'])) + \
         " Decel: " + str(int(state['decel'])))
