from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='cam_depth',
            executable='est_depth',
            name='est_depth',
        ),
        Node(
            package='usb_cam',
            executable='usb_cam_node_exe',
            name='usb_cam_node_exe',
            parameters=[
                {'video_device' : '/dev/video4'},
                {'image_width'  : 1280 },
                {'image_height' : 720},
                {'framerate'    : 60.0}
            ]
        )
    ])