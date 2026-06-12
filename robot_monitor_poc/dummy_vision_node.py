import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class DummyVisionNode(Node):
    def __init__(self):
        super().__init__("dummy_vision_node")
        self.subscription_ = self.create_subscription(
            String, "/camera/fake_frame", self.frame_callback, 10
        )
        self.publisher_ = self.create_publisher(String, "/perception/detections", 10)
        self.get_logger().info("Dummy Vision Node has been started.")

    def frame_callback(self, msg):
        self.get_logger().info(f"Received: {msg.data}")
        detection_msg = String()
        if int(msg.data.split("_")[-1]) % 3 == 0:
            detection_msg.data = "object=person; confidence=0.92"
        elif int(msg.data.split("_")[-1]) % 3 == 1:
            detection_msg.data = "object=chair; confidence=0.81"
        else:
            detection_msg.data = "object=none; confidence=0.00"

        self.publisher_.publish(detection_msg)

        self.get_logger().info(f"Published detection: {detection_msg.data}")


def main(args=None):
    rclpy.init(args=args)
    dummy_vision_node = DummyVisionNode()
    rclpy.spin(dummy_vision_node)
    dummy_vision_node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
