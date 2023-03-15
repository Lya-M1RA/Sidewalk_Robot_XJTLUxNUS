from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='can_bus',
            executable='send_can0',
            name='send_can0'
        ),
        Node(
            package='can_bus',
            executable='recv_can0',
            name='recv_can0'
        ),
        Node(
            package='can_bus',
            executable='encoder_can0',
            name='encoder_can0'
        ),
        Node(
            package='motor_control',
            executable='upper_controller',
            name='upper_controller'
        ),
        Node(
            package='joy',
            executable='joy_node',
            name='joy_node',
            parameters=[{'deadzone': 0.2}]
        ),
        Node(
            package='motor_control',
            executable='encoder_counter_l',
            name='encoder_counter_l'
        ),
        Node(
            package='motor_control',
            executable='encoder_counter_r',
            name='encoder_counter_r'
        )
    ])