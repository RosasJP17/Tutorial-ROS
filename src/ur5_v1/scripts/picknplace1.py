#!/usr/bin/env python3

import sys
import rospy
import moveit_commander
import geometry_msgs.msg
import copy
import tf
import math


def main():
    # Inicialización
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node('pick_and_place_node', anonymous=True)

    arm_group = moveit_commander.MoveGroupCommander("manipulator")
    arm_group.set_planner_id("RRTConnectkConfigDefault")
    arm_group.set_planning_time(10)

    # Ir a posición inicial segura
    arm_group.set_named_target("up")
    arm_group.go(wait=True)

    # Definir orientación del gripper (mirando hacia abajo)
    roll, pitch, yaw = 0.0, 0.0, 1.57  # gripper hacia abajo
    q = tf.transformations.quaternion_from_euler(roll, pitch, yaw)

    # ------------------------------
    # Poses del Pick
    # ------------------------------
    pick_pose_above = geometry_msgs.msg.Pose()
    pick_pose_above.position.x = 0.4
    pick_pose_above.position.y = 0.0
    pick_pose_above.position.z = 0.3  # Altura segura sobre la mesa
    pick_pose_above.orientation.x = q[0]
    pick_pose_above.orientation.y = q[1]
    pick_pose_above.orientation.z = q[2]
    pick_pose_above.orientation.w = q[3]

    pick_pose = copy.deepcopy(pick_pose_above)
    pick_pose.position.z = 0.25  # Altura para recoger objeto

    # ------------------------------
    # Poses del Place
    # ------------------------------
    place_pose_above = copy.deepcopy(pick_pose_above)
    place_pose_above.position.y = 0.3  # hacia un lado

    place_pose = copy.deepcopy(place_pose_above)
    place_pose.position.z = 0.25  # Altura para soltar objeto

    # ------------------------------
    # Movimiento de Pick
    # ------------------------------
    arm_group.set_pose_target(pick_pose_above)
    arm_group.go(wait=True)

    arm_group.set_pose_target(pick_pose)
    arm_group.go(wait=True)

    rospy.sleep(1)  # Simula cerrar gripper

    arm_group.set_pose_target(pick_pose_above)
    arm_group.go(wait=True)

    # ------------------------------
    # Movimiento de Place
    # ------------------------------
    arm_group.set_pose_target(place_pose_above)
    arm_group.go(wait=True)

    arm_group.set_pose_target(place_pose)
    arm_group.go(wait=True)

    rospy.sleep(1)  # Simula abrir gripper

    arm_group.set_pose_target(place_pose_above)
    arm_group.go(wait=True)

    # ------------------------------
    # Regreso a home
    # ------------------------------
    arm_group.set_named_target("up")
    arm_group.go(wait=True)

    arm_group.stop()
    arm_group.clear_pose_targets()
    moveit_commander.roscpp_shutdown()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
