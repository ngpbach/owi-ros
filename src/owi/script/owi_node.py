#!/usr/bin/env python2
import sys
import os
import time
import rospy
from PySide2 import QtCore, QtWidgets, QtUiTools
import random
from owi.msg import joint_state
from owi.msg import position_cmd

pub = rospy.Publisher("command", position_cmd, queue_size=10)
textbox = 0 

def handler(value):
    pub.publish((value,90,0,0,0))

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + " Joints state: %s", data.position)
    global textbox
    textbox.setText("%d\t %d\t %d\t %d\t %d" % (data.position[0], data.position[1], data.position[2], data.position[3], data.position[4]))

def main():    
    rospy.init_node("owi_node", anonymous=True)
    rospy.Subscriber("joint_state", joint_state, callback)    

    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app = QtWidgets.QApplication(sys.argv)
    uiFilename = os.path.join(os.path.dirname(__file__), "CtrlPanel.ui")
    window = QtUiTools.QUiLoader().load(uiFilename)

    slider0 = window.findChild(QtWidgets.QSpinBox, "spinBox_1")
    slider0.valueChanged.connect(handler)
    
    global textbox 
    textbox = window.findChild(QtWidgets.QLabel, "label_6")
    textbox.setText("hello")

    window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()