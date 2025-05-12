#!/usr/bin/env python3

import rospy
import rospkg
from gazebo_msgs.srv import SpawnModel
from geometry_msgs.msg import Pose

def spawn_cubo(nombre, x, y, z):
    rospy.wait_for_service('/gazebo/spawn_urdf_model')
    spawn_model = rospy.ServiceProxy('/gazebo/spawn_urdf_model', SpawnModel)

    rospack = rospkg.RosPack()
    urdf_path = rospack.get_path('ur5_v1') + '/urdf/cubo.urdf'

    with open(urdf_path, 'r') as f:
        cubo_urdf = f.read()

    pose = Pose()
    pose.position.x = x
    pose.position.y = y
    pose.position.z = z + 0.02  # centro del cubo
    pose.orientation.w = 1.0

    spawn_model(nombre, cubo_urdf, '', pose, 'world')

if __name__ == "__main__":
    rospy.init_node("spawn_cubes_gazebo")
    spawn_cubo("cubo_1", 0.4,  0.0, 0.0)
    spawn_cubo("cubo_2", 0.4,  0.1, 0.0)
    spawn_cubo("cubo_3", 0.4, -0.1, 0.0)
    rospy.loginfo("Cubos spawneados en Gazebo.")
