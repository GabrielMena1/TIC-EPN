#!/usr/bin/env python
# coding=utf-8

from __future__ import print_function

import roslib

import sys
import rospy
import rospkg
import cv2  # openCV for image processing
import numpy as np

# messeges for subscribing and publishing
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError  # cv_bridge bridges the gap between ros msgs and openCV
from enum import Enum
#from scipy import ndimage  # import scipy library for center of mass calculation
from gazebo_msgs.srv import SpawnModel, DeleteModel
from geometry_msgs.msg import PoseStamped, Pose, Point, Quaternion

# ---------------------------------------IMAGE PROCESSING---------------------------------------------

class image_to_initial_state:
    received_image = [None]

    class Color(Enum):
        Red = 0
        Blue = 1
        Green = 2
        Yellow = 3

    ## @brief initialize the class artifacts
    def __init__(self):
        self.initial_state_pub = rospy.Publisher("initial_state_from_cameras", Image, queue_size=1)
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/cameras/left_hand_camera/image", Image, self.callback)
	#rospy.Rate(10) # 10hz
        self.received_image = [None]
        # dictionary for colors' lower and upper HSV values
        self.ColorDict = {self.Color.Red: {'LowerHSV': (0, 52, 115), 'UpperHSV': (0, 255, 255)},
                          self.Color.Blue: {'LowerHSV': (110, 50, 50), 'UpperHSV': (130, 255, 255)},
                          self.Color.Green: {'LowerHSV': (50, 100, 50), 'UpperHSV': (70, 255, 255)}}

    ## @brief ROS saves images as ros messages, therefore we need to convert it
    ##        using CvBridge to cv2 format in order to do image processing
    def callback(self, data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print("Error! image converting to cv2 format failed")
        self.received_image[0] = cv_image

    ## @brief creates the masked image for each cube specific color
    ## @param Color an Enum of the used colors
    ## @return mask a masked image

    def image_processing(self, Color):
        original = self.received_image[0]
	#cv2.imshow('Original',original)
	#cv2.waitKey(0)
	self.resut = [0]
        # converts the image to HSV
        hsv = cv2.cvtColor(original, cv2.COLOR_BGR2HSV)
        # a different image processing routine for red due to Baxter's red body
	mask = cv2.inRange(hsv, self.ColorDict.get(Color).get('LowerHSV'),self.ColorDict.get(Color).get('UpperHSV'))
        # erode and dilate the mask in order to clean noise
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
	#cv2.imshow('Mascara',mask)
	#cv2.waitKey(100)
        return mask

    ## @brief calculates the center of mass of the cubes using a masked image of each cube
    def masked_image(self):
        red_mask = self.image_processing(self.Color.Red)
	self.contorno_red = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]

        blue_mask = self.image_processing(self.Color.Blue)
	self.contorno_blue = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]

        #cv2.imshow('Mascara',blue_mask)
	#cv2.waitKey()
	green_mask = self.image_processing(self.Color.Green)
	self.contorno_green = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]

	#cv2.imshow('Mascara',self.contorno_green)
	#cv2.waitKey()

    ## @brief calculate the initial state from the center of mass and publish it
    def find_obj(self):
	Flag = 0	
	while Flag == 0:
            # deduct the initial state using the center of mass x values 
            self.masked_image()
            if len(self.contorno_red): 
	   	self.exist_img = 'Yes'
	    	print (self.exist_img)

            elif len(self.contorno_blue): 
	    	self.exist_img = 'Yes'
	    	print (self.exist_img)

            elif len(self.contorno_green): 
	    	self.exist_img = 'Yes'
	    	print (self.exist_img)
	    else: 
		self.exist_img = 'No'
	    	print (self.exist_img)
            # turn the list into a string in order to publish
            #rate = rospy.Rate(0.5)
	    
	    if self.exist_img != 0:
	    	Flag = 1
	    else:
	    	print ("No hay objeto en la banda transportadora")
	    	Flag = 0
	return self.exist_img
        
	while not rospy.is_shutdown():
            rospy.loginfo(str_to_publish) # publish info in the terminal
            self.initial_state_pub.publish(str_to_publish)
            rate.sleep()
      
# -------------------------------------------- MAIN --------------------------------------------

def main(args):
    #rospy.sleep(4) # sleep untill all models have been loaded 
    i2initialState = image_to_initial_state()
    # we use "disable_signals" because ROS and OpenCV  try to control the same signals,
    # so it's necessary to disable it on ROS to avoid conflicts.
    rospy.init_node("image_to_initial_state", disable_signals=True, anonymous=True)

    global find_objeto

    find_objeto = i2initialState.find_obj()
    
    __all__ = [ 'find_objeto']

if __name__ == '__main__':
    main(sys.argv)
