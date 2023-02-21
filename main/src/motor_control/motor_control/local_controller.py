#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from re import T
from time import sleep
import rclpy                                     # ROS2 Python Client Library
from rclpy.node import Node                      # ROS2 Node
from sensor_msgs.msg import Joy                  # ROS2 standard Joy Message
from share.msg import SendCAN0
from .motor_instruct import *


class LocalController(Node):

    gear = [False, 0]
    emerg_stop = [False, False]
    parking_mode = [False, False, False]
    orientation = 0
    throttle = [0, False]
    last_throttle = 0
    brake = [0, False]

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
            LocalController.emerg_stop[1] = True
        else:
            LocalController.emerg_stop[1] = False
        
        if input['x_button'] == 1:
            if LocalController.gear[0] == False:
                LocalController.gear[0] = True
                if LocalController.gear[1] == 1:
                    LocalController.gear [1] = -1
                else:
                    LocalController.gear[1] = LocalController.gear[1] + 1
        else:
            LocalController.gear[0] = False

        if input['y_button'] == 1:
            if LocalController.parking_mode[0] == False:
                LocalController.parking_mode[0] = True
                LocalController.parking_mode[2] = not LocalController.parking_mode[2]
        else:
            LocalController.parking_mode[0] = False

        LocalController.orientation = input['left_joy_x']
        LocalController.throttle[0] = input['right_trigger']
        LocalController.brake[0] = input['left_trigger']

        if LocalController.emerg_stop[1] == True:
            LocalController.throttle[1] = False
            if LocalController.emerg_stop[0] == False:
                LocalController.emerg_stop[0] == True
                self.can_send(MotorMode('Emergency Stop'), MotorMode('Emergency Stop'))
        else:
            LocalController.emerg_stop[0] = False

            if LocalController.parking_mode[2] == True:
                LocalController.throttle[1] = False
                if LocalController.parking_mode[1] == False:
                    LocalController.parking_mode[1] = True
                    self.can_send(MotorMode('Position Control'), MotorMode('Position Control'))
                    self.can_send(PositionType('Relative Position'), PositionType('Relative Position'))
                    self.can_send(TargetPosition(0),TargetPosition(0))
            else:
                LocalController.emerg_stop[1] = False

                if LocalController.brake[0] != -1:
                    LocalController.throttle[1] = False
                    if LocalController.brake[1] == False:
                        LocalController.brake[1] = True
                    #     self.can_send(MotorMode('Torque Control'), MotorMode('Torque Control'))

                    # brake_factor = 2.5
                    # brake_turning_factor = 0.1
                    # brake_current = brake_factor * (brake + 1)
                    # self.can_send(
                    #     TorqueControl(-brake_current + brake_turning_factor * orientation * (- brake + 3) * 0.25), 
                    #     TorqueControl( brake_current - brake_turning_factor * orientation * (- brake + 3) * 0.25)
                    # )
                        self.can_send(MotorMode('Speed Control'), MotorMode('Speed Control'))
                        self.can_send(RPMControl(0),RPMControl(0))

                else:
                    LocalController.brake[1] = False
                    if LocalController.throttle[0] <= LocalController.last_throttle - 0.2:
                        LocalController.last_throttle = LocalController.throttle[0]
                        LocalController.throttle[1] = False
                        self.can_send(MotorMode('Free Stop'), MotorMode('Free Stop'))
                    else:
                        LocalController.last_throttle = LocalController.throttle[0]
                        if LocalController.throttle[1] == False:
                            LocalController.throttle[1] = True
                            self.can_send(MotorMode('Speed Control'), MotorMode('Speed Control'))
                        if LocalController.gear[1] == 1:
                            rpm_factor = 100
                            rpm_turning_factor = 0.4
                            rpm = rpm_factor * (LocalController.throttle[0] + 1) * 0.5
                            self.can_send(
                                RPMControl(- rpm + LocalController.orientation * rpm_factor * rpm_turning_factor * (-LocalController.throttle[0] + 5) / 3),
                                RPMControl(  rpm + LocalController.orientation * rpm_factor * rpm_turning_factor * (-LocalController.throttle[0] + 5) / 3)
                            )
                        elif LocalController.gear[1] == 0:
                            rpm_factor = 50
                            rpm_turning_factor = 0.5
                            rpm = rpm_factor * (LocalController.throttle[0] + 1) * 0.5
                            self.can_send(
                                RPMControl(- rpm + LocalController.orientation * rpm_factor * rpm_turning_factor * (-LocalController.throttle[0] + 5) / 3),
                                RPMControl(  rpm + LocalController.orientation * rpm_factor * rpm_turning_factor * (-LocalController.throttle[0] + 5) / 3)
                            )
                        elif LocalController.gear[1] == -1:
                            rpm_factor = -50
                            rpm_turning_factor = 0.5
                            rpm = rpm_factor * (LocalController.throttle[0] + 1) * 0.5
                            self.can_send(
                                RPMControl(- rpm + LocalController.orientation * rpm_factor * rpm_turning_factor * (-LocalController.throttle[0] + 5) / 3),
                                RPMControl(  rpm + LocalController.orientation * rpm_factor * rpm_turning_factor * (-LocalController.throttle[0] + 5) / 3)
                            )


def main(args=None):
    rclpy.init(args=args)
    node = LocalController('local_controller')
    rclpy.spin(node)
    node.destory_node()
    rclpy.shutdown()
