#!/usr/bin/env python2
import sys
import time
import rospy
from PySide2 import QtCore, QtWidgets, QtUiTools
import random
from owi.msg import joint_state
from owi.msg import position_cmd

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super(MyWidget, self).__init__()

        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo"]

        self.button = QtWidgets.QPushButton("Click me!")
        self.text = QtWidgets.QLabel("Hello World")
        self.text.setAlignment(QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

        self.button.clicked.connect(self.magic)


    def magic(self):
        self.text.setText(random.choice(self.hello))


def callback(data):
    rospy.loginfo(rospy.get_caller_id() + " Joints state: %s", data.position)

def main():    
    # rospy.init_node("owi_node", anonymous=True)
    # rospy.Subscriber("joint_state", joint_state, callback)    
    # pub = rospy.Publisher("command", position_cmd, queue_size=10)

    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app = QtWidgets.QApplication(sys.argv)
    loader = QtUiTools.QUiLoader()
    MainWindow = loader.load("./CtrlPanel.ui")
    MainWindow.show()


    sys.exit(app.exec_())

if __name__ == '__main__':
    main()