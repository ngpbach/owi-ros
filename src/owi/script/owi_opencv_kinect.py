#!/usr/bin/env python2

import sys
import rospy
import cv2
import tf2_ros
import numpy as np
from std_msgs.msg import String
from geometry_msgs.msg import TransformStamped
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import PointCloud2
import sensor_msgs.point_cloud2 as pc2

class image_converter:

  def __init__(self):
    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("/kinect2/sd/image_color_rect", Image, self.img_callback)
    self.depth_sub = rospy.Subscriber("/kinect2/sd/points", PointCloud2, self.depth_callback)
    self.br = tf2_ros.TransformBroadcaster()
    self.nose = TransformStamped()
    self.centroid = None

  def depth_callback(self,data):

    if self.centroid is not None:    
      gen = pc2.read_points(data, skip_nans=True, field_names=("x", "y", "z"), uvs=(self.centroid,))
      for p in gen:
        print ("{:.2f}\t{:.2f}\t{:.2f}".format(*p))
        self.nose.header.stamp = rospy.Time.now()
        self.nose.header.frame_id = "kinect2_link"
        self.nose.child_frame_id = "nose_link"
        self.nose.transform.translation.x = p[0]
        self.nose.transform.translation.y = p[1]
        self.nose.transform.translation.z = p[2]
        self.nose.transform.rotation.w = 1
        self.br.sendTransform(self.nose)



  def img_callback(self,data):
    try:
      frame = self.bridge.imgmsg_to_cv2(data)
    except CvBridgeError as e:
      print(e)

    frame_h, frame_w = frame.shape[:2]
    center = (frame_w/2, frame_h/2)

    # haarcascade face detection
    face_cascade = cv2.CascadeClassifier("lbpcascade_frontalface_improved.xml")

    # convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
  
    # Detects faces of different sizes in the input image 
    faces = face_cascade.detectMultiScale(gray, 1.3, 5) 

    if type(faces) is np.ndarray:
        x,y,w,h = faces[0] 

        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,255),3)   

        self.centroid = (x+w/2,y+h/2)
        displacement = np.subtract(center, self.centroid)

        cv2.arrowedLine(frame, center, self.centroid, color=(0,255,0), thickness=3)
        cv2.putText(frame, "%d, %d" % (displacement[0], displacement[1]), org=(50,50), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0,255,0))

    cv2.imshow("Image window", frame)
    cv2.waitKey(1)

def main(args):
  image_converter()
  rospy.init_node('opencv_kinect', anonymous=True)
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)