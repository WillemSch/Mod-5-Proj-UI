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
red = 255, 100, 100
blue = 100, 255, 100
yellow = 100, 100, 255

ISGYRO = False

if ISGYRO == False:
	c1 = -100
	c2 = 0.32
else:
	c1 = -5
	c2 = 0.016667

screen = pygame.display.set_mode(size)

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 8845

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', MCAST_PORT))	 # use MCAST_GRP instead of '' to listen only
							 # to MCAST_GRP, not all groups on MCAST_PORT
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)

sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()
	data = sock.recv(10240)
	data = data.decode(encoding='UTF-8')
	gyro = parse_data.parse_gyro(data)
	
	def reformat (color):
		return int (round (color[0] * 255)), int (round (color[1] * 255)), int (round (color[2] * 255))
	rgb1 = reformat (colorsys.hls_to_rgb(abs(gyro['x']*c2), 0.5, 1))
	rgb2 = reformat (colorsys.hls_to_rgb(abs(gyro['y']*c2), 0.5, 1))
	rgb3 = reformat (colorsys.hls_to_rgb(abs(gyro['z']*c2), 0.5, 1))

	
	"""
	Drawing
	"""
	screen.fill(black)
	rectx = pygame.draw.rect(screen, rgb1, (80, 300, 100, (gyro['x']*c1)))
	recty = pygame.draw.rect(screen, rgb2, (200, 300, 100, (gyro['y']*c1)))
	rectz = pygame.draw.rect(screen, rgb3, (320, 300, 100, (gyro['z']*c1)))
	label1 = myfont.render(str(gyro['x']), 1, (255,255,0))
	label2 = myfont.render(str(gyro['y']), 1, (255,255,0))
	label3 = myfont.render(str(gyro['z']), 1, (255,255,0))
	label4 = myfont.render("0", 1, (255,255,0))
	screen.blit(label1, (100, 100))
	screen.blit(label2, (220, 100))
	screen.blit(label3, (340, 100))
	screen.blit(label4, (65,290))
	pygame.display.flip()

	print("{:10.4f}".format(gyro['x']) + \
		"{:10.4f}".format(gyro['y']) + \
		"{:10.4f}".format(gyro['z']))
