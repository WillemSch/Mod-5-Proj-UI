import pygame
import sys
import time
import math
import socket
import struct
import parse_data
import _thread

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

sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)


def minimum(x):
    if x[0] <= x[1]:
        return x[0], x[0]
    else:
        return x[1], x[1]


def animate_rotation(prev_angle, target_rotation, delta_time):
    anim_speed = 200
    if prev_angle == target_rotation:
        return prev_angle

    if target_rotation < 180:
        new_angle = prev_angle + anim_speed * delta_time
        if new_angle > target_rotation and prev_angle < 180:
            new_angle = target_rotation
        elif new_angle > 360:
            new_angle -= 360
        elif new_angle < 0:
            new_angle += 360
    else:
        new_angle = prev_angle - anim_speed * delta_time
        if new_angle < target_rotation and prev_angle > 300:
            new_angle = target_rotation
        elif new_angle > 360:
            new_angle -= 360
        elif new_angle < 0:
            new_angle += 360
    return new_angle


def get_nearest_45(angle):
    if 0 <= angle < 90:
        return 45
    elif 90 <= angle < 180:
        return 135
    elif 180 <= angle < 270:
        return 225
    else:
        return 315


def calc_pos(x, angle, radius):
    nearest_45 = get_nearest_45(angle)
    print(nearest_45)
    offset = math.cos(math.radians(math.fabs(nearest_45 - angle))) * (math.sqrt(2) * .5 * radius) - .5 * radius
    print("angle: " + str(angle) + " - offset:" + str(offset))
    if x[0] <= x[1]:
        difference = x[1]-x[0]
        return 0 - offset, .5 * difference - offset
    else:
        difference = x[0]-x[1]
        return .5 * difference - offset, 0


scale = size


def get_steering(state):
    print("waiting for data")
    data = sock.recv(10240)
    data = data.decode(encoding='UTF-8')
    print("Data decoded")
    return parse_data.parse_steering_state(data)


steering_state = 0
setup = True
prev_time = time.localtime()
current_angle = 0
lastFrameTime = time.time()


def listener():
    while True:
        global steering_state
        steering_state = get_steering(steering_state)
        time.sleep(0.01)


_thread.start_new_thread(listener, ())

while True:

    if setup:
        scale = size
        pygame.display.flip()

        wheel_scale = minimum(scale)
        temp_wheel = pygame.transform.scale(wheel, wheel_scale)
        setup = False

    currentTime = time.time()
    dt = currentTime - lastFrameTime
    lastFrameTime = currentTime

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.VIDEORESIZE:
            scale = event.dict['size']
            pygame.display.flip()

            wheel_scale = minimum(scale)
            temp_wheel = pygame.transform.scale(wheel, wheel_scale)

    screen.blit(pygame.transform.scale(background, scale), (0, 0))
    screen.blit(pygame.transform.scale(bg, scale), (0, 0))
    background.fill(windows98)

    temp_wheel = pygame.transform.scale(wheel, wheel_scale)

    if steering_state == 1:
        new_angle = animate_rotation(current_angle, 45, dt)
    elif steering_state == -1:
        new_angle = animate_rotation(current_angle, 315, dt)
    else:
        new_angle = animate_rotation(current_angle, 0, dt)

    print(calc_pos(wheel_scale, new_angle, wheel_scale[0]))
    temp_wheel = pygame.transform.rotate(temp_wheel, new_angle)
    screen.blit(temp_wheel, calc_pos(wheel_scale, new_angle, wheel_scale[0]))
    current_angle = new_angle

    pygame.display.flip()
    time.sleep(0.01)
