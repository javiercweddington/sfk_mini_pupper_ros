import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from example_interfaces.msg import String

class MinimalPublisher(Node):

    def __init__(self):

        super().__init__("minimal_publisher")

        self._publisher = self.create_publisher(String, "my_topic", 10)

        self._timer = self.create_timer(0.5, self._timer_callback)

        self._counter = 0

    def _timer_callback(self):

        msg = String()
        msg.data = f"Hello world: {self._counter}"
        
        self._publisher.publish(msg)
        self.get_logger().info(f"Publishing: {msg.data}")

        self._counter += 1

def main(args=None):

    try:
        rclpy.init()
        node = MinimalPublisher()
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