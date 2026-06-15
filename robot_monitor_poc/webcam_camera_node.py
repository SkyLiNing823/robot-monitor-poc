import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2


class WebcamCameraNode(Node):
    def __init__(self):
        super().__init__("webcam_camera_node")
        self.declare_parameter("camera_index", 0)
        self.declare_parameter("fps", 10.0)
        self.camera_index = self.get_parameter("camera_index").value
        self.fps = self.get_parameter("fps").value
        self.publisher_ = self.create_publisher(Image, "/camera/image_raw", 10)
        self.bridge = CvBridge()
        self.cap = cv2.VideoCapture(self.camera_index)  # Open the specified webcam

        if not self.cap.isOpened():
            self.get_logger().error(
                f"Could not open webcam with camera_index={self.camera_index}."
            )
            raise RuntimeError("Failed to open webcam.")

        timer_period = 1.0 / self.fps
        self.timer = self.create_timer(timer_period, self.publish_frame)
        self.get_logger().info("Webcam Camera Node has been started.")

    def publish_frame(self):
        ret, frame = self.cap.read()

        if not ret:
            self.get_logger().warn("Failed to capture frame from webcam.")
            return

        msg = self.bridge.cv2_to_imgmsg(frame, encoding="bgr8")
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = "webcam"
        self.publisher_.publish(msg)

    def destroy_node(self):
        if hasattr(self, "cap"):
            self.cap.release()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    webcam_camera_node = WebcamCameraNode()
    rclpy.spin(webcam_camera_node)
    webcam_camera_node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
