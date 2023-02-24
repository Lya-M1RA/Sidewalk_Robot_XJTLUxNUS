#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rclpy                                     # ROS2 Python Client Library
from rclpy.node import Node                      # ROS2 Node
from share.msg import RecvCAN0
from std_msgs.msg import Int16

class Counter(Node):
    def __init__(self,name):
        super().__init__(name)

        self.sub_recv = self.create_subscription(
            RecvCAN0, 
            "recv_can0", 
            self.encoder, 
            10)

        self.pub_lwheel = self.create_publisher(
            Int16,
            'lwheel',
            10)

        self.pub_rwheel = self.create_publisher(
            Int16,
            'rwheel',
            10)

    def encoder(self, msg):
        l_msg = msg.left_motor_stat
        r_msg = msg.right_motor_stat
        l_count = int.from_bytes(l_msg[4:7], byteorder= 'little')
        r_count = int.from_bytes(r_msg[4:7], byteorder= 'little')
        if (l_count in range(-32768,32767) and r_count in range(-32768,32767)):
            l_output = Int16()
            l_output.data = l_count
            r_output = Int16()
            r_output.data = r_count
            self.pub_lwheel.publish(l_output)
            self.pub_rwheel.publish(r_output)


def main(args=None):
    rclpy.init(args=args)
    node = Counter('encoder_counter')
    rclpy.spin(node)
    node.destory_node()
    rclpy.shutdown()
