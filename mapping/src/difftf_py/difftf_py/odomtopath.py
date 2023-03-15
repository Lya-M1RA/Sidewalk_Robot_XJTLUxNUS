import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry, Path
from geometry_msgs.msg import PoseStamped

class OdomToPath(Node):
    def __init__(self):
        super().__init__('odom_to_path')
        self.subscription = self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            10)
        self.publisher = self.create_publisher(Path, '/path', 10)
        self.path = Path()

    def odom_callback(self, msg):
        pose_stamped = PoseStamped()
        pose_stamped.pose = msg.pose.pose
        pose_stamped.header.frame_id = "odom"
        self.path.poses.append(pose_stamped)
        self.path.header.frame_id = "odom"
        self.publisher.publish(self.path)

def main(args=None):
    rclpy.init(args=args)

    odom_to_path = OdomToPath()

    rclpy.spin(odom_to_path)

    odom_to_path.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
