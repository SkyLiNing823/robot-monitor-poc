# ROS 2 Robot Monitor PoC

A ROS 2 mini project for simulating a robot monitoring pipeline:

- Webcam camera node publishes image frames
- Vision node processes images with OpenCV
- LLM-style reasoning node generates semantic status
- Alert node prints normal/alert messages

## Pipeline

```
webcam_camera_node
  -> /camera/image_raw
webcam_vision_node
  -> /perception/detections
dummy_llm_node
  -> /robot/semantic_status
alert_node
```

## Run 

```
cd ~/ros2_ws
colcon build --packages-select robot_monitor_poc
source install/setup.zsh
ros2 launch robot_monitor_poc webcam_monitor.launch.py
```

