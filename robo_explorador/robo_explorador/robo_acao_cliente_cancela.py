import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from robo_interfaces.action import Deslocamento

class ClienteAcaoCancela(Node):
    def __init__(self):
        super().__init__('robo_acao_cliente_cancela')
        self._action_client = ActionClient(self, Deslocamento, 'deslocamento')
        self._timer = None

    def send_goal(self):
        goal_msg = Deslocamento.Goal()
        goal_msg.latitude_destino = 50.0
        goal_msg.longitude_destino = 50.0
        goal_msg.velocidade_lat = 2.0
        goal_msg.velocidade_lon = 2.0

        self.get_logger().info('A aguardar pelo servidor de ação...')
        self._action_client.wait_for_server()
        
        self.get_logger().info('A enviar a meta para o robô...')
        self._send_goal_future = self._action_client.send_goal_async(goal_msg)
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        self.goal_handle = future.result()
        if not self.goal_handle.accepted:
            self.get_logger().info('Ação rejeitada pelo servidor.')
            return

        self.get_logger().info('Ação aceite pelo servidor. A iniciar o temporizador de 5 segundos para cancelamento...')
        
        self._get_result_future = self.goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)
        
        self._timer = self.create_timer(5.0, self.cancelar_acao)

    def cancelar_acao(self):
        self.get_logger().info('A solicitar o cancelamento da ação após 5 segundos...')
        self._timer.cancel()
        self._cancel_future = self.goal_handle.cancel_goal_async()

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'Ação finalizada/cancelada. Distância percorrida apresentada: {result.distancia_percorrida:.2f}')
        rclpy.shutdown()

def main(args=None):
    rclpy.init(args=args)
    action_client = ClienteAcaoCancela()
    action_client.send_goal()
    rclpy.spin(action_client)

if __name__ == '__main__':
    main()