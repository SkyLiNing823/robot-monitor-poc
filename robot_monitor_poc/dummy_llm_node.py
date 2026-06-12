import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class DummyLLMNode(Node):
    def __init__(self):
        super().__init__("dummy_llm_node")
        self.subscription_ = self.create_subscription(
            String, "/perception/detections", self.detection_callback, 10
        )
        self.publisher_ = self.create_publisher(String, "/robot/semantic_status", 10)
        self.get_logger().info("Dummy LLM Node has been started.")

    def detection_callback(self, msg):
        self.get_logger().info(f"Received detection: {msg.data}")
        semantic_msg = self.run_fake_reasoning(msg.data)
        status_msg = String()
        status_msg.data = semantic_msg
        self.publisher_.publish(status_msg)
        self.get_logger().info(f"Published semantic status: {status_msg.data}")

    def run_fake_reasoning(self, detection_result):
        if "object=dark_scene" in detection_result:
            return (
                "risk_level=medium; "
                "summary=The camera view is too dark for reliable monitoring; "
                "action=notify_operator"
            )

        if "object=normal_scene" in detection_result:
            return (
                "risk_level=none; "
                "summary=The camera view is normal; "
                "action=no_action"
            )

        if "object=person" in detection_result:
            return (
                "risk_level=medium; "
                "summary=A person is detected near the robot; "
                "action=notify_operator"
            )

        if "object=chair" in detection_result:
            return (
                "risk_level=low; "
                "summary=A chair is detected in the scene; "
                "action=no_action"
            )

        return (
            "risk_level=none; "
            "summary=No relevant object detected; "
            "action=no_action"
        )


def main(args=None):
    rclpy.init(args=args)
    dummy_llm_node = DummyLLMNode()
    rclpy.spin(dummy_llm_node)
    dummy_llm_node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
