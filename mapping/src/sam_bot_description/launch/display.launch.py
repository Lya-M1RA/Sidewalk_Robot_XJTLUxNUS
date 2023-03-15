import launch
from launch.substitutions import Command, LaunchConfiguration
import launch_ros
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import LifecycleNode
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument

import lifecycle_msgs.msg
import os
from glob import glob

def generate_launch_description():
    pkg_share = launch_ros.substitutions.FindPackageShare(package='sam_bot_description').find('sam_bot_description')
    default_model_path = os.path.join(pkg_share, 'src/description/sam_bot_description1.urdf')
    default_rviz_config_path = os.path.join(pkg_share, 'rviz/urdf_config.rviz')
    driver_dir = os.path.join(get_package_share_directory('lslidar_driver'), 'params', 'lidar_uart_ros2','lsm10_p.yaml')
    map_file = os.path.join(get_package_share_directory('sam_bot_description'), 'map', 'nusri2.yaml')
    #world_path=os.path.join(pkg_share, 'world/my_world.sdf')
    nav2_yaml = os.path.join(get_package_share_directory('sam_bot_description'), 'config', 'amcl_config.yaml')
   
    robot_state_publisher_node = launch_ros.actions.Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': Command(['xacro ', LaunchConfiguration('model')])}]
    )
    joint_state_publisher_node = launch_ros.actions.Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        #condition=launch.conditions.UnlessCondition(LaunchConfiguration('gui'))
    )
    rviz_node = launch_ros.actions.Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        #arguments=['-d', LaunchConfiguration('rvizconfig')],
    )
    lsliadar_node = LifecycleNode(
        package='lslidar_driver',
        executable='lslidar_driver_node',
        name='lslidar_driver_node',		
        output='screen',
        emulate_tty=True,
        namespace='',
        parameters=[driver_dir],
    )
    mapserver_node = launch_ros.actions.Node(
        package='nav2_map_server',
        executable='map_server',
        name='map_server',
        output='screen',
        parameters=[{'use_sim_time': False}, 
                    {'yaml_filename':map_file}]
    )
    amcl_node = launch_ros.actions.Node(
        package='nav2_amcl',
        executable='amcl',
        name='amcl',
        output='screen',
        parameters=[nav2_yaml]
    )
    lifecycle_node = launch_ros.actions.Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager_mapper',
        output='screen',
        parameters=[{'use_sim_time': False},
                    {'autostart': True},
                    {'node_names': ['map_server', 'amcl']}]  
    )
    '''
    spawn_entity = launch_ros.actions.Node(
    	package='gazebo_ros', 
    	executable='spawn_entity.py',
        arguments=['-entity', 'sam_bot', '-topic', 'robot_description'],
        output='screen'
    )
    '''
    robot_localization_node = launch_ros.actions.Node(
         package='robot_localization',
         executable='ekf_node',
         name='ekf_filter_node',
         output='screen',
         parameters=[os.path.join(pkg_share, 'config/ekf.yaml'), {'use_sim_time': False}]
    )
    odom_node = launch_ros.actions.Node(
        package='difftf_py',
        executable='diff_tf',
        name='diff_tf',
    )
    odom_trans = launch_ros.actions.Node(
        package='difftf_py',
        executable='odom_publisher',
        name='odom_publisher',
    )
    
    

    return launch.LaunchDescription([
        launch.actions.DeclareLaunchArgument(name='model', default_value=default_model_path,
                                            description='Absolute path to robot urdf file'),
        launch.actions.DeclareLaunchArgument(name='rvizconfig', default_value=default_rviz_config_path,
                                            description='Absolute path to rviz config file'),
        launch.actions.DeclareLaunchArgument(name='use_sim_time', default_value='False',
                                            description='Flag to enable use_sim_time'),
        #launch.actions.ExecuteProcess(cmd=['gazebo', '--verbose', '-s', 'libgazebo_ros_init.so', '-s', 'libgazebo_ros_factory.so', world_path], output='screen'),
        joint_state_publisher_node,
        robot_state_publisher_node,
        robot_localization_node,
        #spawn_entity,
        #rviz_node,
        lsliadar_node,
        #mapserver_node,
        #amcl_node,
        #lifecycle_node,
        odom_node,
        odom_trans,
    ])
