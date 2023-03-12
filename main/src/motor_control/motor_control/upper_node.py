from re import T
from time import sleep
import rclpy                                     # ROS2 Python Client Library
from rclpy.node import Node                      # ROS2 Node
from sensor_msgs.msg import Joy                  # ROS2 standard Joy Message
from share.msg import SendCAN0
from std_msgs.msg import Float32
import math
from .motor_instruct import *


class UpperController(Node):

    current_mode = False
    mode_change = [False, False]
    emerg_stop = False
    if_emerg_stop = False

    lwheel_freq = 0
    rwheel_freq = 0

    joy_input = dict()
    

    def __init__(self,name):
        super().__init__(name)

        self.sub_joy = self.create_subscription(
            Float32, 
            "lwheel_vtarget", 
            self.lwheel_recv, 
            10)
        
        self.sub_joy = self.create_subscription(
            Float32, 
            "rwheel_vtarget", 
            self.rwheel_recv, 
            10)
        

        self.sub_joy = self.create_subscription(
            Joy, 
            "joy", 
            self.joy_recv, 
            10)
        
        self.pub_can = self.create_publisher(SendCAN0, 'send_can0', 20)

        self.timer = self.create_timer(0.005, self.timer_callback)


    def timer_callback(self):
        self.input_processor()
        

    def lwheel_recv(self, lwheel_vtarget):
        self.lwheel_freq = self.speed2freq(lwheel_vtarget.data)


    def rwheel_recv(self, rwheel_vtarget):  
        self.rwheel_freq = self.speed2freq(rwheel_vtarget.data)


    def joy_recv(self, joy):
            self.joy_input['left_joy_x']            = -joy.axes[0]    
            self.joy_input['left_joy_y']            =  joy.axes[1]    
            self.joy_input['right_joy_x']           = -joy.axes[2]    
            self.joy_input['right_joy_y']           =  joy.axes[3]    
            self.joy_input['dpad_x']                = -joy.axes[6]    
            self.joy_input['dpad_y']                =  joy.axes[7]    
            self.joy_input['left_trigger']          = -joy.axes[5]    
            self.joy_input['right_trigger']         = -joy.axes[4]    
            self.joy_input['left_shoulder_button']  =  joy.buttons[6] 
            self.joy_input['right_shoulder_button'] =  joy.buttons[7] 
            self.joy_input['a_button']              =  joy.buttons[0] 
            self.joy_input['b_button']              =  joy.buttons[1]   
            self.joy_input['x_button']              =  joy.buttons[3] 
            self.joy_input['y_button']              =  joy.buttons[4] 
            self.joy_input['select_button']         =  joy.buttons[15]
            self.joy_input['start_button']          =  joy.buttons[11]
            self.joy_input['xbox_button']           =  joy.buttons[16]
            self.joy_input['left_joy_button']       =  joy.buttons[13]
            self.joy_input['right_joy_button']      =  joy.buttons[14]


    #  Converting speed (m/s) into wheel rotation (rpm)
    def speed2freq(self, speed):
        wheel_diameter = 285                    #  Measured diameter (mm) of the wheel
        perimeter = wheel_diameter * math.pi    #  Calculate the perimeter (mm) of the wheel
        rpm = speed * 1000 * 60 / perimeter     #  Calculate the rotation speed (rpm) of the wheel
        freq = rpm * 5                          #  Calculate the rotation frequency (Hz) of the wheel
        return freq


    #  Send instructions "can_tx" node
    def can_send(self, left_frame_data, right_frame_data):
        msg = SendCAN0()
        msg.left_motor_data = left_frame_data
        msg.right_motor_data = right_frame_data
        self.pub_can.publish(msg)


    # Process Xbox Controller input and spped instructions
    def input_processor(self):
        if self.joy_input['y_button'] == 1 :
            self.mode_change = [self.mode_change[1], True]
        else :
            self.mode_change = [self.mode_change[1], False]

        if self.mode_change == [False, True]:
            self.current_mode = not self.current_mode

        if self.current_mode == True:
            if self.joy_input['x_button'] != 1 :
                if self.if_emerg_stop == True:
                    self.can_send(MotorMode('Speed Control'), MotorMode('Speed Control'))
                    self.if_emerg_stop = False
                self.can_send(RPMControl(-self.lwheel_freq), RPMControl(self.rwheel_freq))

            else :
                self.if_emerg_stop = True
                self.can_send(MotorMode('Emergency Stop'), MotorMode('Emergency Stop'))
        else :
            self.if_emerg_stop = True
            self.can_send(MotorMode('Free Stop'), MotorMode('Free Stop'))



def main(args=None):
    rclpy.init(args=args)
    node = UpperController('upper_controller')
    rclpy.spin(node)
    node.destory_node()
    rclpy.shutdown()
