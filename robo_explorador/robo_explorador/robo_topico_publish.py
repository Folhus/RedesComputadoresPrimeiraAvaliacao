import rclpy
from rclpy.node import Node
from robo_interfaces.msg import Monitoramento
import random

class RoboPublisher(Node):
    def __init__(self):
        super().__init__('robo_topico_publish')
        self.publisher_ = self.create_publisher(Monitoramento, 'monitoramento', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)

    def timer_callback(self):
        msg = Monitoramento()
        msg.oxigenio = random.uniform(1.0, 100.0)
        msg.temperatura = random.uniform(1.0, 100.0)
        self.get_logger().info(f'Publicando - O2: {msg.oxigenio:.2f}, Temp: {msg.temperatura:.2f}')
        self.publisher_.publish(msg)

def main():
    rclpy.init()
    node = RoboPublisher()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()