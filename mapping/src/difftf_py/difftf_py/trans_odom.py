import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from std_msgs.msg import Header
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3


class OdomPublisher(Node):
    def __init__(self):
        super().__init__("odom_publisher")
        self.publisher_ = self.create_publisher(Odometry, "/odom", 10)
        self.subscription_ = self.create_subscription(
            Odometry, "/odometry/filtered", self.odometry_callback, 10)

        self.timer_ = self.create_timer(1/200, self.timer_callback)

        self.odom_msg_ = Odometry()
        self.header_msg_ = Header()
        self.pose_msg_ = Pose()
        self.twist_msg_ = Twist()

    def odometry_callback(self, msg):
        self.header_msg_.frame_id = msg.header.frame_id
        self.header_msg_.stamp = msg.header.stamp
        self.odom_msg_.header = self.header_msg_
        self.odom_msg_.child_frame_id = msg.child_frame_id
        self.pose_msg_ = msg.pose.pose
        self.twist_msg_ = msg.twist.twist
        #self.get_logger().info(f'发布了转换{msg.pose.pose.position.x,msg.pose.pose.position.y}')  


    def timer_callback(self):
        self.odom_msg_.header.stamp = self.get_clock().now().to_msg()
        self.odom_msg_.pose.pose = self.pose_msg_
        self.odom_msg_.twist.twist = self.twist_msg_

        self.publisher_.publish(self.odom_msg_)
        #self.get_logger().info(f'发布了转换{self.odom_msg_.pose.pose.position.x,self.odom_msg_.pose.pose.position.y}')  


def main(args=None):
    rclpy.init(args=args)
    odom_publisher = OdomPublisher()
    rclpy.spin(odom_publisher)
    odom_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
