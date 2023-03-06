#!./venv/bin/python3.8

import rclpy                            # ROS2 Python接口库
from rclpy.node import Node             # ROS2 节点类
from sensor_msgs.msg import Image       # 图像消息类型
from cv_bridge import CvBridge          # ROS与OpenCV图像转换类
import cv2                              # Opencv图像处理库
import numpy as np                      # Python数值计算库
import torch
import torchvision.transforms as transforms
import networks

class Depth(Node):
    def __init__(self, name):
        super().__init__(name)                      # ROS2节点父类初始化

        self.depth_encoder = networks.ResnetEncoder(18, False)
        self.depth_decoder = networks.HRDepthDecoder(self.depth_encoder.num_ch_enc)

        depth_encoder_path = "./model/HR_Depth_K_M_1280x384/encoder.pth"
        depth_decoder_path = "./model/HR_Depth_K_M_1280x384/depth.pth"

        encoder_dict = torch.load(depth_encoder_path)
        self.img_height = encoder_dict["height"]
        self.img_width = encoder_dict["width"]

        self.get_logger().info("Test image height is:" + str(self.img_height))
        self.get_logger().info("Test image width is:" + str(self.img_width))
        load_dict = {k: v for k, v in encoder_dict.items() if k in self.depth_encoder.state_dict()}

        decoder_dict = torch.load(depth_decoder_path)

        self.depth_encoder.load_state_dict(load_dict)
        self.depth_decoder.load_state_dict(decoder_dict)

        device = torch.device("cuda:0")
        self.depth_encoder.to(device)
        self.depth_decoder.to(device)

        self.sub = self.create_subscription(
            Image, 'image_raw', 
            self.listener_callback, 
            10)                                     # 创建订阅者对象（消息类型、话题名、订阅者回调函数、队列长度）

        self.cv_bridge = CvBridge() 


    def est_depth(self, image):
        device = torch.device("cuda:0")
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (self.img_width, self.img_height))

        image_tensor = transforms.ToTensor()(image).unsqueeze(0).to(device)

        # predict depth from single image
        result = self.depth_decoder(self.depth_encoder(image_tensor))

        # cv2.imshow("Est_Depth", result.cpu().squeeze().numpy())  # 不使用OpenCV

        result = re
        cv2.imshow("Est_Depth", result)                           # 使用OpenCV显示处理后的图像效果
        cv2.waitKey(10)


    def listener_callback(self, data):
        self.get_logger().info('Receiving video frame')         # 输出日志信息，提示已进入回调函数
        image = self.cv_bridge.imgmsg_to_cv2(data, 'bgr8')      # 将ROS的图像消息转化成OpenCV图像
        self.est_depth(image)     


def main(args=None):                            # ROS2节点主入口main函数
    rclpy.init(args=args)                       # ROS2 Python接口初始化
    node = Depth("est_depth")                   # 创建ROS2节点对象并进行初始化
    rclpy.spin(node)                            # 循环等待ROS2退出
    node.destroy_node()                         # 销毁节点对象
    rclpy.shutdown()                            # 关闭ROS2 Python接口                     