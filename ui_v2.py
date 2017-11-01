import pygame
import sys
import time
import math
import socket
import struct
import parse_data

pygame.init()

size = width, height = 600, 600
windows98 = 107, 127, 152

screen = pygame.display.set_mode(size, pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
pygame.display.set_caption('\"UI\"')
screen.fill(windows98)
pygame.display.flip()

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((250, 250, 250))

wheel = pygame.image.load("./imgs/wheel.png")
bg = pygame.image.load("./imgs/bg.jpg")


MCAST_GRP = '224.1.1.1'
MCAST_PORT = 8846

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', MCAST_PORT))	 # use MCAST_GRP instead of '' to listen only to MCAST_GRP, not all groups on MCAST_PORT
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)


def minimum(x):
    if x[0] <= x[1]:
        return x[0], x[0]
    else:
        return x[1], x[1]


def calc_pos(x, state):
    if not state == 0:
        offset = .5 * math.sqrt(math.pow(x[1], 2) + math.pow(x[1], 2)) - .5 * x[1]
    if x[0] <= x[1]:
        difference = x[1]-x[0]
        if not state == 0:
            return 0 - offset, .5 * difference - offset
        return 0, .5 * difference
    else:
        difference = x[0]-x[1]
        return .5 * difference, 0


scale = size


def get_steering(state):
    data = sock.recv(10240)
    data = data.decode(encoding='UTF-8')

    return parse_data.parse_steering_state(data)


steering_state = 0
setup = True

while True:
    if setup:
        scale = size
        pygame.display.flip()

        wheel_scale = minimum(scale)
        temp_wheel = pygame.transform.scale(wheel, wheel_scale)
        setup = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.VIDEORESIZE:
            scale = event.dict['size']
            pygame.display.flip()

            wheel_scale = minimum(scale)
            temp_wheel = pygame.transform.scale(wheel, wheel_scale)

    steering_state = get_steering(steering_state)

    screen.blit(pygame.transform.scale(background, scale), (0, 0))
    screen.blit(pygame.transform.scale(bg, scale), (0, 0))
    background.fill(windows98)

    temp_wheel = pygame.transform.scale(wheel, wheel_scale)

    if steering_state == 1:
        screen.blit(pygame.transform.rotate(temp_wheel, 45), calc_pos(wheel_scale, steering_state))
        print("state = 1")
    elif steering_state == 2:
        screen.blit(pygame.transform.rotate(temp_wheel, -45), calc_pos(wheel_scale, steering_state))
        print("state = 2")
    else:
        screen.blit(pygame.transform.rotate(temp_wheel, 0), calc_pos(wheel_scale, steering_state))

    pygame.display.flip()
    time.sleep(0.03)
