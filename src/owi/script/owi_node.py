#!/usr/bin/env python
import rospy
from owi.msg import joint_state
from owi.msg import position_cmd
def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "Joints state: %s", data.position)
    
def control():
    rospy.init_node("owi_node", anonymous=True)

    rospy.Subscriber("joint_state", joint_state, callback)
    pub = rospy.Publisher("command", position_cmd, queue_size=10)

    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        pub.publish((0,90,0,0,0))
        rate.sleep()

    

if __name__ == '__main__':
    control()