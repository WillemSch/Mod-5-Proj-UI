def parse_accel(data):
    accel_dict = {}
    accel_dict['x'] = round(float(data.split(" ")[0]), 4)
    accel_dict['y'] = round(float(data.split(" ")[1]), 4)
    accel_dict['z'] = round(float(data.split(" ")[2]), 4)
    return accel_dict

def parse_gyro(data):
    gyro_dict = {}
    gyro_dict['x'] = round(float(data.split(" ")[3]), 4)
    gyro_dict['y'] = round(float(data.split(" ")[4]), 4)
    gyro_dict['z'] = round(float(data.split(" ")[5]), 4)
    return gyro_dict

# Takes the 3 acceleration axes and returns the orientation
def grav_to_angle(x, y, z):
    orientation = {'x': 0, 'y': 0, 'z': 0}

    return orientation
