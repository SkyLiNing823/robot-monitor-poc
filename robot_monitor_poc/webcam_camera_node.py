import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class WebcamCameraNode(Node):
    def __init__(self):
        super().__init__("webcam_camera_node")
        self.publisher_ = self.create_publisher(Image, "/camera/image_raw", 10)
        self.bridge = CvBridge()
        self.cap = cv2.VideoCapture(0)  # Open the default webcam

        if not self.cap.isOpened():
            self.get_logger().error("Could not open webcam.")
            raise RuntimeError("Failed to open webcam.")
        
    
        self.timer = self.create_timer(0.1, self.publish_frame)
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
        
        self.get_logger().info(
            f"Published image frame: {frame.shape[1]}x{frame.shape[0]}"
        )
    
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

