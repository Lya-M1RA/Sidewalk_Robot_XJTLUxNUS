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
    map_file = os.path.join(get_package_share_directory('sam_bot_description'), 'map', 'EBEEL3edited.yaml')
    #world_path=os.path.join(pkg_share, 'world/my_world.sdf')

    nav2_yaml = os.path.join(get_package_share_directory('sam_bot_description'), 'config', 'amcl_config.yaml')
    controller_yaml = os.path.join(get_package_share_directory('sam_bot_description'), 'config', 'controller.yaml')
    bt_navigator_yaml = os.path.join(get_package_share_directory('sam_bot_description'), 'config', 'bt_navigator.yaml')
    planner_yaml = os.path.join(get_package_share_directory('sam_bot_description'), 'config', 'planner_server.yaml')
    recovery_yaml = os.path.join(get_package_share_directory('sam_bot_description'), 'config', 'recovery.yaml')
    filters_yaml = os.path.join(get_package_share_directory('sam_bot_description'), 'config', 'filters.yaml')

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
    controller_node = launch_ros.actions.Node(
        package='nav2_controller',
        executable='controller_server',
        name='controller_server',
        output='screen',
        parameters=[controller_yaml]
    )
    planner_node = launch_ros.actions.Node(
        package='nav2_planner',
        executable='planner_server',
        name='planner_server',
        output='screen',
        parameters=[planner_yaml]
    )
    behavior_node = launch_ros.actions.Node(
        package='nav2_behaviors',
        executable='behavior_server',
        name='behavior_server',
        parameters=[recovery_yaml],
        output='screen'
    )
    bt_node = launch_ros.actions.Node(
        package='nav2_bt_navigator',
        executable='bt_navigator',
        name='bt_navigator',
        output='screen',
        parameters=[bt_navigator_yaml]
    )
    filter_node = launch_ros.actions.Node(
            package='nav2_map_server',
            executable='map_server',
            name='filter_mask_server',
            output='screen',
            emulate_tty=True,
            parameters=[filters_yaml]
    )

    costmapfilter_node = launch_ros.actions.Node(
            package='nav2_map_server',
            executable='costmap_filter_info_server',
            name='costmap_filter_info_server',
            output='screen',
            emulate_tty=True,
            parameters=[filters_yaml]
    )
    lifecycle_node = launch_ros.actions.Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager_mapper',
        output='screen',
        parameters=[{'use_sim_time': False},
                    {'autostart': True},
                    {'node_names': ['map_server', 
                                    'amcl','controller_server',
                                    'planner_server',
                                    'behavior_server','bt_navigator',
                                    'filter_mask_server',
                                    'costmap_filter_info_server'
                                    ]}])
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
    twist_motor = launch_ros.actions.Node(
        package='difftf_py',
        executable='robotvtowheelv',
        name='robotvtowheelv',
    )
    imu_init = launch_ros.actions.Node(
        package='imu',
        executable='imu_node',
        name='imu_node',
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
        rviz_node,
        lsliadar_node,
        mapserver_node,
        amcl_node,
        planner_node,
        behavior_node,
        controller_node,
        bt_node,
        odom_node,
        odom_trans,
        imu_init,
        twist_motor,
        costmapfilter_node,
        filter_node,
        lifecycle_node,
    ])
