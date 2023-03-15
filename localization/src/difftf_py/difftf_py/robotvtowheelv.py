import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32

class MyNode(Node):
    def __init__(self):
        super().__init__('robotvtowheelv')

        self.create_subscription(
            Twist, '/cmd_vel', self.cmd_vel_callback, 10)
        self.left_pub = self.create_publisher(
            Float32, '/lwheel_vtarget', 10)
        self.right_pub = self.create_publisher(
            Float32, '/rwheel_vtarget', 10)
        self.wheel_base = 0.585 # 轴距
        # self.linear_vel_last = 0
        # self.angular_vel_last = 0

    def cmd_vel_callback(self, msg):
        # 根据cmd_vel计算轮子速度
        linear_vel = msg.linear.x
        angular_vel = msg.angular.z
        # 滤波
        # if (self.linear_vel_last != 0.0) & (linear_vel == 0.0):
        #     linear_vel = self.linear_vel_last
        
        # if (self.angular_vel_last != 0.0) & (angular_vel == 0.0):
        #     angular_vel = self.angular_vel_last

        # self.linear_vel_last = linear_vel
        # self.angular_vel_last = angular_vel
        
        left_wheel_vel = (2*linear_vel - angular_vel*self.wheel_base) / 2
        right_wheel_vel = (2*linear_vel + angular_vel*self.wheel_base) / 2
        # left_wheel_vel = 0.5
        # right_wheel_vel = 0.5



        
        msg_left = Float32()

        msg_right = Float32()
        msg_left.data = left_wheel_vel
        msg_right.data = right_wheel_vel
        # 发布轮子速度
        self.left_pub.publish(msg_left)
        self.right_pub.publish(msg_right)

def main(args=None):
    rclpy.init(args=args)
    node = MyNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
