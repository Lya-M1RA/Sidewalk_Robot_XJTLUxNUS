#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rclpy                                     # ROS2 Python Client Library
from rclpy.node import Node                      # ROS2 Node
from share.msg import RecvCAN0
import can

class Rx(Node):

    def __init__(self,name):
        super().__init__(name)

        self.recv_can = self.create_publisher(
            RecvCAN0,
            'recv_can0',
            20)

        self.timer = self.create_timer(0.0025, self.timer_callback)

    def timer_callback(self):
        can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan')
        message = can0.recv(0)
        msg = RecvCAN0()
        if message is not None:
            if message.arbitration_id == 0x602:
                msg.left_motor_stat = message.data
            if message.arbitration_id == 0x603:
                msg.right_motor_stat = message.data
            self.recv_can.publish(msg)



def main(args=None):
    rclpy.init(args=args)
    node = Rx('receive_can0')
    rclpy.spin(node)
    node.destory_node()
    rclpy.shutdown()