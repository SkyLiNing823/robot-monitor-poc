import os
from glob import glob
from setuptools import setup

package_name = "robot_monitor_poc"

setup(
    name=package_name,
    version="0.0.0",
    packages=[package_name],
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        (os.path.join("share", package_name, "launch"), glob("launch/*.launch.py")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="skylining",
    maintainer_email="84125881+SkyLiNing823@users.noreply.github.com",
    description="TODO: Package description",
    license="TODO: License declaration",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "dummy_camera_node = robot_monitor_poc.dummy_camera_node:main",
            "dummy_vision_node = robot_monitor_poc.dummy_vision_node:main",
            "dummy_llm_node = robot_monitor_poc.dummy_llm_node:main",
            "alert_node = robot_monitor_poc.alert_node:main",
            "webcam_camera_node = robot_monitor_poc.webcam_camera_node:main",
            "image_debug_node = robot_monitor_poc.image_debug_node:main",
            "webcam_vision_node = robot_monitor_poc.webcam_vision_node:main",
        ],
    },
)
