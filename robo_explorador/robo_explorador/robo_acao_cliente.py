import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from robo_interfaces.action import Deslocamento

class DeslocamentoActionClient(Node):
    def __init__(self):
        super().__init__('robo_acao_cliente')
        self._action_client = ActionClient(self, Deslocamento, 'deslocamento')

    def send_goal(self):
        goal_msg = Deslocamento.Goal()
        goal_msg.latitude_destino = 10.0
        goal_msg.longitude_destino = 20.0
        goal_msg.velocidade_lat = 1.0
        goal_msg.velocidade_lon = 2.0

        self._action_client.wait_for_server()
        self._send_goal_future = self._action_client.send_goal_async(goal_msg)
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            return
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'Distância total percorrida: {result.distancia_percorrida:.2f}')
        rclpy.shutdown()

def main():
    rclpy.init()
    action_client = DeslocamentoActionClient()
    action_client.send_goal()
    rclpy.spin(action_client)