import sys
import rclpy
from rclpy.node import Node
from robo_interfaces.srv import ColetaMaterial
import random

class ColetaClienteAsync(Node):
    def __init__(self):
        super().__init__('robo_coleta_cliente')
        self.cli = self.create_client(ColetaMaterial, 'coleta_material')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Serviço indisponível, aguardando...')
        self.req = ColetaMaterial.Request()

    def send_request(self):
        self.req.profundidade = random.uniform(0.1, 0.5)
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()

def main():
    rclpy.init()
    cliente = ColetaClienteAsync()
    response = cliente.send_request()
    if response.sucesso:
        cliente.get_logger().info('A coleta foi bem sucedida!')
    else:
        cliente.get_logger().info('A coleta falhou.')
    cliente.destroy_node()
    rclpy.shutdown()