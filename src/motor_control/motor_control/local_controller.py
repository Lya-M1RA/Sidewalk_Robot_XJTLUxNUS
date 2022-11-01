#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from re import T
from time import sleep
import rclpy                                     # ROS2 Python Client Library
from rclpy.node import Node                      # ROS2 Node
from sensor_msgs.msg import Joy                  # ROS2 standard Joy Message
from share.msg import SendCAN0
from motor_instruct.py import *

gear = [False, 0]
emerg_stop = False
parking_mode = [False, False]
orientation = 0
throttle = 0
brake = 0

class LocalController(Node):

    def __init__(self,name):
        super().__init__(name)


        self.sub_joy = self.create_subscription(
            Joy, 
            "joy", 
            self.joy_recv, 
            10)

        self.pub_can = self.create_publisher(
            SendCAN0,
            'send_can0',
            10)


    def joy_recv(self,msg):
        input = {
            'left_joy_x'            : -msg.axes[0]     ,
            'left_joy_y'            :  msg.axes[1]     ,
            'right_joy_x'           : -msg.axes[2]     ,
            'right_joy_y'           :  msg.axes[3]     ,
            'dpad_x'                : -msg.axes[6]     ,
            'dpad_y'                :  msg.axes[7]     ,
            'left_trigger'          : -msg.axes[5]     ,
            'right_trigger'         : -msg.axes[4]     ,
            'left_shoulder_button'  :  msg.buttons[6]  ,
            'right_shoulder_button' :  msg.buttons[7]  ,
            'a_button'              :  msg.buttons[0]  ,
            'b_button'              :  msg.buttons[1]  ,   
            'x_button'              :  msg.buttons[3]  ,
            'y_button'              :  msg.buttons[4]  ,
            'select_button'         :  msg.buttons[15]  ,
            'start_button'          :  msg.buttons[11]  ,
            'xbox_button'           :  msg.buttons[16]  ,
            'left_joy_button'       :  msg.buttons[13]  ,
            'right_joy_button'      :  msg.buttons[14]  
        } 
        self.input_processor(input)


    def can_send(self, left_frame_data, right_frame_data):
        msg = SendCAN0()
        msg.left_motor_data = left_frame_data
        msg.right_motor_data = right_frame_data
        self.pub_can.publish(msg)


    def input_processor(self, input):

        if input['b_button'] == 1:
            emerg_stop = True
        else:
            emerg_stop = False
        
        if input['x_button'] == 1:
            if gear[0] == False:
                gear[0] = True
                if gear[1] == 2:
                    gear [1] = -1
                else:
                    gear[1] = gear[1] + 1
        else:
            gear[0] = False

        if input['y_button'] == 1:
            if parking_mode[0] == False:
                parking_mode[0] = True
                parking_mode[1] = not parking_mode[1]
        else:
            parking_mode[0] = False

        orientation = input['left_joy_x']
        throttle = input['right_trigger']
        brake = input['left_trigger']

        if emerg_stop == True:
            self.can_send(MotorMode('Emergency Stop'), MotorMode('Emergency Stop'))
            sleep(0.5)
            self.can_send(MotorMode('Position Control'), MotorMode('Position Control'))
            self.can_send(PositionType('Relative Position'), PositionType('Relative Position'))
            self.can_send(TargetPosition(0),TargetPosition(0))
        elif parking_mode[1] == True:
            self.can_send(MotorMode('Position Control'), MotorMode('Position Control'))
            self.can_send(PositionType('Relative Position'), PositionType('Relative Position'))
            self.can_send(TargetPosition(0),TargetPosition(0))
        elif brake != -1:
            self.can_send(MotorMode('Torque Control'), MotorMode('Torque Control'))
            brake_factor = 2.5
            brake_turning_factor = 0.2
            brake_current = brake_factor * (brake + 1)
            self.can_send(
                TorqueControl(-brake_current * (1 - brake_turning_factor * orientation) * (- brake + 3) * 0.25), 
                TorqueControl( brake_current * (1 + brake_turning_factor * orientation) * (- brake + 3) * 0.25)
                )
        else:
            self.can_send(MotorMode('PWM Control'), MotorMode('PWM Control'))
            if gear[1] == 2:
                pwm_factor = 900
                pwm_turning_factor = 0.1
                self.can_send(
                    PWMControl(throttle * pwm_factor + orientation * pwm_factor * pwm_turning_factor * (-throttle + 3) * 0.25),
                    PWMControl(throttle * pwm_factor - orientation * pwm_factor * pwm_turning_factor * (-throttle + 3) * 0.25)
                )
            elif gear[1] == 1:
                pwm_factor = 500
                pwm_turning_factor = 0.2
                self.can_send(
                    PWMControl(throttle * pwm_factor + orientation * pwm_factor * pwm_turning_factor * (-throttle + 3) * 0.25),
                    PWMControl(throttle * pwm_factor - orientation * pwm_factor * pwm_turning_factor * (-throttle + 3) * 0.25)
                )
            elif gear[1] == 0:
                pwm_factor = 200
                pwm_turning_factor = 0.5
                self.can_send(
                    PWMControl(throttle * pwm_factor + orientation * pwm_factor * pwm_turning_factor * (-throttle + 3) * 0.25),
                    PWMControl(throttle * pwm_factor - orientation * pwm_factor * pwm_turning_factor * (-throttle + 3) * 0.25)
                )
            elif gear[1] == -1:
                pwm_factor = -150
                pwm_turning_factor = 1
                self.can_send(
                    PWMControl(throttle * pwm_factor + orientation * pwm_factor * pwm_turning_factor * (-throttle + 3) * 0.25),
                    PWMControl(throttle * pwm_factor - orientation * pwm_factor * pwm_turning_factor * (-throttle + 3) * 0.25)
                )



def main(args=None):
    rclpy.init(args=args)
    node = LocalController('local_controller')
    rclpy.spin(node)
    node.destory_node()
    rclpy.shutdown()
