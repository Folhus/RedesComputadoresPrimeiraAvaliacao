import rclpy
from rclpy.node import Node
from robo_interfaces.srv import ColetaMaterial
import random

class ColetaServidor(Node):
    def __init__(self):
        super().__init__('robo_coleta_servidor')
        self.srv = self.create_service(ColetaMaterial, 'coleta_material', self.coleta_callback)

    def coleta_callback(self, request, response):
        probabilidade = random.random()
        response.sucesso = probabilidade <= 0.7  # 70% de chance de sucesso
        self.get_logger().info(f'Req Profundidade: {request.profundidade:.2f} | Sucesso: {response.sucesso}')
        return response

def main():
    rclpy.init()
    node = ColetaServidor()
    rclpy.spin(node)
    rclpy.shutdown()