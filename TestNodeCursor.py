#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
class BasicPublisher(Node):
    def __init__(self):
        super().__init__('basic_publisher')
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

        self.sub = self.create_subscription(LaserScan, 'Scan', self.callback, 10)

    def callback(self, msg):
        self.get_logger().info(f'Received: {msg.ranges}')
        self.ranges = msg.ranges

    def timer_callback(self):
        self.security_check()
        self.i += 1

    def security_check(self):
        # Vérifier si des données laser sont disponibles
        self.get_logger().info('Running security check')
        if hasattr(self, 'ranges'):
            # Vérifier les obstacles dans un angle frontal (indices centraux)
            centre = len(self.ranges) // 2
            angle_check = 10  # Nombre de points à vérifier de chaque côté
            zone_frontale = self.ranges[centre-angle_check:centre+angle_check]
            
            # Vérifier si un obstacle est détecté à moins de 0.5m
            if min(zone_frontale) < 0.5:
                # Désactiver les mouvements linéaires
                msg = Twist()
                msg.linear.x = 0.0
                self.publisher_.publish(msg)
                self.get_logger().warn('Obstacle détecté! Arrêt des mouvements linéaires')
                return True
            
            # Vérifier si un obstacle est détecté à moins de 0.3m
            if min(zone_frontale) < 0.3:
                # Faire reculer le robot à une vitesse de -0.2
                msg = Twist()
                msg.linear.x = -0.2
                self.publisher_.publish(msg)
                self.get_logger().warn('Obstacle très proche! Recul à une vitesse de -0.2')
                return True
        return False

def main(args=None):
    rclpy.init(args=args)
    
    basic_publisher = BasicPublisher()
    
    try:
        rclpy.spin(basic_publisher)
    except KeyboardInterrupt:
        pass
    finally:
        basic_publisher.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
