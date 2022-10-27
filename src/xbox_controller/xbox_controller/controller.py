#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from unicodedata import name
import rclpy                                     # ROS2 Python Client Library
from rclpy.node import Node                      # ROS2 Node
from sensor_msgs.msg import Joy                  # ROS2 standard Joy Message

class ReadController(Node):

    def __init__(self, name):
        super().__init__(name)
        self.sub = self.create_subscription(Joy, "/joy", self.listener_callback, 10)

    def listener_callback(self, msg):
        self.get_logger().info('L-Joystick-x: ', msg.axes[0])

def main(args=None):
    rclpy.init(args=args)
    node = ReadController("read_controller")
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
 