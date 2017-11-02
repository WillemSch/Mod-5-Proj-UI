import socket
import struct
import parse_data
import sys
import pygame
import colorsys

pygame.init()
myfont = pygame.font.SysFont("monospace", 15)

size = width, height = 1280, 720
black = 0, 0, 0
white = 255, 255, 255

#set constants for graph amplitude
gyroamp = -0.39215
accelamp = -5
#set constants for graph colours
gyrocolour = 0.0013071
accelcolour = 0.016667

screen = pygame.display.set_mode(size)
bg = pygame.image.load("background.jpg")


MCAST_GRP = '224.1.1.1'
MCAST_PORT = 8845

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', MCAST_PORT))	 # use MCAST_GRP instead of '' to listen only
							 # to MCAST_GRP, not all groups on MCAST_PORT
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)

sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

def reformat (color):
	return int (round (color[0] * 255)), int (round (color[1] * 255)), int (round (color[2] * 255))

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

	#Draw dynamic gyroscope graphs and their outlines
	gyrographx = pygame.draw.rect(screen, rgbxg, (80, 300, 100, (gyro['x']*gyroamp)))
	gyroxoutline = pygame.draw.rect(screen, black, (80, 300, 100, (gyro['x']*gyroamp)), 2)
	gyrography = pygame.draw.rect(screen, rgbyg, (200, 300, 100, (gyro['y']*gyroamp)))
	gyroyoutline = pygame.draw.rect(screen, black, (200, 300, 100, (gyro['y']*gyroamp)), 2)
	gyrographz = pygame.draw.rect(screen, rgbzg, (320, 300, 100, (gyro['z']*gyroamp)))
	gyrozoutline = pygame.draw.rect(screen, black, (320, 300, 100, (gyro['z']*gyroamp)), 2)
	
	#Draw dynamic accelerometer graphs and their outlines
	accelgraphx = pygame.draw.rect(screen, rgbxa, (860, 300, 100, (accel['x']*accelamp)))
	accelxoutline = pygame.draw.rect(screen, black, (860, 300, 100, (accel['x']*accelamp)), 2)
	accelgraphy = pygame.draw.rect(screen, rgbya, (980, 300, 100, (accel['y']*accelamp)))
	accelyoutline = pygame.draw.rect(screen, black, (980, 300, 100, (accel['y']*accelamp)), 2)
	accelgraphz = pygame.draw.rect(screen, rgbza, (1100, 300, 100, (accel['z']*accelamp)))
	accelzoutline = pygame.draw.rect(screen, black, (1100, 300, 100, (accel['z']*accelamp)), 2)
	
	#set up and blit dynamic data label for gyro
	xgyrodata = myfont.render(str(gyro['x']), 1, (255,255,0))
	ygyrodata = myfont.render(str(gyro['y']), 1, (255,255,0))
	zgyrodata = myfont.render(str(gyro['z']), 1, (255,255,0))
	screen.blit(xgyrodata, (95, 100))
	screen.blit(ygyrodata, (215, 100))
	screen.blit(zgyrodata, (335, 100))
	
	#set up and blit dynamic data label for accel
	xacceldata = myfont.render(str(accel['x']), 1, (255,255,0))
	yacceldata = myfont.render(str(accel['y']), 1, (255,255,0))
	zacceldata = myfont.render(str(accel['z']), 1, (255,255,0))
	screen.blit(xacceldata, (880, 100))
	screen.blit(yacceldata, (1000, 100))
	screen.blit(zacceldata, (1120, 100))
	
	#set up value labels
	zerolabel = myfont.render("0", 1, (255,255,0))
	maxlabel = myfont.render("255", 1, (255,255,0))
	minlabel = myfont.render("-255", 1, (255,255,0))
	#blit for gyro graphs
	screen.blit(zerolabel, (65,290))
	screen.blit(maxlabel, (45,190))
	screen.blit(minlabel, (35,390))
	#blit for accel graphs
	screen.blit(zerolabel, (845,290))
	screen.blit(maxlabel, (825,190))
	screen.blit(minlabel, (815,390))
	
	#Set up and blit graph legends and title
	gyrotitle = myfont.render("Gyroscope data in deg/s", 5, (255,255,0))
	acceltitle = myfont.render("Accelerometer data in m/s", 5, (255,255,0))
	graphlegend = myfont.render("x-axis        y-axis       z-axis", 5, (255,255,0))
	screen.blit(gyrotitle, (150, 60))
	screen.blit(graphlegend, (103, 80))
	screen.blit(acceltitle, (920, 60))
	screen.blit(graphlegend, (885, 80))	

	pygame.display.flip()
