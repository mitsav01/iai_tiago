import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare
import serial.tools.list_ports

def get_ports():
    # Find all ports with Robotiq/Espressif HWIDs, sorted for stability
    devs = sorted([p.device for p in serial.tools.list_ports.comports() if any(h in p.hwid for h in ["303A", "0403"])])
    return (devs[0] if len(devs) > 0 else "/dev/ttyACM0", 
            devs[1] if len(devs) > 1 else "/dev/ttyACM1")

def generate_launch_description():
    pkg_share = FindPackageShare("robotiq_description").find("robotiq_description")
    ctrl_file = os.path.join(os.path.dirname(__file__), "../config/dual_robotiq_controllers.yaml")
    dev_l, dev_r = get_ports()

    # Define arguments
    args = [
        DeclareLaunchArgument("model", default_value=os.path.join(pkg_share, "urdf", "robotiq_2f_140_gripper.urdf.xacro")),
        DeclareLaunchArgument("com_port_left", default_value=dev_l),
        DeclareLaunchArgument("com_port_right", default_value=dev_r),
    ]

    nodes = []
    # Create both gripper stacks in a single loop
    for side, port in [("left", "com_port_left"), ("right", "com_port_right")]:
        prefix = f"{side}_"
        
        desc = ParameterValue(Command([
            FindExecutable(name="xacro"), " ", LaunchConfiguration("model"),
            " use_fake_hardware:=false com_port:=", LaunchConfiguration(port), " prefix:=", prefix
        ]), value_type=str)

        # Main control and state nodes
        nodes.append(Node(package="controller_manager", executable="ros2_control_node", 
                          namespace=side, parameters=[{"robot_description": desc}, ctrl_file]))
        nodes.append(Node(package="robot_state_publisher", executable="robot_state_publisher", 
                          namespace=side, parameters=[{"robot_description": desc}]))

        # Spawn all three controllers for this side
        for ctrl in ["joint_state_broadcaster", "robotiq_activation_controller", "robotiq_gripper_controller"]:
            nodes.append(Node(package="controller_manager", executable="spawner",
                              arguments=[ctrl, "-c", f"/{side}/controller_manager"]))

    return LaunchDescription(args + nodes)