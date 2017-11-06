import socket
import time
import random


MCAST_GRP = '224.1.1.1'
MCAST_PORT = 8845
MCAST_SEND_PORT = 8846

send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
send_sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

steer_state = 0
speed_state = 0
speeds = [-1, -0.3, -0.1, 0, 0.1, 0.3, 1]

first = True

while True:
    steer_state = random.randint(-1, 1)
    speed_state = speeds[random.randint(0, 6)]

    data = str(steer_state) + " " + str(speeds[speed_state])
    send_sock.sendto(data.encode(encoding="UTF-8"), (MCAST_GRP, MCAST_SEND_PORT))
    time.sleep(1)
