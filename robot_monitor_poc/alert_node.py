import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import json


class AlertNode(Node):
    def __init__(self):
        super().__init__("alert_node")

        self.subscription = self.create_subscription(
            String, "/robot/semantic_status", self.status_callback, 10
        )

        self.get_logger().info("Alert node started.")

    def status_callback(self, msg):
        self.get_logger().info(f"Received semantic status: {msg.data}")

        try:
            status = json.loads(msg.data)
        except json.JSONDecodeError:
            self.get_logger().error(f"Failed to parse semantic status JSON: {msg.data}")
            return

        action = status.get("action", "no_action")
        risk_level = status.get("risk_level", "unknown")
        summary = status.get("summary", "")

        if action == "notify_operator":
            self.get_logger().warn(
                f"[ALERT] risk_level={risk_level}; summary={summary}; action={action}"
            )
        else:
            self.get_logger().info(
                f"[NORMAL] risk_level={risk_level}; summary={summary}; action={action}"
            )


def main(args=None):
    rclpy.init(args=args)
    alert_node = AlertNode()
    rclpy.spin(alert_node)
    alert_node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
