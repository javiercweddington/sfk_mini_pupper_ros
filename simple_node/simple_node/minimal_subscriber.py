import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from example_interfaces.msg import String

class MinimalSubscrber(Node):

    def __init__(self):

        super().__init__("minimal_subscriber")

        self.subcription = self.create_subscription(
            String,
            "my_topic",
            self._listener_callback,
            10
        )

    def _listener_callback(self, msg):

        self.get_logger().info(f"Received Message: {msg.data}")

def main(args=None):

    try:
        rclpy.init()
        node = MinimalSubscrber()
        rclpy.spin(node)

    except (KeyboardInterrupt, ExternalShutdownException):
        pass

    finally:
        if node is not None:
            node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == "__main__":
    main()