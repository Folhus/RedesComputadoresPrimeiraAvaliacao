import rclpy
from rclpy.node import Node
from robo_interfaces.msg import Monitoramento

class EstacaoBaseSubscriber(Node):
    def __init__(self):
        super().__init__('robo_topico_subscriber')
        self.subscription = self.create_subscription(
            Monitoramento, 'monitoramento', self.listener_callback, 10)

    def listener_callback(self, msg):
        if 10 <= msg.temperatura <= 40 and msg.oxigenio > 80:
            status = "Safe"
        else:
            status = "Not Safe"
        self.get_logger().info(f'Recebido - O2: {msg.oxigenio:.2f}, Temp: {msg.temperatura:.2f} -> {status}')

def main():
    rclpy.init()
    node = EstacaoBaseSubscriber()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()