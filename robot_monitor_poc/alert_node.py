import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class AlertNode(Node):
    def __init__(self):
        super().__init__("alert_node")

        self.subscription = self.create_subscription(
            String, "/robot/semantic_status", self.status_callback, 10
        )

        self.get_logger().info("Alert node started.")

    def status_callback(self, msg):
        self.get_logger().info(f"Received semantic status: {msg.data}")

        if "action=notify_operator" in msg.data:
            self.get_logger().warn(f"[ALERT] {msg.data}")
        else:
            self.get_logger().info(f"[NORMAL] {msg.data}")


def main(args=None):
    rclpy.init(args=args)
    alert_node = AlertNode()
    rclpy.spin(alert_node)
    alert_node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
