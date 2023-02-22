#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rclpy                                     # ROS2 Python Client Library
from rclpy.node import Node                      # ROS2 Node
from share.msg import SendCAN0
import can

class Tx(Node):
    
    def __init__(self, name):
        super().__init__(name)

        self.sub_can = self.create_subscription(
            SendCAN0,
            '/send_can0',
            self.send,
            20)

    def send(self, msg):
        can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan')
        left_msg = can.Message(is_extended_id=False, arbitration_id=0x602, data=msg.left_motor_data)
        right_msg = can.Message(is_extended_id=False, arbitration_id=0x603, data=msg.right_motor_data)
        can0.send(left_msg)
        can0.send(right_msg)
        

def main(args=None):
    rclpy.init(args=args)
    node = Tx('send_can0')
    rclpy.spin(node)
    node.destory_node()
    rclpy.shutdown()
