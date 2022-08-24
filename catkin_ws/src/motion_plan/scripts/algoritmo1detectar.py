#! /usr/bin/env python
from __future__ import print_function
import rospy
import sense_p

import roslib
import os
import sys
import rospkg
import cv2  # openCV for image processing
import numpy as np
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

def callback_laser():
    os.system('rosrun motion_plan deteccion.py')
    

def main():
    rospy.init_node("proceso", disable_signals=True, anonymous=True)
    callback_laser()

    #rospy.spin()

if __name__ == '__main__':
  main()
