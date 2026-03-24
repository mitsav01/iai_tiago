import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # Use nav2_amcl for ROS 2 compatibility
    default_amcl_params = os.path.join(
        get_package_share_directory('iai_tiago_bringup'),
        'config', 'amcl.yaml'
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'scan_topic', default_value='scan', description='Laser scan topic'
        ),
        DeclareLaunchArgument(
            'map_topic', default_value='map', description='Map topic'
        ),
        DeclareLaunchArgument(
            'amcl_params_file', default_value=default_amcl_params,
            description='Full path to the AMCL parameters file'
        ),

        Node(
            package='nav2_amcl', # Updated package name
            executable='amcl',
            name='amcl',
            output='screen',
            parameters=[LaunchConfiguration('amcl_params_file')],
            remappings=[
                ('scan', LaunchConfiguration('scan_topic')),
                ('map', LaunchConfiguration('map_topic'))
            ]
        ),

        # AMCL requires a lifecycle manager to move to the 'active' state
        Node(
            package='nav2_lifecycle_manager',
            executable='lifecycle_manager',
            name='lifecycle_manager_localization',
            output='screen',
            parameters=[{'use_sim_time': True},
                        {'autostart': True},
                        {'node_names': ['amcl']}]
        )
    ])