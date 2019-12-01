#!/usr/bin/env python2
import sys
import os
import copy
import rospy
# import tf2
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg

def plan_path():
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node('moveit_python_interface')
    # rate = rospy.Rate(1)

    # br = tf2.StaticTransformBroadcaster()
    # robot = moveit_commander.RobotCommander()
    scene = moveit_commander.PlanningSceneInterface()
    # group = moveit_commander.MoveGroupCommander("arm")

    # display_trajectory_publisher = rospy.Publisher("move_group/display_planned_path", moveit_msgs.msg.DisplayTrajectory, queue_size=10)
    rospy.sleep(1)
    
    
    kn_pose = geometry_msgs.msg.PoseStamped()
    kn_pose.header.frame_id = "kinect2_link"
    kn_pose.pose.position = geometry_msgs.msg.Point(x=0.1, y=0.0, z=0.0)
    kn_pose.pose.orientation = geometry_msgs.msg.Quaternion(x=0, y=-1, z=1, w=0)
    filename = os.path.join(os.path.dirname(__file__), "kinect.stl")
    scene.add_mesh("kinect", kn_pose, filename, size=(0.001,0.001,0.001))

    # scene.get_object_poses()
    # group.set_random_target()
    # group.plan()

if __name__=='__main__':
  try:
    plan_path()
  except rospy.ROSInterruptException:
    pass