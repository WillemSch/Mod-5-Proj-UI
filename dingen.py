import socket
import struct
import parse_data
import sys
import pygame
import colorsys
import _thread
import time

pygame.init()
myfont = pygame.font.SysFont("monospace", 15)

size = width, height = 960, 540
black = 0, 0, 0
white = 255, 255, 255
iets = 150, 0, 150

#set constants for graph amplitude
gyroamp = -0.29411
accelamp = -3.75
#set constants for graph colours
gyrocolour = 0.0013070
accelcolour = 0.016667

screen = pygame.display.set_mode(size)
bg = pygame.image.load("background.jpg")


MCAST_GRP = '224.1.1.1'
MCAST_PORT = 8845
MCAST_PORT_STATE = 8846

steering_state = 0
speed_state = 0

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', MCAST_PORT))	 # use MCAST_GRP instead of '' to listen only
							 # to MCAST_GRP, not all groups on MCAST_PORT
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)

state_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
state_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
state_sock.bind(('', MCAST_PORT_STATE))

sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
state_sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

def reformat (color):
	return int (round (color[0] * 255)), int (round (color[1] * 255)), int (round (color[2] * 255))


def get_steering():
    data = state_sock.recv(10240)
    data = data.decode(encoding='UTF-8')
    return parse_data.parse_steering_state(data)


def get_speed():
    data = state_sock.recv(10240)
    data = data.decode(encoding='UTF-8')
    return parse_data.parse_speed_state(data)


def listener():
    while True:
        global steering_state
        global speed_state
        speed_state = get_speed()
        steering_state = get_steering()
        time.sleep(0.01)


_thread.start_new_thread(listener, ())

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()
	data = sock.recv(10240)
	data = data.decode(encoding='UTF-8')

	gyro = parse_data.parse_gyro(data)
	accel = parse_data.parse_accel(data)

	#set up colours for gyro	
	rgbxg = reformat (colorsys.hls_to_rgb(abs(gyro['x']*gyrocolour), 0.5, 1))
	rgbyg = reformat (colorsys.hls_to_rgb(abs(gyro['y']*gyrocolour), 0.5, 1))
	rgbzg = reformat (colorsys.hls_to_rgb(abs(gyro['z']*gyrocolour), 0.5, 1))
	#set up colours for accel
	rgbxa = reformat (colorsys.hls_to_rgb(abs(accel['x']*accelcolour), 0.5, 1))
	rgbya = reformat (colorsys.hls_to_rgb(abs(accel['y']*accelcolour), 0.5, 1))
	rgbza = reformat (colorsys.hls_to_rgb(abs(accel['z']*accelcolour), 0.5, 1))

	"""
	Drawing
	"""
	screen.blit(bg, (0, 0))
	
	#Draw state buttons and their outlines
	stateleft = pygame.draw.rect(screen, white, (330, 400, 100, 100))
	stateright = pygame.draw.rect(screen, white, (530, 400, 100, 100))
	statefwd = pygame.draw.rect(screen, white, (430, 300, 100, 100))
	statebkwd = pygame.draw.rect(screen, white, (430, 400, 100, 100))
	
	#Visualise state using buttons
	if steering_state == -1:
		stateleft = pygame.draw.rect(screen, iets, (330, 400, 100, 100))
	elif steering_state == 1:
		stateright = pygame.draw.rect(screen, iets, (530, 400, 100, 100))	

	if speed_state > 0:
		statefwd = pygame.draw.rect(screen, iets, (430, 300, 100, 100))
	elif speed_state < 0:
		statebkwd = pygame.draw.rect(screen, iets, (430, 400, 100, 100))
	 
	stateleftoutline = pygame.draw.rect(screen, black, (330, 400, 100, 100), 2)
	staterightoutline = pygame.draw.rect(screen, black, (530, 400, 100, 100), 2)
	statefwdoutline = pygame.draw.rect(screen, black, (430, 300, 100, 100), 2)	
	statebkwdoutline = pygame.draw.rect(screen, black, (430, 400, 100, 100), 2)

		
	#Draw dynamic gyroscope graphs and their outlines
	gyrographx = pygame.draw.rect(screen, rgbxg, (60, 225, 75, (gyro['x']*gyroamp)))
	gyroxoutline = pygame.draw.rect(screen, black, (60, 225, 75, (gyro['x']*gyroamp)), 2)
	gyrography = pygame.draw.rect(screen, rgbyg, (150, 225, 75, (gyro['y']*gyroamp)))
	gyroyoutline = pygame.draw.rect(screen, black, (150, 225, 75, (gyro['y']*gyroamp)), 2)
	gyrographz = pygame.draw.rect(screen, rgbzg, (240, 225, 75, (gyro['z']*gyroamp)))
	gyrozoutline = pygame.draw.rect(screen, black, (240, 225, 75, (gyro['z']*gyroamp)), 2)
	
	#Draw dynamic accelerometer graphs and their outlines
	accelgraphx = pygame.draw.rect(screen, rgbxa, (645, 225, 75, (accel['x']*accelamp)))
	accelxoutline = pygame.draw.rect(screen, black, (645, 225, 75, (accel['x']*accelamp)), 2)
	accelgraphy = pygame.draw.rect(screen, rgbya, (735, 225, 75, (accel['y']*accelamp)))
	accelyoutline = pygame.draw.rect(screen, black, (735, 225, 75, (accel['y']*accelamp)), 2)
	accelgraphz = pygame.draw.rect(screen, rgbza, (825, 225, 75, (accel['z']*accelamp)))
	accelzoutline = pygame.draw.rect(screen, black, (825, 225, 75, (accel['z']*accelamp)), 2)
	
	#set up and blit dynamic data label for gyro
	xgyrodata = myfont.render(str(gyro['x']), 1, (255,255,0))
	ygyrodata = myfont.render(str(gyro['y']), 1, (255,255,0))
	zgyrodata = myfont.render(str(gyro['z']), 1, (255,255,0))
	screen.blit(xgyrodata, (71, 75))
	screen.blit(ygyrodata, (161, 75))
	screen.blit(zgyrodata, (251, 75))
	
	#set up and blit dynamic data label for accel
	xacceldata = myfont.render(str(accel['x']), 1, (255,255,0))
	yacceldata = myfont.render(str(accel['y']), 1, (255,255,0))
	zacceldata = myfont.render(str(accel['z']), 1, (255,255,0))
	screen.blit(xacceldata, (660, 75))
	screen.blit(yacceldata, (750, 75))
	screen.blit(zacceldata, (840, 75))
	
	#set up value labels
	zerolabel = myfont.render("0", 1, (255,255,0))
	maxlabel = myfont.render("255", 1, (255,255,0))
	minlabel = myfont.render("-255", 1, (255,255,0))
	#blit for gyro graphs
	screen.blit(zerolabel, (49,217))
	screen.blit(maxlabel, (34,142))
	screen.blit(minlabel, (26,292))
	#blit for accel graphs
	screen.blit(zerolabel, (634,217))
	screen.blit(maxlabel, (619,142))
	screen.blit(minlabel, (611,292))
	
	#Set up and blit graph legends and title
	gyrotitle = myfont.render("Gyroscope data in deg/s", 5, (255,255,0))
	acceltitle = myfont.render("Accelerometer data in m/s", 5, (255,255,0))
	graphlegend = myfont.render("x-axis	   y-axis	 z-axis", 5, (255,255,0))
	screen.blit(gyrotitle, (90, 45))
	screen.blit(graphlegend, (77, 60))
	screen.blit(acceltitle, (669, 45))
	screen.blit(graphlegend, (664, 60))	

	pygame.display.flip()
