import os
import sys
import json
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from uarm.wrapper import SwiftAPI


"""
uArm code for movement
moves based on the movement of the kinect, it doesn't let the user move past the allowed limit
Authors: Rony Tsirkel, Jake Savitt
"""

swift = SwiftAPI(filters={'hwid': 'USB VID:PID=2341:0042'}, cmd_pend_size=2, callback_thread_pool_size=1)

swift.waiting_ready()

device_info = swift.get_device_info()
print(device_info)
firmware_version = device_info['firmware_version']
if firmware_version and not firmware_version.startswith(('0.', '1.', '2.', '3.')):
    swift.set_speed_factor(0.00005)

swift.set_mode(0)

speed = 10000
# x Limits: 110mm - 330mm
# Y Limits: -350mm - 350mm
# Z Limits: max 160mm
# swift.reset(speed=speed)
#  (138.54,115.64,148.39)|(195.62,115.64,148.39)|(285.21,115.64,148.39)
# ---------------------------------------------------------------
#  (138.54,3.07,148.39)|(195.62,3.07,148.39)|(285.21,3.07,148.39)
# ---------------------------------------------------------------
#  (138.54,-115.64,148.39)|(195.62,-115.64,148.39)|(285.21,-115.64,148.39)
# y+:x+,x0,x- -> y0:x+,x0,x- -> y-:x+,x0,x- --> z

x_max = 285.21
x_min = 138.54
y_max = 115.64
y_min = -115.64
z_max = 156.13
z_min = 83
# base start
swift.reset()
swift.get_position(wait=False, callback=lambda i: print('pos', i))
# give x,y,z base position to keep them in loop
x_pos = 195.62
y_pos = 3.07
z_pos = 148.39

while swift.connected:
    with open('data.json') as json_file:
        input = json.load(json_file)

    if os.path.exists(input):
        hand = False
    else:
        hand  = True
        x_pos = input[x] * 0.118
        y_pos = input[y] * 0.138
        z_pos = input[z] * 0.07
    os.remove('data.json')

    # x_pos = 195.62
    # y_pos = 3.07
    # z_pos = 148.39
    # hand = True

    if x_pos > x_max:
        x_pos = x_max
    elif x_pos < x_min:
        x_pos = x_min
    if y_pos > y_max:
        y_pos = y_max
    elif y_pos < y_min:
        y_pos = y_min
    if z_pos > z_max:
        z_pos = z_max
    elif z_pos < z_min:
        z_pos = z_min
    # move based on hand
    swift.set_position(x=x_pos, y=y_pos, z=z_pos, speed=speed)
    swift.get_position(wait=False, callback=lambda i: print('pos', i))

    swift.set_pump(on=hand, timeout = 1)
    """
    # TOP
    # Position 1
    swift.set_position(x=285.21, y=115.64, z=156.13, speed=speed)
    swift.get_position(wait=False, callback=lambda i: print('pos', i))
    # Position 2
    swift.set_position(x=195.62, y=115.64, z=156.13, speed=speed)
    swift.get_position(wait=False, callback=lambda i: print('pos', i))
    # Position 3
    swift.set_position(x=138.54, y=115.64, z=156.13, speed=speed)
    swift.get_position(wait=False, callback=lambda i: print('pos', i))
    # Position 4
    swift.set_position(x=285.21, y=3.07, z=156.13, speed=speed)
    swift.get_position(wait=False, callback=lambda i: print('pos', i))
    # Position 5(center)
    swift.set_position(x=195.62, y=3.07, z=156.13, speed=speed)
    swift.get_position(wait=False, callback=lambda i: print('pos', i))
    # Position 6
    swift.set_position(x=138.54, y=3.07, z=156.13, speed=speed)
    swift.get_position(wait=False, callback=lambda i: print('pos', i))
    # Position 7
    swift.set_position(x=285.21, y=-115.64, z=156.13, speed=speed)
    swift.get_position(wait=False, callback=lambda i: print('pos', i))
    # Position 8
    swift.set_position(x=195.62, y=-115.64, z=156.13, speed=speed)
    swift.get_position(wait=False, callback=lambda i: print('pos', i))
    # Position 9
    swift.set_position(x=138.54, y=-115.64, z=156.13, speed=speed)
    swift.get_position(wait=False, callback=lambda i: print('pos', i))
    # MIDDLE
    # Position 1
    swift.set_position(x=285.21, y=115.64, z=148.39, speed=speed)
    swift.get_position(wait=False, callback=lambda i: print('pos', i))
    # Position 2
    swift.set_position(x=195.62, y=115.64, z=148.39, speed=speed)
    swift.get_position(wait=False, callback=lambda i: print('pos', i))
    # Position 3
    swift.set_position(x=138.54, y=115.64, z=148.39, speed=speed)
    swift.get_position(wait=False, callback=lambda i: print('pos', i))
    # Position 4
    swift.set_position(x=285.21, y=3.07, z=148.39, speed=speed)
    swift.get_position(wait=False, callback=lambda i: print('pos', i))
    # Position 5(center)
    swift.set_position(x=195.62, y=3.07, z=148.39, speed=speed)
    swift.get_position(wait=False, callback=lambda i: print('pos', i))
    # Position 6
    swift.set_position(x=138.54, y=3.07, z=148.39, speed=speed)
    swift.get_position(wait=False, callback=lambda i: print('pos', i))
    # Position 7
    swift.set_position(x=285.21, y=-115.64, z=148.39, speed=speed)
    swift.get_position(wait=False, callback=lambda i: print('pos', i))
    # Position 8
    swift.set_position(x=195.62, y=-115.64, z=148.39, speed=speed)
    swift.get_position(wait=False, callback=lambda i: print('pos', i))
    # Position 9
    swift.set_position(x=138.54, y=-115.64, z=148.39, speed=speed)
    swift.get_position(wait=False, callback=lambda i: print('pos', i))
    # BOTTOM
    # Position 1
    swift.set_position(x=285.21, y=115.64, z=83, speed=speed)
    swift.get_position(wait=False, callback=lambda i: print('pos', i))
    # Position 2
    swift.set_position(x=195.62, y=115.64, z=83, speed=speed)
    swift.get_position(wait=False, callback=lambda i: print('pos', i))
    # Position 3
    swift.set_position(x=138.54, y=115.64, z=83, speed=speed)
    swift.get_position(wait=False, callback=lambda i: print('pos', i))
    # Position 4
    swift.set_position(x=285.21, y=3.07, z=83, speed=speed)
    swift.get_position(wait=False, callback=lambda i: print('pos', i))
    # Position 5(center)
    swift.set_position(x=195.62, y=3.07, z=83, speed=speed)
    swift.get_position(wait=False, callback=lambda i: print('pos', i))
    # Position 6
    swift.set_position(x=138.54, y=3.07, z=83, speed=speed)
    swift.get_position(wait=False, callback=lambda i: print('pos', i))
    # Position 7
    swift.set_position(x=285.21, y=-115.64, z=83, speed=speed)
    swift.get_position(wait=False, callback=lambda i: print('pos', i))
    # Position 8
    swift.set_position(x=195.62, y=-115.64, z=83, speed=speed)
    swift.get_position(wait=False, callback=lambda i: print('pos', i))
    # Position 9
    swift.set_position(x=138.54, y=-115.64, z=83, speed=speed)
    swift.get_position(wait=False, callback=lambda i: print('pos', i))
"""
