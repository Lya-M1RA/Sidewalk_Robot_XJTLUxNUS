from re import T
from time import sleep
import rclpy                                     # ROS2 Python Client Library
from rclpy.node import Node                      # ROS2 Node
from sensor_msgs.msg import Joy                  # ROS2 standard Joy Message
from share.msg import SendCAN0
from std_msgs.msg import Float32
import message_filters
import math
from .motor_instruct import *


class UpperController(Node):

    cunrrent_mode = False
    mode_change = [False, False]
    emerg_stop = False
    if_emerg_stop = False

    def __init__(self,name):
        super().__init__(name)


        self.sub_joy = message_filters.Subscriber(self, Joy, "joy")
        
        self.sub_lwheel_speed = message_filters.Subscriber(self, Float32, "lwheel_vtarget")
        
        self.sub_rwheel_speed = message_filters.Subscriber(self, Float32, "rwheel_vtarget")     

        sub_instr = message_filters.TimeSynchronizer([self.sub_joy, self.sub_lwheel_speed, self.sub_rwheel_speed], 10)
        sub_instr.registerCallback(self.instr_recv)

        self.pub_can = self.create_publisher(SendCAN0, 'send_can0', 20)
        

    def instr_recv(self, joy, lwheel_vtarget, rwheel_vtarget):
        joy_input = {
            'left_joy_x'            : -joy.axes[0]     ,
            'left_joy_y'            :  joy.axes[1]     ,
            'right_joy_x'           : -joy.axes[2]     ,
            'right_joy_y'           :  joy.axes[3]     ,
            'dpad_x'                : -joy.axes[6]     ,
            'dpad_y'                :  joy.axes[7]     ,
            'left_trigger'          : -joy.axes[5]     ,
            'right_trigger'         : -joy.axes[4]     ,
            'left_shoulder_button'  :  joy.buttons[6]  ,
            'right_shoulder_button' :  joy.buttons[7]  ,
            'a_button'              :  joy.buttons[0]  ,
            'b_button'              :  joy.buttons[1]  ,   
            'x_button'              :  joy.buttons[3]  ,
            'y_button'              :  joy.buttons[4]  ,
            'select_button'         :  joy.buttons[15]  ,
            'start_button'          :  joy.buttons[11]  ,
            'xbox_button'           :  joy.buttons[16]  ,
            'left_joy_button'       :  joy.buttons[13]  ,
            'right_joy_button'      :  joy.buttons[14]  
        } 

        lwheel_speed = lwheel_vtarget.data
        rwheel_speed = rwheel_vtarget.data

        lwheel_rpm = self.speed2rpm(lwheel_speed)
        rwheel_rpm = self.speed2rpm(rwheel_speed)

        self.input_processor(joy_input, lwheel_rpm, rwheel_rpm)


    #  Converting speed (m/s) into wheel rotation (rpm)
    def speed2freq(speed):
        wheel_diameter = 285                    #  Measured diameter (mm) of the wheel
        perimeter = wheel_diameter * math.pi    #  Calculate the perimeter (mm) of the wheel
        rpm = speed * 1000 * 60 / perimeter     #  Calculate the rotation speed (rpm) of the wheel
        freq = rpm / 60 * 100                       #  Calculate the rotation frequency (Hz) of the wheel
        return freq

    #  Send instructions "can_tx" node
    def can_send(self, left_frame_data, right_frame_data):
        msg = SendCAN0()
        msg.left_motor_data = left_frame_data
        msg.right_motor_data = right_frame_data
        self.pub_can.publish(msg)


    # Process Xbox Controller input and spped instructions
    def input_processor(self, joy_input, lwheel_rpm, rwheel_rpm):
        if joy_input['y_button'] == 1 :
            self.mode_change = [self.mode_change[1], True]
        else :
            self.mode_change = [self.mode_change[1], False]

        if self.mode_change == [False, True]:
            self.cunrrent_mode = not self.current_mode

        if self.current_mode == True:
            if joy_input['x_button'] != 1 :
                if if_emerg_stop == True:
                    self.can_send(MotorMode('Speed Control'), MotorMode('Speed Control'))
                    if_emerg_stop = False
                self.can_send(RPMControl(-lwheel_rpm), RPMControl(rwheel_rpm))

            else :
                if_emerg_stop = True
                self.can_send(MotorMode('Emergency Stop'), MotorMode('Emergency Stop'))
        else :
            if_emerg_stop = True


def main(args=None):
    rclpy.init(args=args)
    node = UpperController('upper_controller')
    rclpy.spin(node)
    node.destory_node()
    rclpy.shutdown()
