from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='cam_depth',
            executable='est_depth',
            name='est_depth',
        ),
    ])