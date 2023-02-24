#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rclpy                                     # ROS2 Python Client Library
from rclpy.node import Node                      # ROS2 Node
from share.msg import SendCAN0

class Encoder(Node):
    
    def __init__(self, name):
        super().__init__(name)

        self.pub_can = self.create_publisher(
            SendCAN0,
            'send_can0',
            20)

        self.timer = self.create_timer(0.1, self.timer_callback)

    def timer_callback(self):
        get_encoder = [0x40,0x05,0x21,0x00,0x0,0x00,0x00,0x00]
        msg = SendCAN0()
        msg.left_motor_data = get_encoder
        msg.right_motor_data = get_encoder
        self.pub_can.publish(msg)
        

def main(args=None):
    rclpy.init(args=args)
    node = Encoder('encoder_can0')
    rclpy.spin(node)
    node.destory_node()
    rclpy.shutdown()