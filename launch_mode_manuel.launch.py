from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_Description():
    return LaunchDescription([
    Node(package='ModeManuel', executable='ModeManuel', name='manuel')
    ])
