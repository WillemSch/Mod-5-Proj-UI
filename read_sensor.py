# from mpu6050 import mpu6050
import socket
import time

# sensor = mpu6050(0x68)

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 8845

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

while True:
    x = 10
    y = 15
    z = 20
    gyro_data_dict = {'x': x, 'y': y, 'z': z} #sensor.get_gyro_data()
    gyro_data = str(gyro_data_dict['x']) + " " + \
                str(gyro_data_dict['y']) + " " + \
                str(gyro_data_dict['z'])

    accel_data_dict = {'x': x, 'y': y, 'z': z} #sensor.get_accel_data()
    accel_data = str(accel_data_dict['x']) + " " + \
                 str(accel_data_dict['y']) + " " + \
                 str(accel_data_dict['z'])
    sock.sendto(accel_data + " " + gyro_data + " " + str(time.time()), (MCAST_GRP, MCAST_PORT))
    time.sleep(1/60)
