#!/usr/bin/env python2
import sys
import os
import copy
import rospy
import tf2_ros
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg



def plan_path():
  moveit_commander.roscpp_initialize(sys.argv)
  rospy.init_node('moveit_python_interface')
  tfBuf = tf2_ros.Buffer()
  listener = tf2_ros.TransformListener(tfBuf)
  br = tf2_ros.StaticTransformBroadcaster()
  display_trajectory_publisher = rospy.Publisher("move_group/display_planned_path", moveit_msgs.msg.DisplayTrajectory, queue_size=10)

  robot = moveit_commander.RobotCommander()
  scene = moveit_commander.PlanningSceneInterface()
  group = moveit_commander.MoveGroupCommander("arm")

  rate = rospy.Rate(1)
  rospy.sleep(1)
  
  
  kn_pose = geometry_msgs.msg.PoseStamped()
  kn_pose.header.frame_id = "kinect2_link"
  kn_pose.pose.position = geometry_msgs.msg.Point(x=0.1, y=0.0, z=0.0)
  kn_pose.pose.orientation = geometry_msgs.msg.Quaternion(x=0, y=-1, z=1, w=0)
  filename = os.path.join(os.path.dirname(__file__), "kinect.stl")
  scene.add_mesh("kinect", kn_pose, filename, size=(0.001,0.001,0.001))

  while not rospy.is_shutdown():
    raw_input("Press Enter to continue...")
    try:
      trans = tfBuf.lookup_transform("base_link", "nose_link", rospy.Time())
    except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
      rate.sleep()
      continue

    pos_target = (trans.transform.translation.x,
                  trans.transform.translation.y,
                  trans.transform.translation.z)
    print (pos_target)
    group.set_num_planning_attempts(10)
    group.set_goal_position_tolerance(0.05)
    group.set_position_target(pos_target, "dummy_eef")
    group.go()
    group.stop()
    print ("Done")


if __name__=='__main__':
  try:
    plan_path()
  except rospy.ROSInterruptException:
    pass