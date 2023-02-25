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


        self.timer = self.create_timer(0.005, self.timer_callback)

    def timer_callback(self):
        can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan')
        message = can0.recv(0)
        # self.get_logger().info(message)
        msg_l = RecvCAN0l()
        msg_r = RecvCAN0r()
        if message != None:
            if (message.arbitration_id == 0x582) & (message.data[0:2] == [0x43,0x05,0x21]):
                msg_l.left_motor_stat = message.data
                self.recv_can_l.publish(msg_l)
            if (message.arbitration_id == 0x583) & (message.data[0:2] == [0x43,0x05,0x21]):
                msg_r.right_motor_stat = message.data
                self.recv_can.publish(msg_r)


def main(args=None):
    rclpy.init(args=args)
    node = Rx('recv_can0')
    rclpy.spin(node)
    node.destory_node()
    rclpy.shutdown()