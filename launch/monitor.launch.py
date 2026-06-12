from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    webcam_camera_node = Node(
        package="robot_monitor_poc",
        executable="webcam_camera_node",
        name="webcam_camera_node",
        output="screen",
    )

    webcam_vision_node = Node(
        package="robot_monitor_poc",
        executable="webcam_vision_node",
        name="webcam_vision_node",
        output="screen",
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