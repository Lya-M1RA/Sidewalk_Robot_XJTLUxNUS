#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rclpy                                     # ROS2 Python Client Library
from rclpy.node import Node                      # ROS2 Node
from sensor_msgs.msg import Joy                  # ROS2 standard Joy Message
from share.msg import SendCAN0
from motor_instruct import *

class LocalController(Node):

    def __init__(self,name):
        super().__init__(name)

        self.sub_joy = self.create_subscription(
            Joy, 
            "/joy", 
            self.joy_recv, 
            10)

        self.pub_can = self.create_publisher(
            SendCAN0,
            '/send_can0',
            10)

        self.declare_parameter('gear', 0)
        self.declare_parameter('park', True)


    def joy_recv(self,msg):
        left_joy_x = msg.axes[0]
        left_joy_y = msg.axes[1]
        right_joy_x = msg.axes[2]
        right_joy_y = msg.axes[3]
        dpad_x = msg.axes[6]
        dpad_y = msg.axes[7]
        left_trigger = msg.axes[4]
        right_trigger = msg.axes[5]
        left_shoulder_button = msg.buttons[4]
        right_shoulder_button = msg.buttons[5]
        a_button = msg.buttons[0]
        b_button = msg.buttons[1]     
        x_button = msg.buttons[2]
        y_button = msg.buttons[3]
        select_button = msg.buttons[6]
        start_button = msg.buttons[7]
        xbox_button = msg.buttons[8]
        left_joy_button = msg.button[9]
        right_joy_button = msg.button[10]
        self.input_processor()


    def can_send(self, left_frame_data, right_frame_data):
        msg = SendCAN0()
        msg.left_motor_data = left_frame_data
        msg.right_motor_data = right_frame_data
        self.pub_can.publish(msg)


    def input_processor(self):
        
        









def main(args=None):
    rclpy.init(args=args)
    node = LocalController('local_controller')
    rclpy.spin(node)
    node.destory_node()
    rclpy.shutdown()
