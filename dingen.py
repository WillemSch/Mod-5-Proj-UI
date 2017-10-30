import socket
import struct
import parse_data
import sys
import pygame

pygame.init()
myfont = pygame.font.SysFont("monospace", 15)

size = width, height = 1280, 720
black = 0, 0, 0
white = 255, 255, 255
red = 255, 100, 100

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
	
	"""
	Drawing
	"""
	screen.fill(black)
	rect1 = pygame.draw.rect(screen, red, (50, 150, 100, 50))
	if int(gyro['x']) > 0:
		rect1.inflate_ip(100, 50)
	else:
		rect1.inflate_ip(0,0)
	label1 = myfont.render(str(gyro['x']), 1, (255,255,0))
	label2 = myfont.render(str(gyro['y']), 1, (255,255,0))
	label3 = myfont.render(str(gyro['z']), 1, (255,255,0))
	screen.blit(label1, (100, 100))
	screen.blit(label2, (200, 100))
	screen.blit(label3, (300, 100))
	pygame.display.flip()

	print("{:10.4f}".format(gyro['x']) + \
		"{:10.4f}".format(gyro['y']) + \
		"{:10.4f}".format(gyro['z']))