import time
import math
import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
from robo_interfaces.action import Deslocamento

class DeslocamentoActionServer(Node):
    def __init__(self):
        super().__init__('robo_acao_servidor')
        self._action_server = ActionServer(
            self, Deslocamento, 'deslocamento', self.execute_callback)
        self.lat_atual = 0.0
        self.lon_atual = 0.0

    def execute_callback(self, goal_handle):
        self.get_logger().info('Iniciando deslocamento...')
        feedback_msg = Deslocamento.Feedback()
        dist_total = 0.0
        
        if (goal_handle.request.latitude_destino == self.lat_atual and 
            goal_handle.request.longitude_destino == self.lon_atual):
            goal_handle.abort()
            return Deslocamento.Result()

        for i in range(1, 10): # Simulação de tempo
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self.get_logger().info('Ação cancelada!')
                result = Deslocamento.Result()
                result.distancia_percorrida = dist_total
                return result

            passo_lat = goal_handle.request.velocidade_lat * 1.0
            passo_lon = goal_handle.request.velocidade_lon * 1.0
            self.lat_atual += passo_lat
            self.lon_atual += passo_lon
            dist_total += math.sqrt(passo_lat**2 + passo_lon**2)
            
            feedback_msg.latitude_atual = self.lat_atual
            feedback_msg.longitude_atual = self.lon_atual
            goal_handle.publish_feedback(feedback_msg)
            time.sleep(1.0)

        goal_handle.succeed()
        result = Deslocamento.Result()
        result.distancia_percorrida = dist_total
        return result

def main():
    rclpy.init()
    node = DeslocamentoActionServer()
    rclpy.spin(node)
    rclpy.shutdown()