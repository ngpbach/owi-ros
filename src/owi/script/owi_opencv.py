#!/usr/bin/env python2

import cv2
import rospy
import time
import numpy as np
import owi.msg

def giveCommand(displacement):
    if not cur_pos:
        return

    cmd_pos = list(cur_pos)
    
    cmd_pos[0] += 0.05*displacement[0]   
    cmd_pos[1] += 0.05*displacement[1]

    print(cmd_pos)
    cmdPub.publish(cmd_pos)


def report_cb(data):
    global cur_pos
    cur_pos = data.position

rospy.init_node("owi_opencv_node", anonymous=True)
rospy.Subscriber("state", owi.msg.joint_state, report_cb)
cmdPub = rospy.Publisher("command", owi.msg.position_cmd, queue_size=10)
cap = cv2.VideoCapture(0)
cur_pos = None
displacement = None

while(True):

    ret, frame = cap.read()
    center = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)/2), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)/2))

    params = cv2.SimpleBlobDetector_Params()

    params.filterByArea = True
    params.minArea = 1000
    params.maxArea = 100000

    params.filterByColor = 1
    params.blobColor = 0

    params.filterByCircularity = True
    params.minCircularity = 0.5
    params.maxCircularity = 0.8

    detector = cv2.SimpleBlobDetector_create(params)
    keypoints = detector.detect(frame)

    if (keypoints):
        centroid = (int(keypoints[0].pt[0]), int(keypoints[0].pt[1]))
        displacement = np.subtract(center, centroid)

        cv2.arrowedLine(frame, center, centroid, color=(0,255,0), thickness=5)
        cv2.putText(frame, "%d, %d" % (displacement[0], displacement[1]), org=(50,50), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0,255,0))
        giveCommand(displacement)

    frame = cv2.drawKeypoints(frame, keypoints, np.array([]), color=(0,0,255))

    cv2.imshow('frame', frame) 

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()