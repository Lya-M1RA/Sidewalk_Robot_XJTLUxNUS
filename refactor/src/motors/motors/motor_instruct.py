def GenerateFrame(data_byte_num, index_num, data):
    data_byte_num_dict = {
        1: 0x2F,
        2: 0x2B,
        3: 0x27,
        4: 0x23,
        5: 0x40,
    }
    return [data_byte_num_dict.get(data_byte_num)] + index_num + [0x00] + data


# 
def MotorMode(mode):
    modes = {
        'Normal Stop': [0x10, 0x00, 0x00, 0x00],
        'Emergency Stop': [0x11, 0x00, 0x00, 0x00],
        'Free Stop': [0x12, 0x00, 0x00, 0x00],
        'PWM Control': [0x00, 0x00, 0x00, 0x00],
        'Speed Control': [0x01, 0x00, 0x00, 0x00],
        'Torque Control': [0x02, 0x00, 0x00, 0x00],
        'Position Control': [0x03, 0x00, 0x00, 0x00],
    }
    return GenerateFrame(1, [0x00, 0x20], modes[mode])


def PWMControl(pwm):
    param = int(pwm * 10)
    data = [(param >> (i * 8)) & 0xFF for i in range(4)]
    return GenerateFrame(4, [0x01, 0x20], data)


def RPMControl(rpm):
    param = int(rpm)
    data = [(param >> (i * 8)) & 0xFF for i in range(4)]
    return GenerateFrame(4, [0x01, 0x20], data)


def TorqueControl(current):
    param = int(current * 100)
    data = [(param >> (i * 8)) & 0xFF for i in range(4)]
    return GenerateFrame(4, [0x01, 0x20], data)


def PositionType(type):
    types = {
        'Absolute Position': [0x00, 0x00, 0x00, 0x00],
        'Relative Position': [0x01, 0x00, 0x00, 0x00],
    }
    return GenerateFrame(1, [0x02, 0x20], types[type])


def TargetPosition(position):
    param = int(position)
    data = [(param >> (i * 8)) & 0xFF for i in range(4)]
    return GenerateFrame(4, [0x03, 0x20], data)


def ResetPosition():
    return GenerateFrame(4, [0x0F, 0x20], [0x00] * 4)

