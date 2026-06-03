#!/usr/bin/env python3

import os
import serial.tools.list_ports

from ament_index_python.packages import get_package_share_directory

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


def get_default_port():
    """
    Detect the first ESP32-S3 / FTDI device.
    Falls back to /dev/ttyACM0 if nothing is found.
    """
    for port in serial.tools.list_ports.comports():
        if any(vid in port.hwid for vid in ["303A", "0403"]):
            return port.device

    return "/dev/ttyACM0"


def generate_launch_description():

    description_pkg = get_package_share_directory("robotiq_description")

    default_model = os.path.join(
        description_pkg,
        "urdf",
        "robotiq_2f_140_gripper.urdf.xacro",
    )

    controller_config = PathJoinSubstitution(
        [
            FindPackageShare("iai_robotiq_gripper"),
            "config",
            "robotiq_controllers.yaml",
        ]
    )

    model_arg = DeclareLaunchArgument(
        "model",
        default_value=default_model,
        description="Path to robot xacro file",
    )

    com_port_arg = DeclareLaunchArgument(
        "com_port",
        default_value=get_default_port(),
        description="Serial port connected to Robotiq adapter",
    )

    tf_prefix_arg = DeclareLaunchArgument(
        "tf_prefix",
        default_value="",
        description="TF prefix for multi-robot setups",
    )

    robot_description = ParameterValue(
        Command(
            [
                FindExecutable(name="xacro"),
                " ",
                LaunchConfiguration("model"),
                " use_fake_hardware:=false",
                " com_port:=",
                LaunchConfiguration("com_port"),
                " prefix:=",
                LaunchConfiguration("tf_prefix"),
            ]
        ),
        value_type=str,
    )

    control_node = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[
            {"robot_description": robot_description},
            controller_config,
        ],
        output="screen",
    )

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[
            {"robot_description": robot_description},
        ],
        output="screen",
    )

    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "joint_state_broadcaster",
            "--controller-manager",
            "/controller_manager",
        ],
        output="screen",
    )

    robotiq_gripper_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "robotiq_gripper_controller",
            "--controller-manager",
            "/controller_manager",
        ],
        output="screen",
    )

    robotiq_activation_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "robotiq_activation_controller",
            "--controller-manager",
            "/controller_manager",
        ],
        output="screen",
    )

    return LaunchDescription(
        [
            model_arg,
            com_port_arg,
            tf_prefix_arg,
            control_node,
            robot_state_publisher,
            joint_state_broadcaster_spawner,
            robotiq_gripper_controller_spawner,
            robotiq_activation_controller_spawner,
        ]
    )