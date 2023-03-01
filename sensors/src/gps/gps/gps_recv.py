from socket import *
import time
import rclpy                                     # ROS2 Python Client Library
from rclpy.node import Node   

class GPS(Node):

    def __init__(self,name):
        super().__init__(name)

        self.pub_can = self.create_publisher(
            GPS,
            'gps',
            5)

def main(args=None):
    rclpy.init(args=args)
    node = GPS('gps_node')
    rclpy.spin(node)
    node.destory_node()
    rclpy.shutdown()
