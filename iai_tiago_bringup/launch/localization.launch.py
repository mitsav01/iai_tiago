import launch
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument(
            'scan_topic', default_value='scan', description='Laser scan topic'
        ),
        DeclareLaunchArgument(
            'map_topic', default_value='map', description='Map topic'
        ),
        DeclareLaunchArgument(
            'amcl_params_file', default_value='$(find iai_tiago_bringup)/config/amcl.yaml',
            description='Full path to the AMCL parameters file'
        ),

        Node(
            package='amcl',
            executable='amcl',
            name='amcl',
            output='screen',
            parameters=[{
                'scan_topic': LaunchConfiguration('scan_topic'),
                'map_topic': LaunchConfiguration('map_topic')
            },LaunchConfiguration('amcl_params_file')],
            remappings=[
                ('/scan', LaunchConfiguration('scan_topic')),
                ('/map', LaunchConfiguration('map_topic'))
            ]
        )
    ])
