#!/usr/bin/env python3

import rospy
from gazebo_msgs.srv import SpawnModel, DeleteModel
from geometry_msgs.msg import Pose

def delete_model(name):
    try:
        rospy.wait_for_service('/gazebo/delete_model')
        delete_srv = rospy.ServiceProxy('/gazebo/delete_model', DeleteModel)
        delete_srv(name)
    except rospy.ServiceException:
        pass

def spawn_colored_cube(model_name, color_rgba, x, y, z):
    cube_sdf = f"""
    <sdf version='1.6'>
      <model name='{model_name}'>
        <static>false</static>
        <link name='{model_name}_link'>
          <pose>{x} {y} {z} 0 0 0</pose>
          <collision name='collision'>
            <geometry>
              <box>
                <size>0.04 0.04 0.04</size>
              </box>
            </geometry>
          </collision>
          <visual name='visual'>
            <geometry>
              <box>
                <size>0.04 0.04 0.04</size>
              </box>
            </geometry>
            <material>
              <ambient>{color_rgba}</ambient>
              <diffuse>{color_rgba}</diffuse>
            </material>
          </visual>
          <inertial>
            <mass>0.1</mass>
          </inertial>
        </link>
      </model>
    </sdf>
    """

    rospy.wait_for_service('/gazebo/spawn_sdf_model')
    spawn_model = rospy.ServiceProxy('/gazebo/spawn_sdf_model', SpawnModel)
    pose = Pose()

    try:
        spawn_model(model_name, cube_sdf, "", pose, "world")
        rospy.loginfo(f"Spawned {model_name}")
    except rospy.ServiceException as e:
        rospy.logerr(f"Failed to spawn {model_name}: {e}")

if __name__ == "__main__":
    rospy.init_node("spawn_colored_cubes")

    # Eliminar si ya existen
    for name in ["red_cube", "green_cube", "blue_cube", "purple_cube"]:
        delete_model(name)

    # Spawnear cubos con diferentes colores
    spawn_colored_cube("red_cube",   "1 0.5 0 1", 0.5,  0.0, 1.2)
    spawn_colored_cube("green_cube", "0.1 1 0.7 1", 0.6,  0.1, 1.2)
    spawn_colored_cube("blue_cube",  "0.5 0.85 0.9 1", 0.4, -0.1, 1.2)
    spawn_colored_cube("purple_cube", "0.5 0 0.5 1", 0.3, -0.2, 1.2)

