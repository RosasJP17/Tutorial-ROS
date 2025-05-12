#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import JointState
from visualization_msgs.msg import Marker

class JointStateMarker:
    def __init__(self):
        rospy.init_node('joint_state_marker_rad')
        self.pub = rospy.Publisher('/joint_state_marker_rad', Marker, queue_size=10)
        rospy.Subscriber('/joint_states', JointState, self.callback)

        self.base_frame = "base_link"

        self.joint_order = [
            'elbow_joint',
            'robotiq_85_left_knuckle_joint',
            'shoulder_lift_joint',
            'shoulder_pan_joint',
            'wrist_1_joint',
            'wrist_2_joint'
        ]

        self.joint_map = {
            'elbow_joint': 'q1',
            'robotiq_85_left_knuckle_joint': 'q2',
            'shoulder_lift_joint': 'q3',
            'shoulder_pan_joint': 'q4',
            'wrist_1_joint': 'q5',
            'wrist_2_joint': 'q6'
        }

    def callback(self, msg):
        name_to_position = dict(zip(msg.name, msg.position))

        q1 = name_to_position.get('elbow_joint', 0)
        q2 = name_to_position.get('robotiq_85_left_knuckle_joint', 0)
        q3 = name_to_position.get('shoulder_lift_joint', 0)
        q4 = name_to_position.get('shoulder_pan_joint', 0)
        q5 = name_to_position.get('wrist_1_joint', 0)
        q6 = name_to_position.get('wrist_2_joint', 0)

        text = (
            f"q1: {q1:<7.3f}  q4: {q4:<7.3f}\n"
            f"q2: {q2:<7.3f}  q5: {q5:<7.3f}\n"
            f"q3: {q3:<7.3f}  q6: {q6:<7.3f}\n"
        )

        # Crear el marcador
        marker = Marker()
        marker.header.frame_id = self.base_frame
        marker.header.stamp = rospy.Time.now()
        marker.ns = "joint_text"
        marker.id = 0
        marker.type = Marker.TEXT_VIEW_FACING
        marker.action = Marker.ADD

        marker.pose.position.x = 0.0
        marker.pose.position.y = -0.1
        marker.pose.position.z = 0.3
        marker.pose.orientation.w = 1.0

        marker.scale.z = 0.05
        marker.color.r = 1.0
        marker.color.g = 1.0
        marker.color.b = 1.0
        marker.color.a = 1.0

        marker.text = text

        self.pub.publish(marker)

if __name__ == '__main__':
    JointStateMarker()
    rospy.spin()
