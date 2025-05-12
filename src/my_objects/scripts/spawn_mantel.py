#!/usr/bin/env python3

import rospy
from gazebo_msgs.srv import SpawnModel
from geometry_msgs.msg import Pose
from tf.transformations import quaternion_from_euler
import os

def spawn_mantel():
    rospy.init_node("spawn_mantel_node")

    urdf_path = os.path.join(
        os.path.expanduser("~"),
        "test2_ws/src/my_objects/urdf/mantel.urdf"
    )

    with open(urdf_path, "r") as f:
        model_xml = f.read()

    rospy.wait_for_service("/gazebo/spawn_urdf_model")
    spawn_model = rospy.ServiceProxy("/gazebo/spawn_urdf_model", SpawnModel)

    pose = Pose()
    pose.position.x = 0.55  # o donde necesites la base
    pose.position.y = 0.45
    pose.position.z = 1.2  # justo sobre el plano del mundo

    # Sin rotación (opcional)
    q = quaternion_from_euler(0, 0, 0)
    pose.orientation.x = q[0]
    pose.orientation.y = q[1]
    pose.orientation.z = q[2]
    pose.orientation.w = q[3]

    spawn_model("mantel_base", model_xml, "", pose, "world")
    rospy.loginfo("Spawned 'mantel_base' for paletizado.")

if __name__ == "__main__":
    spawn_mantel()
