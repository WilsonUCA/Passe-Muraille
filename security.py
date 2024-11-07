import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
from sensor_msgs.msg import LaserScan

class Security(Node):

    def __init__(self):
        super().__init__('modemanuel')

        # initialisation des variables
        self.velX = 0.0
        self.rotZ = 0.0
        self.velX_Brut = 0.0
        self.rotZ_Brut = 0.0
        
####################### Publisher #######################
        
        # Création du topic blabla
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        # Création d'un timer
        timer_period = 0.1
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0
        
#######################  Subscriber #######################
        
        # souscription au topic blabla, appelle la fonction listener_callback a chaque message recu
        self.subscription = self.create_subscription(Twist,'cmd_brut',self.set_cmd_brut, 10)
        self.subscription = self.create_subscription(LaserScan,'Scan',self.evaluate_range, 10)
        #self.subscription

####################### Fonction #######################

    def evaluate_range(self, msg):
        self.Lidar = msg
        
    def set_cmd_brut(self, msg):
        self.velX_Brut = msg.linear.x
        self.rotZ_Brut = msg.angular.z
        
        
    def timer_callback(self):
        msg = Twist()
        #recuperer les données de range dans un cône de 20° devant le robot
        centre = ( self.Lidar.angle_max - self.Lidar.angle_min ) / 2
        range_cone = self.Lidar.ranges[int(centre)-10:int(centre)+10]

        if min(range_cone) > 0.5:
            self.velX = self.velX_Brut
        elif min(range_cone) > 0.3:
            self.velX = 0.0
        else:
            self.velX = -0.2
        
        msg.linear.x = self.velX
        msg.angular.z = self.rotZ_Brut
        # Publication et affichage du message sur le terminal
        self.publisher_.publish(msg)
        self.get_logger().info('Obstacle le plus proche : %.2f' % min(range_cone))
       
####################### Fonction principale #######################
def main(args=None):

    rclpy.init(args=args)   # Init
    
    security = Security() # Creation d'une instance de classe
    
    rclpy.spin(security)     # attente de destruction ou arret de l'instance
    
    security.destroy_node()  # Destruction de l'instance
    
    rclpy.shutdown()    # Fin du noeud
    
if __name__ == '__main__':
    main()
