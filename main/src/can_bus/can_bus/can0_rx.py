#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rclpy                                     # ROS2 Python Client Library
from rclpy.node import Node                      # ROS2 Node
from share.msg import RecvCAN0l
from share.msg import RecvCAN0r
import can

class Rx(Node):

    def __init__(self,name):
        super().__init__(name)

        self.recv_can_l = self.create_publisher(
            RecvCAN0l,
            'recv_can_l',
            40)
        
        self.recv_can_r = self.create_publisher(
            RecvCAN0r,
            'recv_can_r',
            40)


        self.timer = self.create_timer(0.0005, self.timer_callback)

    def timer_callback(self):
        can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan')
        message = can0.recv(0)
        msg_l = RecvCAN0l()
        msg_r = RecvCAN0r()
        if message != None:
            self.get_logger().info("True")
            if (message.arbitration_id == 0x582):
                # self.get_logger().info("False")
                msg_l.left_motor_stat = message.data
                self.recv_can_l.publish(msg_l)
            if (message.arbitration_id == 0x583):
                if(hex(int.from_bytes(message.data[:3], byteorder='big')) == 0x430521):
                    self.get_logger().info("False")
                    msg_r.right_motor_stat = message.data
                    self.recv_can_r.publish(msg_r)


def main(args=None):
    rclpy.init(args=args)
    node = Rx('recv_can0')
    rclpy.spin(node)
    node.destory_node()
    rclpy.shutdown()