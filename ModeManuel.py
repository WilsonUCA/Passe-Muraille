import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy


class ModeManuel(Node):



    def __init__(self):
        super().__init__('modemanuel')
        #TEMPORAIRE, calcul nécessaire avec les infos de joy
        self.velX = 0.0
        self.rotZ = 0.0

        
####################### Publisher #######################
        
        # Création du topic blabla
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        # Création d'un timer
        timer_period = 0.1
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0
        
#######################  Subscriber #######################
        
        # souscription au topic blabla, appelle la fonction listener_callback a chaque message recu
        self.subscription = self.create_subscription(Joy,'joy',self.calcul_vitesse, 10) #remplacer lister_callback par calcul_vitesse
        #self.subscription

####################### Fonction #######################

    def calcul_vitesse(self, msg):
        self.multiplicateur_lineaire = 0.3
        self.multiplicateur_angulaire = 2.0
        self.rotZ = self.multiplicateur_angulaire * msg.axes[0]
        self.velX = self.multiplicateur_lineaire * msg.axes[1]

        self.get_logger().info('j ai recu : Up/Down: "%.2f"' % msg.axes[0])
        self.get_logger().info('j ai recu : Left/Right: "%.2f"' % msg.axes[1])
        self.get_logger().info('je calcul velX : "%.2f"' % self.velX)
        self.get_logger().info('je calcul rotZ : "%.2f"' % self.rotZ)
        
        
    def timer_callback(self):
        # création d'un message de type twist
        msg = Twist()
        
        msg.linear.x = self.velX
        msg.linear.y = 0.0
        msg.linear.z = 0.0
        
        msg.angular.x = 0.0
        msg.angular.y = 0.0
        msg.angular.z = self.rotZ
        
        # Publication et affichage du message sur le terminal
        self.publisher_.publish(msg)
        self.get_logger().info('je envoie: Linear velocity x: %.2f, angular_z=%.2f' % (msg.linear.x, msg.angular.z))
       
# Fonction principale
def main(args=None):

    rclpy.init(args=args)   # Init
    
    modeManuel = ModeManuel() # Creation d'une instance de classe
    
    rclpy.spin(modeManuel)     # attente de destruction ou arret de l'instance
    
    modeManuel.destroy_node()  # Destruction de l'instance
    
    rclpy.shutdown()    # Fin du noeud
    
if __name__ == '__main__':
    main()
