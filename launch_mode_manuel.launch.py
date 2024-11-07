from launch import LaunchDescription
from launch_ros.actions import Node

def generate_lauch_description():
    return Launchdescription([
    Node(package='ModeManuel', executable='ModeManuel', name='manuel')
    ])
