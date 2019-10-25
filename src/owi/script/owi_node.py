#!/usr/bin/env python2
import sys
import os
import time
import rospy
from PySide2 import QtCore, QtWidgets, QtUiTools
import random
from sensor_msgs.msg import JointState
import owi.msg

cmdPub = rospy.Publisher("command", owi.msg.position_cmd, queue_size=10)
statePub = rospy.Publisher("owi_state_report", JointState, queue_size=10)
textbox = 0 
joint_names = [ "jointLink1",
                "jointLink2",
                "jointLink3",
                "jointLink4",
                "jointRgripper"]

def handler(value):
    cmdPub.publish((value,90,0,0,0))

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + " joint angles: %s", data.position)
    textbox.setText("%d\t %d\t %d\t %d\t %d" % (data.position[0], data.position[1], data.position[2], data.position[3], data.position[4]))

    state = JointState()
    for i,name in enumerate(joint_names):
        state.name.append(name)
        state.position.append(data.position[i])
        state.velocity.append(0)
        state.effort.append(0)

    statePub.publish(state)

def main():    
    global textbox
    rospy.init_node("owi_node", anonymous=True)
    rospy.Subscriber("state", owi.msg.joint_state, callback)

    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app = QtWidgets.QApplication(sys.argv)
    uiFilename = os.path.join(os.path.dirname(__file__), "CtrlPanel.ui")
    window = QtUiTools.QUiLoader().load(uiFilename)

    slider0 = window.findChild(QtWidgets.QSpinBox, "spinBox_1")
    slider0.valueChanged.connect(handler)
    
    textbox = window.findChild(QtWidgets.QLabel, "label_6")
    textbox.setText("hello")

    window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()