from mpu6050 import mpu6050
import socket
import time

sensor = mpu6050(0x68)

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 8845

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

print("Callibrating. You have 10 seconds to lay hold the glove still and flat.")

speed = { 'x': 0, 'y': 0, 'z': 0 }
orientation = { 'x': 0, 'y': 0, 'z': 0 }

for i in range(1, 2):
    time.sleep(1)
    print(10 - i)

current_time = time.time()

while True:
    dt = current_time - time.time()
    current_time = time.time()

    # Get data
    gyro_data_dict = { 'x': 0, 'y': 0, 'z': 0 }
    gyro_data_dict = sensor.get_gyro_data()
    gyro_data = str(gyro_data_dict['x']) + " " + \
                str(gyro_data_dict['y']) + " " + \
                str(gyro_data_dict['z'])

    accel_data_dict = { 'x': 0, 'y': 0, 'z': 0 }
    accel_data_dict = sensor.get_accel_data()
    accel_data = str(accel_data_dict['x']) + " " + \
                 str(accel_data_dict['y']) + " " + \
                 str(accel_data_dict['z'])

    # Update state
    speed['x'] += accel_data_dict['x'] * dt
    speed['y'] += accel_data_dict['y'] * dt
    speed['z'] += accel_data_dict['z'] * dt

    orientation['x'] += gyro_data_dict['x'] * dt
    orientation['y'] += gyro_data_dict['y'] * dt
    orientation['z'] += gyro_data_dict['z'] * dt

    speed_data = str(speed['x']) + " " + str(speed['y']) + " " + str(speed['z'])
    orientation_data = str(orientation['x']) + " " + str(orientation['y'])\
        + " " + str(orientation['z'])

    sock.sendto(accel_data + " " + gyro_data + " " + \
        orientation_data + " " + speed_data, (MCAST_GRP, MCAST_PORT))

    time.sleep(1/30.0)
