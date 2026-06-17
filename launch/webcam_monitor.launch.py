import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    package_share_dir = get_package_share_directory("robot_monitor_poc")

    params_file = os.path.join(
        package_share_dir,
        "config",
        "monitor_params.yaml",
    )

    webcam_camera_node = Node(
        package="robot_monitor_poc",
        executable="webcam_camera_node",
        name="webcam_camera_node",
        output="screen",
        parameters=[params_file],
    )

    webcam_vision_node = Node(
        package="robot_monitor_poc",
        executable="webcam_vision_node",
        name="webcam_vision_node",
        output="screen",
        parameters=[params_file],
    )

    dummy_llm_node = Node(
        package="robot_monitor_poc",
        executable="dummy_llm_node",
        name="dummy_llm_node",
        output="screen",
    )

    alert_node = Node(
        package="robot_monitor_poc",
        executable="alert_node",
        name="alert_node",
        output="screen",
    )

    return LaunchDescription([
        webcam_camera_node,
        webcam_vision_node,
        dummy_llm_node,
        alert_node,
    ])