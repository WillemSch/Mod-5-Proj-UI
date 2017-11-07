import pygame
import sys
import time
import math
import socket
import struct
import parse_data
import _thread

pygame.init()

size = width, height = 1200, 600
windows98 = 107, 127, 152

screen = pygame.display.set_mode(size, pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
pygame.display.set_caption('(ง ͡ʘ ͜ʖ ͡ʘ)ง')
screen.fill(windows98)
pygame.display.flip()

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((250, 250, 250))

wheel = pygame.image.load("./imgs/wheel.png")
meter = pygame.image.load("./imgs/meter.png")
meter_bg = pygame.image.load("./imgs/meterbg.png")
bg = pygame.image.load("./imgs/bg.jpg")

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 8846

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', MCAST_PORT))  # use MCAST_GRP instead of '' to listen only to MCAST_GRP, not all groups on MCAST_PORT
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)

sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)


def minimum(tuple):
    if tuple[0] <= tuple[1]:
        return tuple[0], tuple[0]
    else:
        return tuple[1], tuple[1]


def animate_rotation(prev_angle, target_rotation, delta_time):
    anim_speed = 200
    if prev_angle == target_rotation:
        return prev_angle

    if target_rotation < 180:
        new_angle = prev_angle + anim_speed * delta_time
        if new_angle > target_rotation and prev_angle < 180:
            new_angle = target_rotation
    else:
        new_angle = prev_angle - anim_speed * delta_time
        if new_angle < target_rotation and prev_angle > 300:
            new_angle = target_rotation
    return new_angle % 360


def get_nearest_45(angle):
    if 0 <= angle < 90:
        return 45
    elif 90 <= angle < 180:
        return 135
    elif 180 <= angle < 270:
        return 225
    else:
        return 315


def calc_pos(scale_tuple, angle, radius, square_id=0):
    nearest_45 = get_nearest_45(angle)
    offset = math.cos(math.radians(math.fabs(nearest_45 - angle))) * (math.sqrt(2) * .5 * radius) - .5 * radius
    if scale_tuple[0] <= scale_tuple[1]:
        difference = scale_tuple[1] - scale_tuple[0]
        if vertical:
            return 0 - offset, .5 * difference - offset + scale_tuple[1] * .5 * square_id
        else:
            return 0 - offset + scale_tuple[0] * square_id, .5 * difference - offset
    else:
        difference = scale_tuple[0] - scale_tuple[1]
        if vertical:
            return .5 * difference - offset, 0 - offset + scale_tuple[1] * square_id
        else:
            return .5 * difference - offset + scale_tuple[0] * square_id, 0 - offset


scale = size


def get_steering():
    data = sock.recv(10240)
    data = data.decode(encoding='UTF-8')
    return parse_data.parse_steering_state(data)


def get_speed():
    data = sock.recv(10240)
    data = data.decode(encoding='UTF-8')
    return parse_data.parse_speed_state(data)


steering_state = 0
speed_state = 0
setup = True
vertical = size[0] < size[1]
prev_time = time.localtime()
current_steer_angle = 0
current_speed_angle = 0
lastFrameTime = time.time()


def listener():
    while True:
        global steering_state
        global speed_state
        speed_state = get_speed()
        steering_state = get_steering()
        time.sleep(0.01)


_thread.start_new_thread(listener, ())

while True:

    if setup:
        scale = size
        pygame.display.flip()

        wheel_scale = minimum(scale)
        temp_wheel = pygame.transform.scale(wheel, wheel_scale)
        setup = False

        if vertical:
            halve = scale[0], scale[1] / 2
        else:
            halve = scale[0] / 2, scale[1]

    currentTime = time.time()
    dt = currentTime - lastFrameTime
    lastFrameTime = currentTime

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode(event.dict['size'], pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
            scale = event.dict['size']
            vertical = scale[0] < scale[1]
            pygame.display.flip()

            if vertical:
                halve = scale[0], int(scale[1] / 2)
            else:
                halve = int(scale[0] / 2), scale[1]

            wheel_scale = minimum(halve)
            temp_wheel = pygame.transform.scale(wheel, wheel_scale)
            temp_speed = pygame.transform.scale(meter, wheel_scale)

    screen.blit(pygame.transform.scale(background, scale), (0, 0))
    screen.blit(pygame.transform.scale(bg, scale), (0, 0))
    temp_meter_bg = pygame.transform.scale(meter_bg, wheel_scale)
    background.fill(windows98)

    temp_wheel = pygame.transform.scale(wheel, wheel_scale)
    temp_speed = pygame.transform.scale(meter, wheel_scale)

    # calculate steering angle
    if steering_state == 1:
        new_angle_wheel = animate_rotation(current_steer_angle, 45, dt)
    elif steering_state == -1:
        new_angle_wheel = animate_rotation(current_steer_angle, 315, dt)
    else:
        new_angle_wheel = animate_rotation(current_steer_angle, 0, dt)

    # calculate speed angle
    if speed_state >= 0:
        speed_angle = animate_rotation(current_speed_angle, 45 * speed_state, dt)
    else:
        speed_angle = animate_rotation(current_speed_angle, 360 + 45 * speed_state, dt)

    temp_speed = pygame.transform.rotate(temp_speed, speed_angle)
    temp_wheel = pygame.transform.rotate(temp_wheel, new_angle_wheel)
    screen.blit(temp_wheel, calc_pos(halve, new_angle_wheel, wheel_scale[0], square_id=0))
    screen.blit(temp_speed, calc_pos(halve, speed_angle, wheel_scale[0], square_id=1))
    screen.blit(temp_meter_bg, calc_pos(halve, 0, wheel_scale[0], square_id=1))
    current_steer_angle = new_angle_wheel
    current_speed_angle = speed_angle

    pygame.display.flip()
    time.sleep(0.01)
