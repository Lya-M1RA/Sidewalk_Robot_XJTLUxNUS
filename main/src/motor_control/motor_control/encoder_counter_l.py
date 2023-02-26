#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rclpy                                     # ROS2 Python Client Library
from rclpy.node import Node                      # ROS2 Node
from share.msg import RecvCAN0l
from std_msgs import Int16

class Counter(Node):
    def __init__(self,name):
        super().__init__(name)

        self.sub_recv = self.create_subscription(
            RecvCAN0l, 
            "recv_can0_l", 
            self.encoder, 
            10)

        self.pub_lwheel = self.create_publisher(
            Int16,
            'lwheel',
            10)

    def encoder(self, msg):
        l_msg = msg.left_motor_stat
        # self.get_logger().info(l_msg)
        l_count = - int.from_bytes(bytearray(l_msg[4:8]), byteorder= 'little', signed=True)
        l_output = Int16()
        l_output.data = l_count
        self.pub_lwheel.publish(l_output)


def main(args=None):
    rclpy.init(args=args)
    node = Counter('encoder_counter_l')
    rclpy.spin(node)
    node.destory_node()
    rclpy.shutdown()
