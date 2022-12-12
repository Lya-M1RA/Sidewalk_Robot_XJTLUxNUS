

def GenerateFrame(data_byte_num, index_num, data):

    data_byte_num_dict = {
    1: 0x2F,
    2: 0x2B,
    3: 0x27,
    4: 0x23,
    5: 0x40,
    }

    frame_data = [data_byte_num_dict.get(data_byte_num)] + index_num + [0x00] + data

    return frame_data


def MotorMode(mode):

    if mode == 'Normal Stop':
        frame_data = GenerateFrame(1, [0x00, 0x20], [0x10,0x00,0x00,0x00])
    elif mode == 'Emergency Stop':
        frame_data = GenerateFrame(1, [0x00, 0x20], [0x11,0x00,0x00,0x00])
    elif mode == 'Free Stop':
        frame_data = GenerateFrame(1, [0x00, 0x20], [0x12,0x00,0x00,0x00])
    elif mode == 'PWM Control':
        frame_data = GenerateFrame(1, [0x00, 0x20], [0x00,0x00,0x00,0x00])
    elif mode == 'Speed Control':
        frame_data = GenerateFrame(1, [0x00, 0x20], [0x01,0x00,0x00,0x00])
    elif mode == 'Torque Control':
        frame_data = GenerateFrame(1, [0x00, 0x20], [0x02,0x00,0x00,0x00])
    elif mode == 'Position Control':
        frame_data = GenerateFrame(1, [0x00, 0x20], [0x03,0x00,0x00,0x00])

    return frame_data


def PWMControl(pwm):

    param = int(pwm * 10)

    data = []
    for i in range(0,4):
        digit = i * 8
        data.append((param >> digit) & 0xFF)

    frame_data = GenerateFrame(4, [0x01, 0x20], data)

    return frame_data


def RPMControl(rpm):

    param = int(rpm)

    data = []
    for i in range(0,4):
        digit = i * 8
        data.append((param >> digit) & 0xFF)

    frame_data = GenerateFrame(4, [0x01, 0x20], data)

    return frame_data

def TorqueControl(current):

    param = int (current * 100)

    data = []
    for i in range(0,4):
        digit = i * 8
        data.append((param >> digit) & 0xFF)

    frame_data = GenerateFrame(4, [0x01, 0x20], data)

    return frame_data


def PositionType(type):

    if type == 'Absolute Position':
        frame_data = GenerateFrame(1, [0x02, 0x20], [0x00,0x00,0x00,0x00])
    elif type == 'Relative Position':
        frame_data = GenerateFrame(1, [0x02, 0x20], [0x01,0x00,0x00,0x00])

    return frame_data


def TargetPosition(position):

    param = int(position)

    data = []
    for i in range(0,4):
        digit = i * 8
        data.append((param >> digit) & 0xFF)

    frame_data = GenerateFrame(4, [0x03, 0x20], data)

    return frame_data


def ResetPosition():

    frame_data = GenerateFrame(4, [0x0F, 0x20], [0x00,0x00,0x00,0x00])

    return frame_data

