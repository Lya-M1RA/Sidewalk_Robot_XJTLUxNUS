# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-

# import rclpy                                     # ROS2 Python Client Library
# from rclpy.node import Node                      # ROS2 Node
# from share.msg import RecvCAN0
# from share.msg import lwheel
# from share.msg import rwheel

# class Counter(Node):
#     def __init__(self,name):
#         super().__init__(name)

#         self.sub_recv = self.create_subscription(
#             RecvCAN0, 
#             "recv_can0", 
#             self.encoder, 
#             10)

#         self.pub_lwheel = self.create_publisher(
#             lwheel,
#             'send_lwheel',
#             10)

#     def encoder(self, msg):
