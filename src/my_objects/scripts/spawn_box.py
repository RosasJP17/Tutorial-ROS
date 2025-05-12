#!/usr/bin/env python3

import rospy
from gazebo_msgs.srv import SpawnModel
from geometry_msgs.msg import Pose
from tf.transformations import quaternion_from_euler
import os

def spawn_box():
    rospy.init_node("spawn_box_node")

    urdf_path = os.path.join(
        os.path.expanduser("~"),
        "test2_ws/src/my_objects/urdf/caja.urdf"
    )

    with open(urdf_path, "r") as f:
        model_xml = f.read()

    rospy.wait_for_service("/gazebo/spawn_urdf_model")
    spawn_model = rospy.ServiceProxy("/gazebo/spawn_urdf_model", SpawnModel)

    pose = Pose()
    pose.position.x = -0.55
    pose.position.y = 0.0
    pose.position.z = 1.0

    # Rotación de 270 grados (3 * pi / 2 rad) alrededor del eje Z
    q = quaternion_from_euler(0, 0, 3 * 3.14159265 / 2)
    pose.orientation.x = q[0]
    pose.orientation.y = q[1]
    pose.orientation.z = q[2]
    pose.orientation.w = q[3]

    spawn_model("box_container", model_xml, "", pose, "world")
    rospy.loginfo("Spawned box_container with 270° rotation")

if __name__ == "__main__":
    spawn_box()
