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
pub = None

from gazebo_msgs.srv import (
    GetModelState,
    SetModelState,
    SpawnModel,
    DeleteModel,
)


def callback_laser(msg):
  # 120 degrees into 3 regions
  regions = {
    'right':  min(min(msg.ranges[0:9]), 10),
   
  }
  
  take_action(regions)
  
def take_action(regions):
  threshold_dist = 1.5
  linear_speed = 0
  angular_speed = 0

  msg = Twist()
  linear_x = 0
  angular_z = 0
  
  state_description = ''
  
  if regions['right'] < threshold_dist:
    state_description = 'ESFERA COLOR VERDE DETECTADA'
    linear_x = 0
    angular_z = 0

  elif  regions['right'] >  threshold_dist:
    state_description = 'ESFERA COLOR VERDE DETECTADA'
    linear_x = 0
    angular_z = 0 # Increase this angular speed for avoiding obstacle faster
  #  mover_objetos1()
 
  def mover_objetos1():
    
    [cord_z_0, cord_y_0, cord_x_0] = show_gazebo_models1('robot5')


  def show_gazebo_models1(blockName):
    try:
      model_coordinates = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)
      resp_coordinates = model_coordinates(blockName, '')
      cord_x_block = resp_coordinates.pose.position.x
      cord_z_block = resp_coordinates.pose.position.z
      cord_y_block = resp_coordinates.pose.position.y
      valorx1=cord_x_block
      valory1=cord_y_block
      valorz1=cord_z_block
    except rospy.ServiceException as e:
      rospy.loginfo("Get Model State service call failed:  {0}".format(e))
    print("------- ROBOT OBRERO 2 ENCONTRO LA ESFERA------------")
    print("    COORDENADAS DE LA ESFERA ENCONTRADA:", valorx1, valory1)


 
    return cord_z_block, cord_y_block, cord_x_block
       
 

  #rospy.loginfo(state_description)
  msg.linear.x = linear_x
  msg.angular.z = angular_z
  pub.publish(msg)
  mover_objetos1()
def main():
  global pub
  
  rospy.init_node('reading3_laser3')
  
  pub = rospy.Publisher('/cmd3_vel3', Twist, queue_size=1)
  
  sub = rospy.Subscriber('/robot3/laser3/scan3', LaserScan, callback_laser)
 # mover_objetos1()
  rospy.spin()

if __name__ == '__main__':
  main()
