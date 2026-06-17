import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge
import cv2
import json


class WebcamVisionNode(Node):
    def __init__(self):
        super().__init__("webcam_vision_node")
        self.declare_parameter("brightness_threshold", 30.0)

        self.brightness_threshold = self.get_parameter("brightness_threshold").value
        self.subscription_ = self.create_subscription(
            Image, "/camera/image_raw", self.image_callback, 10
        )
        self.publisher_ = self.create_publisher(String, "/perception/detections", 10)
        self.bridge = CvBridge()
        self.get_logger().info("Webcam Vision Node has been started.")

    def image_callback(self, msg):
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
        detection_result = self.run_brightness_detection(frame)
        detection_msg = String()
        detection_msg.data = detection_result
        self.publisher_.publish(detection_msg)
        self.get_logger().info(f"Published detection: {detection_msg.data}")

    def run_brightness_detection(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        mean_brightness = float(gray.mean())

        if mean_brightness < self.brightness_threshold:
            result = {
                "object": "dark_scene",
                "confidence": 0.95,
                "brightness": round(mean_brightness, 2),
                "threshold": float(self.brightness_threshold),
            }
        else:
            result = {
                "object": "normal_scene",
                "confidence": 0.80,
                "brightness": round(mean_brightness, 2),
                "threshold": float(self.brightness_threshold),
            }

        return json.dumps(result)


def main(args=None):
    rclpy.init(args=args)
    webcam_vision_node = WebcamVisionNode()
    rclpy.spin(webcam_vision_node)
    webcam_vision_node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
