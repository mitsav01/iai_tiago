import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument,LogInfo
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch_ros.descriptions import ParameterValue
def generate_launch_description():

    tiago_xacro_file = os.path.join(get_package_share_directory('iai_tiago_description'), 'urdf',
                                     'tiago_from_our_robot.urdf')
    robot_description = Command(
        [FindExecutable(name='xacro'), ' ', tiago_xacro_file])

    rviz_file = os.path.join(get_package_share_directory('iai_tiago_description'), 'rviz2',
                              'default.rviz')
    
    collision_parameter_file = PathJoinSubstitution([FindPackageShare('tiago_dual_description'),'config','collision','collision_parameters.yaml'])
    return LaunchDescription([
        # Robot description parameter
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{
                'robot_description': ParameterValue(robot_description,value_type=str)}]
        ),
        
        # # Load collision parameters from YAML file
        # Node(
        #     package='tiago_dual_description',
        #     executable='collision_parameters_loader',
        #     name='collision_parameters_loader',
        #     output='screen',
        #     parameters=[{
        #         'collision_parameters': collision_parameter_file}]
        # ),

        # Joint state publisher GUI
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui',
            output='screen'
        ),
        
        Node(package='rviz2',executable='rviz2',name='rviz2',arguments=['--display-config',rviz_file]),
        
        # Additional useful log message to confirm launch
        LogInfo(
            msg="Robot description and parameters have been loaded successfully!"
        )
    ])
