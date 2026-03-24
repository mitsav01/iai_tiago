import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare
import serial.tools.list_ports

def get_default_port():
    """Finds the first Robotiq/Espressif device or defaults to ACM0."""
    devs = [p.device for p in serial.tools.list_ports.comports() if any(h in p.hwid for h in ["303A", "0403"])]
    return devs[2] if devs else "/dev/ttyACM0"

def generate_launch_description():
    pkg_share = FindPackageShare("robotiq_description").find("robotiq_description")
    ctrl_yaml = os.path.join(os.path.dirname(__file__), "../config/robotiq_controllers.yaml")

    # --- Arguments ---
    args = [
        DeclareLaunchArgument("model", default_value=os.path.join(pkg_share, "urdf", "robotiq_2f_140_gripper.urdf.xacro")),
        DeclareLaunchArgument("com_port", default_value=get_default_port()),
        DeclareLaunchArgument("tf_prefix", default_value="")
    ]

    # --- Robot Description ---
    robot_desc = ParameterValue(Command([
        FindExecutable(name="xacro"), " ", LaunchConfiguration("model"),
        " use_fake_hardware:=false com_port:=", LaunchConfiguration("com_port"),
        " prefix:=", LaunchConfiguration("tf_prefix")
    ]), value_type=str)

    # --- Core Nodes ---
    nodes = [
        Node(package="controller_manager", executable="ros2_control_node", 
             parameters=[{"robot_description": robot_desc}, ctrl_yaml], output="screen"),
        Node(package="robot_state_publisher", executable="robot_state_publisher", 
             parameters=[{"robot_description": robot_desc}], output="screen")
    ]

    # --- Controller Spawners (Compact Loop) ---
    controllers = ["joint_state_broadcaster", "robotiq_gripper_controller", "robotiq_activation_controller"]
    for ctrl in controllers:
        nodes.append(Node(package="controller_manager", executable="spawner", arguments=[ctrl]))

    return LaunchDescription(args + nodes)