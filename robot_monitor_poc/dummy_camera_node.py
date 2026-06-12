import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class DummyCameraNode(Node):
    def __init__(self):
        super().__init__("dummy_camera_node")
        self.publisher_ = self.create_publisher(String, "/camera/fake_frame", 10)
        self.frame_count = 0
        self.timer = self.create_timer(1.0, self.publish_fake_frame)
        self.get_logger().info("Dummy Camera Node has been started.")

    def publish_fake_frame(self):
        msg = String()
        msg.data = f"frame_{self.frame_count}"
        self.publisher_.publish(msg)
        self.get_logger().info(f"Published: {msg.data}")
        self.frame_count += 1


def main(args=None):
    rclpy.init(args=args)
    dummy_camera_node = DummyCameraNode()
    rclpy.spin(dummy_camera_node)
    dummy_camera_node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
