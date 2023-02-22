from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='can_bus',
            namespace='send_can0',
            executable='send_can0',
            name='send_can0'
        ),
        Node(
            package='can_bus',
            namespace='recv_can0',
            executable='recv_can0',
            name='recv_can0'
        ),
        Node(
            package='can_bus',
            namespace='encoder_can0',
            executable='encoder_can0',
            name='encoder_can0'
        ),
        Node(
            package='motor_control',
            namespace='local_controller',
            executable='local_controller',
            name='local_controller'
        ),
        Node(
            package='joy',
            executable='joy_node',
            name='joy_node'
        )
    ])