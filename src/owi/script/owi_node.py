#!/usr/bin/env python2
import sys
import os
import time
import numpy
import rospy
from PySide2 import QtCore, QtWidgets, QtUiTools
import random
from sensor_msgs.msg import JointState
import owi.msg


class Panel():

    @classmethod
    def __init__(cls):
        rospy.init_node("owi_node", anonymous=True)
        rospy.Subscriber("state", owi.msg.joint_state, cls.report_cb)
        rospy.Subscriber("/move_group/fake_controller_joint_states", JointState,cls.execute_cb)
        cls.cmdPub = rospy.Publisher("command", owi.msg.position_cmd, queue_size=10)
        cls.statePub = rospy.Publisher("owi_state_report", JointState, queue_size=10)

        cls.state = JointState()
        cls.state.name =  [ "jointLink1",
                            "jointLink2",
                            "jointLink3",
                            "jointLink4",
                            "jointRgripper"]
        cls.state.position = [0,numpy.pi/2,0,0,0] 

        QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
        app = QtWidgets.QApplication(sys.argv)
        uiFilename = os.path.join(os.path.dirname(__file__), "CtrlPanel.ui")
        window = QtUiTools.QUiLoader().load(uiFilename)

        cls.textbox = window.findChild(QtWidgets.QLabel, "label_6")
        cls.spinbox1 = window.findChild(QtWidgets.QSpinBox, "spinBox_1")
        cls.spinbox2 = window.findChild(QtWidgets.QSpinBox, "spinBox_2")
        cls.spinbox3 = window.findChild(QtWidgets.QSpinBox, "spinBox_3")
        cls.spinbox4 = window.findChild(QtWidgets.QSpinBox, "spinBox_4")
        cls.spinbox5 = window.findChild(QtWidgets.QSpinBox, "spinBox_5")
        cls.button = window.findChild(QtWidgets.QPushButton, "pushButton")

        cls.button.clicked.connect(cls.clicked_cb)
        window.show()
        sys.exit(app.exec_())

    @classmethod
    def clicked_cb(cls, value):
        cls.cmdPub.publish((cls.spinbox1.value(), cls.spinbox2.value(), cls.spinbox3.value(), cls.spinbox4.value(), cls.spinbox5.value()))

    @classmethod
    def report_cb(cls, data):
        # rospy.loginfo(rospy.get_caller_id() + " joint angles deg: %s", data.position)
        cls.textbox.setText("%d\t %d\t %d\t %d\t %d" % (data.position[0], data.position[1], 
                                        data.position[2], data.position[3], data.position[4]))
        for i in range(len(cls.state.name)):
            cls.state.position[i] = numpy.pi*float(data.position[i])/180
        cls.statePub.publish(cls.state)

    @classmethod
    def execute_cb(cls, data):
        command = [0,numpy.pi/2,0,0,0]
        for i in range(len(data.position)):
            command[i] = int(180*data.position[i]/numpy.pi)
        print(command)
        cls.cmdPub.publish(command)


if __name__ == '__main__':
    Panel()


