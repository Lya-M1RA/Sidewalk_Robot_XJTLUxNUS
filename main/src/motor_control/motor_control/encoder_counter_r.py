#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rclpy                                     # ROS2 Python Client Library
from rclpy.node import Node                      # ROS2 Node
from share.msg import RecvCAN0r
from std_msgs.msg import Int16
import numpy as np

class Counter(Node):
    def __init__(self,name):
        super().__init__(name)

        self.sub_recv = self.create_subscription(
            RecvCAN0r, 
            "recv_can_r", 
            self.encoder, 
            10)

        self.pub_rwheel = self.create_publisher(
            Int16,
            'rwheel',
            10)

    def encoder(self, msg):
        r_msg = msg.right_motor_stat
        r_32 = int.from_bytes(bytearray(r_msg[4:8]), byteorder= 'little', signed=True)
        r_np = np.array([r_32])
        r_output = Int16()
        r_output.data = r_np.astype(np.int16)[0]
        self.pub_rwheel.publish(r_output)


def main(args=None):
    rclpy.init(args=args)
    node = Counter('encoder_counter_l')
    rclpy.spin(node)
    node.destory_node()
    rclpy.shutdown()
