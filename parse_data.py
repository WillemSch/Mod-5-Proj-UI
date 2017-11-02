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

def parse_steering_state(data):
    return int(data.split(" ")[0])

def parse_speed_state(data):
    return float(data.split(" ")[1])

