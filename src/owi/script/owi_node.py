#!/usr/bin/env python
import rospy
import time
import threading as thr
import Tkinter as tk
from owi.msg import joint_state
from owi.msg import position_cmd


class CtrlPanel:
    master = tk.Tk()
    def __init__(self, pub):
        print("hello")
        self.pub = pub
    
    def tkLoop(self):
        self.slider = tk.Scale(CtrlPanel.master, from_=-90, to=90)
        self.slider.bind("<ButtonRelease-1>", self.actuate)
        self.slider.pack()
        tk.mainloop()

    def actuate(self, event):
        self.pub.publish((self.slider.get(),90,0,0,0))


def callback(data):
    rospy.loginfo(rospy.get_caller_id() + " Joints state: %s", data.position)



def control():
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        pub.publish((0,90,0,0,0))
        rate.sleep()

def main():    
    rospy.init_node("owi_node", anonymous=True)
    rospy.Subscriber("joint_state", joint_state, callback)    
    pub = rospy.Publisher("command", position_cmd, queue_size=10)
    panel1 = CtrlPanel(pub)

    # ctrlTh = thr.Thread(target=control)    
    # ctrlTh.daemon = True
    # ctrlTh.start()

    panel1.tkLoop()





if __name__ == '__main__':
    main()