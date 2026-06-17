import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import json


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

        try:
            detection = json.loads(msg.data)
        except json.JSONDecodeError:
            self.get_logger().error(f"Failed to parse detection JSON: {msg.data}")
            return

        semantic_status = self.run_fake_reasoning(detection)

        status_msg = String()
        status_msg.data = json.dumps(semantic_status)

        self.publisher_.publish(status_msg)

        self.get_logger().info(f"Published semantic status: {status_msg.data}")

    def run_fake_reasoning(self, detection):
        object_name = detection.get("object", "unknown")
        brightness = detection.get("brightness", None)
        confidence = detection.get("confidence", None)

        if object_name == "dark_scene":
            return {
                "risk_level": "medium",
                "summary": (
                    f"The camera view is too dark for reliable monitoring. "
                    f"brightness={brightness}, confidence={confidence}"
                ),
                "action": "notify_operator",
            }

        if object_name == "normal_scene":
            return {
                "risk_level": "none",
                "summary": (
                    f"The camera view is normal. "
                    f"brightness={brightness}, confidence={confidence}"
                ),
                "action": "no_action",
            }

        if object_name == "person":
            return {
                "risk_level": "medium",
                "summary": "A person is detected near the robot.",
                "action": "notify_operator",
            }

        if object_name == "chair":
            return {
                "risk_level": "low",
                "summary": "A chair is detected in the scene.",
                "action": "no_action",
            }

        return {
            "risk_level": "none",
            "summary": "No relevant object detected.",
            "action": "no_action",
        }


def main(args=None):
    rclpy.init(args=args)
    dummy_llm_node = DummyLLMNode()
    rclpy.spin(dummy_llm_node)
    dummy_llm_node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
