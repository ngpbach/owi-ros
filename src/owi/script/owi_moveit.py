#!/usr/bin/env python2
import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg

def plan_path():
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node('move_group_python_interface')

    robot = moveit_commander.RobotCommander()
    scene = moveit_commander.PlanningSceneInterface()
    group = moveit_commander.MoveGroupCommander("arm")

    display_trajectory_publisher = rospy.Publisher("move_group/display_planned_path", moveit_msgs.msg.DisplayTrajectory)
    rospy.sleep(5)

    print(robot.get_current_state())


if __name__=='__main__':
  try:
    plan_path()
  except rospy.ROSInterruptException:
    pass