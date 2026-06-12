import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2


class ImageDebugNode(Node):
    def __init__(self):
        super().__init__("image_debug_node")
        self.subscription_ = self.create_subscription(
            Image, "/camera/image_raw", self.image_callback, 10
        )
        self.bridge = CvBridge()
        self.get_logger().info("Image Debug Node has been started.")

    def image_callback(self, msg):
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
        height, width, channels = frame.shape
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        mean_brightness = gray.mean()

        self.get_logger().info(
            f"Received image: {width}x{height}, channels={channels}, mean brightness={mean_brightness:.2f}"
        )


def main(args=None):
    rclpy.init(args=args)
    image_debug_node = ImageDebugNode()
    rclpy.spin(image_debug_node)
    image_debug_node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
