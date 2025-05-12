#!/usr/bin/env python3

import sys
import rospy
import moveit_commander
import geometry_msgs.msg
import copy
import tf  # para la conversión de ángulos a cuaterniones

def main():
    # Inicializa MoveIt Commander y ROS node
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node('pick_and_place_node', anonymous=True)

    # Inicializa el grupo de planificación para el brazo
    arm_group = moveit_commander.MoveGroupCommander("manipulator")
    
    # Inicializa el grupo de planificación para el gripper
    gripper_group = moveit_commander.MoveGroupCommander("gripper")
    
    # Establece un tiempo de planificación mayor
    arm_group.set_planner_id("RRTConnectkConfigDefault")  # Cambia el planificador si es necesario
    arm_group.set_planning_time(20)  # Aumenta el tiempo de planificación a 20 segundos

    # Posición de los cubos en el mundo (a 1 metro de altura sobre la mesa)
    cube_positions = [
        [0.5, 0.0, 0.04],  # Cubo rojo (sobre la mesa)
        [0.6, 0.1, 0.04],  # Cubo verde (sobre la mesa)
        [0.4, -0.1, 0.04], # Cubo azul (sobre la mesa)
        [0.3, -0.2, 0.04]  # Cubo morado (sobre la mesa)
    ]

    # Definir la orientación hacia abajo para el gripper (gripper debe ver hacia el eje Z negativo)
    roll = 0.0
    pitch = 3.14
    yaw = 0.0
    quaternion = tf.transformations.quaternion_from_euler(roll, pitch, yaw)

    # Pose de 'pick' para cada cubo
    for position in cube_positions:
        pick_pose = geometry_msgs.msg.Pose()

        # Asignar la posición y la orientación
        pick_pose.position.x = position[0]
        pick_pose.position.y = position[1]
        pick_pose.position.z = position[2] + 0.15  # Ajustar la altura en z para que el robot esté ligeramente por encima del cubo
        pick_pose.orientation.x = quaternion[0]
        pick_pose.orientation.y = quaternion[1]
        pick_pose.orientation.z = quaternion[2]
        pick_pose.orientation.w = quaternion[3]

        # Establece el objetivo de pose para recoger el cubo
        arm_group.set_pose_target(pick_pose)
        success = arm_group.go(wait=True)
        
        if not success:
            rospy.logwarn(f"Movimiento fallido al intentar mover a {pick_pose.position.x}, {pick_pose.position.y}, {pick_pose.position.z}")
            break

        rospy.sleep(1)  # Simula el tiempo de recoger el cubo

        # Cerrar el gripper para recoger el cubo
        gripper_group.set_named_target("close")
        gripper_group.go(wait=True)
        rospy.sleep(1)  # Tiempo de agarre

        # Pose de 'place' (simplemente se mueve 0.3 unidades en Y)
        place_pose = copy.deepcopy(pick_pose)
        place_pose.position.y += 0.3  # Coloca el cubo un poco más lejos en Y

        # Mueve el robot a la posición de colocación
        arm_group.set_pose_target(place_pose)
        success = arm_group.go(wait=True)

        if not success:
            rospy.logwarn(f"Movimiento fallido al intentar colocar el cubo en {place_pose.position.x}, {place_pose.position.y}, {place_pose.position.z}")
            break

        rospy.sleep(1)  # Simula abrir el gripper para soltar el cubo

        # Abrir el gripper para soltar el cubo
        gripper_group.set_named_target("open")
        gripper_group.go(wait=True)

    # Regresa a una posición segura (no a la posición cero)
    safe_pose = geometry_msgs.msg.Pose()
    safe_pose.position.x = 0.5  # Ajusta para que esté lejos de los cubos
    safe_pose.position.y = 0.0
    safe_pose.position.z = 0.5  # Eleva el brazo para evitar colisiones con la mesa
    safe_pose.orientation.w = 1.0  # Sin rotación

    arm_group.set_pose_target(safe_pose)
    success = arm_group.go(wait=True)

    if not success:
        rospy.logwarn(f"Movimiento fallido al intentar mover a la posición segura: {safe_pose.position.x}, {safe_pose.position.y}, {safe_pose.position.z}")

    # Limpia
    arm_group.stop()
    arm_group.clear_pose_targets()
    moveit_commander.roscpp_shutdown()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
