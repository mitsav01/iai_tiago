#!/usr/bin/env python3

import os
import serial.tools.list_ports

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import (
    Command,
    FindExecutable,
    LaunchConfiguration,
    PathJoinSubstitution,
)
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare

from ament_index_python.packages import get_package_share_directory


def get_ports():
    """
    Detect two Robotiq adapters.

    ESP32-S3 VID:PID contains 303A
    FTDI adapters often contain 0403

    Falls back to ACM0/ACM1 if detection fails.
    """
    devices = sorted(
        [
            port.device
            for port in serial.tools.list_ports.comports()
            if any(hwid in port.hwid for hwid in ["303A", "0403"])
        ]
    )

    left_port = devices[0] if len(devices) > 0 else "/dev/ttyACM0"
    right_port = devices[1] if len(devices) > 1 else "/dev/ttyACM1"

    return left_port, right_port


def generate_launch_description():

    description_pkg = get_package_share_directory(
        "robotiq_description"
    )

    default_model = os.path.join(
        description_pkg,
        "urdf",
        "robotiq_2f_140_gripper.urdf.xacro",
    )

    controller_config = PathJoinSubstitution(
        [
            FindPackageShare("iai_robotiq_gripper"),
            "config",
            "dual_robotiq_controllers.yaml",
        ]
    )

    left_port, right_port = get_ports()

    launch_args = [
        DeclareLaunchArgument(
            "model",
            default_value=default_model,
            description="Path to Robotiq xacro file",
        ),
        DeclareLaunchArgument(
            "com_port_left",
            default_value=left_port,
            description="Left gripper serial port",
        ),
        DeclareLaunchArgument(
            "com_port_right",
            default_value=right_port,
            description="Right gripper serial port",
        ),
    ]

    nodes = []

    grippers = [
        ("left", "com_port_left"),
        ("right", "com_port_right"),
    ]

    for side, port_arg in grippers:

        prefix = f"{side}_"

        robot_description = ParameterValue(
            Command(
                [
                    FindExecutable(name="xacro"),
                    " ",
                    LaunchConfiguration("model"),
                    " use_fake_hardware:=false",
                    " com_port:=",
                    LaunchConfiguration(port_arg),
                    " prefix:=",
                    prefix,
                ]
            ),
            value_type=str,
        )

        nodes.append(
            Node(
                package="controller_manager",
                executable="ros2_control_node",
                namespace=side,
                parameters=[
                    {"robot_description": robot_description},
                    controller_config,
                ],
                output="screen",
            )
        )

        nodes.append(
            Node(
                package="robot_state_publisher",
                executable="robot_state_publisher",
                namespace=side,
                parameters=[
                    {"robot_description": robot_description},
                ],
                output="screen",
            )
        )

        controllers = [
            "joint_state_broadcaster",
            "robotiq_activation_controller",
            "robotiq_gripper_controller",
        ]

        for controller in controllers:
            nodes.append(
                Node(
                    package="controller_manager",
                    executable="spawner",
                    arguments=[
                        controller,
                        "--controller-manager",
                        f"/{side}/controller_manager",
                    ],
                    output="screen",
                )
            )

    return LaunchDescription(
        launch_args + nodes
    )