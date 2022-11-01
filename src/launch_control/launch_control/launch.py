from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='can_bus',
            executable='can0_tx'
        ),
        Node(
            package='joy',
            executable='joy_node'
        ),
        Node(
            package='motor_control',
            executable='local_controller'
        ),
    ])