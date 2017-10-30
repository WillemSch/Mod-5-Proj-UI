import socket
import struct
import parse_data

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 8845

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', MCAST_PORT))  # use MCAST_GRP instead of '' to listen only
                             # to MCAST_GRP, not all groups on MCAST_PORT
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)

sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

while True:
  data = sock.recv(10240)

  gyro = parse_data.parse_gyro(data)

  print("{:10.4f}".format(gyro['x']) + \
        "{:10.4f}".format(gyro['y']) + \
        "{:10.4f}".format(gyro['z']))
