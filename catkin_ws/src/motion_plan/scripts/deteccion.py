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

from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
pub2 = None
import os
from gazebo_msgs.srv import (
    GetModelState,
    SetModelState,
    SpawnModel,
    DeleteModel,
)

# ---------------------------------------IMAGE PROCESSING---------------------------------------------


class image_to_initial_state:
    received_image = [None]
   # global regions
    class Color(Enum):
        Red = 0
        Blue = 1
        Green = 2
        Yellow = 3

    ## @brief initialize the class artifacts
    def __init__(self):
        self.initial_state_pub = rospy.Publisher("initial_state_from_cameras", Image, queue_size=1)
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/cameras/head_camera/image", Image, self.callback)
	#rospy.Rate(10) # 10hz
        self.received_image = [None]
        # dictionary for colors' lower and upper HSV values
        self.ColorDict = {self.Color.Red: {'LowerHSV': (71, 255, 255), 'UpperHSV': (255, 255, 255)},
                          self.Color.Blue: {'LowerHSV': (110, 50, 50), 'UpperHSV': (130, 255, 255)},
                          self.Color.Green: {'LowerHSV': (50, 100, 50), 'UpperHSV': (70, 255, 255)},
                          self.Color.Yellow: {'LowerHSV': (0, 0, 0), 'UpperHSV': (49, 99, 49)}}
        self.Cubes_center_of_mass = [0, 0, 0, 0]

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
        if Color == self.Color.Red:
            # splits the image to h, s, v where v is a gray scale image
            (h, s, v) = cv2.split(hsv)
           
            v[480:][:] = 1
         
            hsv_no_red = cv2.merge((h, s, v))
    
            mask = cv2.inRange(hsv_no_red, self.ColorDict.get(Color).get('LowerHSV'),
                               self.ColorDict.get(Color).get('UpperHSV'))
        else:
     
            mask = cv2.inRange(hsv, self.ColorDict.get(Color).get('LowerHSV'),
                               self.ColorDict.get(Color).get('UpperHSV'))
   
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        return mask

 
    def masked_image(self):
        red_mask = self.image_processing(self.Color.Red)
	self.contorno_red = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]
        blue_mask = self.image_processing(self.Color.Blue)
	self.contorno_blue = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]

	green_mask = self.image_processing(self.Color.Green)
	self.contorno_green = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]
        yellow_mask = self.image_processing(self.Color.Yellow)
        self.contorno_yellow = cv2.findContours(yellow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]

    def initial_color(self):
	Flag = 0
	globalv= 2	
   
	while Flag == 0:
            
            self.masked_image()
            if len(self.contorno_red): 
	   	self.color = 'Rojo'
	
	    	namefig = 'Rectangulo'
                Flag = 0
	    	print (namefig)
	  
          
            elif len(self.contorno_green):
	    	self.color = 'Verde'
    	
	    	namefig = 'Circulo'
		globalv = 1
                Flag = 0
	    	if self.valorx > self.valorx1-2.5 and self.valorx < self.valorx1+2.5 and self.valory > self.valory1-2.5 and self.valory < self.valory1+2.5: 
                    print ("*************************ROBOT EXPLORADOR*************************")
                    print ("-------------------ESFERA VERDE DETECTADA CERCA-------------------")
                    self.mover_objetos() 
                    self.mover_objetos1() 
                    self.mover_objetos2() 
                    self.mover_objetos3() 
                    print("Coordenadas del objeto encontrado:",self.valorx1, self.valory1)
                    os.system('rosrun motion_plan algoritmo1parar.py')
	    	else: 
                
                    print ("*************************ROBOT EXPLORADOR*************************")
                    print ("-------------------ESFERA VERDE DETECTADA PERO LEJOS-------------------") 
                    self.mover_objetos() 
                    self.mover_objetos1() 
                    self.mover_objetos2() 
                    self.mover_objetos3()                    
                
           
                print("Robot Explorador coordenadas:",self.valorx, self.valory)
                print("      Estado: en movimiento")
 #               print("Coordenadas del objeto",self.valorx1, self.valory1)
                print("Robot obrero 1 coordenadas:",self.valorx2, self.valory2)
                print("      Estado: en espera")
                print("Robot obrero 2 coordenadas:",self.valorx3, self.valory3)

                print("      Estado: en espera")
               
	    else:
                print ("*************************ROBOT EXPLORADOR*************************")
	    	print ("-------------------ESFERA VERDE NO DETECTADA-------------------")
	    	Flag = 0
		globalv= 0
                namefig = 'Circulo'
                self.color = 'Azul'
                self.mover_objetos() 
                self.mover_objetos1() 
                self.mover_objetos2() 
                self.mover_objetos3() 
                print("Robot Explorador coordenadas:",self.valorx, self.valory)
                print("      Estado: en movimiento")
  #              print("Coordenadas del objeto",self.valorx1, self.valory1)
                print("Robot obrero 1 coordenadas:",self.valorx2, self.valory2)
                print("      Estado: en espera")

                print("Robot obrero 2 coordenadas:",self.valorx3, self.valory3)
                print("      Estado: en espera")


               # self.mover_objetos() 
               # self.mover_objetos1() 
                #os.system('rosrun motion_plan algoritmo1detectar.py')
	return self.color,namefig
        
	while not rospy.is_shutdown():
            rospy.loginfo(str_to_publish)
            self.initial_state_pub.publish(str_to_publish)
            rate.sleep()
 
 

    def initial_form(self):
        red_mask = self.image_processing(self.Color.Red)
	self.contorno_red = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]
        blue_mask = self.image_processing(self.Color.Blue)
	self.contorno_blue = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]
	green_mask = self.image_processing(self.Color.Green)
	self.contorno_green = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]
	
	namefig = 0
        if len(self.contorno_red): 
	    self.color = 'Rojo'
	   
	    namefig = 'Rectangulo'
	    print (namefig)
	    return namefig

        elif len(self.contorno_blue): 
	    self.color = 'Azul'

	    namefig = 'Rectangulo'
	    print (namefig)
	    return namefig

        elif len(self.contorno_green): 
	    self.color = 'Verde'

	    namefig = 'Circulo'
	    print (namefig)
	    return namefig
    def mover_objetos1(self):
   
        [cord_z_0, cord_y_0, cord_x_0] = self.show_gazebo_models1('robot5')


    def show_gazebo_models1(self, blockName):
        try:
            model_coordinates = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)
            resp_coordinates = model_coordinates(blockName, '')
            cord_x_block = resp_coordinates.pose.position.x
            cord_z_block = resp_coordinates.pose.position.z
            cord_y_block = resp_coordinates.pose.position.y
            self.valorx1=cord_x_block
            self.valory1=cord_y_block
            self.valorz1=cord_z_block


        except rospy.ServiceException as e:
            rospy.loginfo("Get Model State service call failed:  {0}".format(e))
        #print(self.valorx1, self.valory1, self.valorz1)
        return cord_z_block, cord_y_block, cord_x_block
      
    def mover_objetos2(self):
   
        [cord_z_0, cord_y_0, cord_x_0] = self.show_gazebo_models2('robot2')


    def show_gazebo_models2(self, blockName):
        try:
            model_coordinates = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)
            resp_coordinates = model_coordinates(blockName, '')
            cord_x_block = resp_coordinates.pose.position.x
            cord_z_block = resp_coordinates.pose.position.z
            cord_y_block = resp_coordinates.pose.position.y
            self.valorx2=cord_x_block
            self.valory2=cord_y_block
            self.valorz2=cord_z_block


        except rospy.ServiceException as e:
            rospy.loginfo("Get Model State service call failed:  {0}".format(e))
       
        return cord_z_block, cord_y_block, cord_x_block
      
    def mover_objetos3(self):
   
        [cord_z_0, cord_y_0, cord_x_0] = self.show_gazebo_models3('robot3')


    def show_gazebo_models3(self, blockName):
        try:
            model_coordinates = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)
            resp_coordinates = model_coordinates(blockName, '')
            cord_x_block = resp_coordinates.pose.position.x
            cord_z_block = resp_coordinates.pose.position.z
            cord_y_block = resp_coordinates.pose.position.y
            self.valorx3=cord_x_block
            self.valory3=cord_y_block
            self.valorz3=cord_z_block


        except rospy.ServiceException as e:
            rospy.loginfo("Get Model State service call failed:  {0}".format(e))
       
        return cord_z_block, cord_y_block, cord_x_block                  

    def mover_objetos(self):
   
        [cord_z_0, cord_y_0, cord_x_0] = self.show_gazebo_models('robot1')


    def show_gazebo_models(self, blockName):
        try:
            model_coordinates = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)
            resp_coordinates = model_coordinates(blockName, '')
            cord_x_block = resp_coordinates.pose.position.x
            cord_z_block = resp_coordinates.pose.position.z
            cord_y_block = resp_coordinates.pose.position.y
            self.valorx=cord_x_block
            self.valory=cord_y_block
            self.valorz=cord_z_block


        except rospy.ServiceException as e:
            rospy.loginfo("Get Model State service call failed:  {0}".format(e))
       # print(cord_x_block, cord_y_block,cord_z_block)
        return cord_z_block, cord_y_block, cord_x_block
      
         
def main(args):
  
    i2initialState = image_to_initial_state()
    i2initialState.mover_objetos() 
    i2initialState.mover_objetos1() 
 
    rospy.init_node("image_to_initial_state", disable_signals=True, anonymous=True)
    
    global objeto_color, objeto_form

    [objeto_color,globalv]=i2initialState.initial_color()

 
    
    __all__ = [ 'objeto_color', 'objeto_form', 'globalv' ]
    rospy.spin()
    
if __name__ == '__main__':
    main(sys.argv)
