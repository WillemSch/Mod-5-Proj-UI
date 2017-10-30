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

DEADZONE = 180

skiprate = 5
count = 0

while True:
    raw_data = sock.recv(10240)
    count += 1
    if count % skiprate != 0:
        continue
    gyro = parse_gyro(raw_data)

    if gyro['y'] > DEADZONE:
        state['accel'] = True
    if gyro['y'] < -DEADZONE:
        state['accel'] = False

    if gyro['x'] > DEADZONE:
        if state['right']:
            state['right'] = False
        else:
            state['left'] = True
    if gyro['x'] < -DEADZONE:
        if state['left']:
            state['left'] = False
        else:
            state['right'] = True

    print(str(int(state['left'])) + " " + str(int(state['right'])))
