#! /usr/bin/env python

import rospy
import argparse
import struct
import sys
import copy

import rospy
import rospkg

from gazebo_msgs.msg import ModelState

from gazebo_msgs.srv import (
    GetModelState,
    SetModelState,
    SpawnModel,
    DeleteModel,
)

from geometry_msgs.msg import (
    PoseStamped,
    Pose,
    Point,
    Quaternion,
)
from std_msgs.msg import (
    Header,
    Empty,
)

from sensor_msgs.msg import LaserScan



class lector:
    senal = [0]
    def __init__(self):

    	sub= rospy.Subscriber("/robot/laser2/scan", LaserScan, self.callback_laser)
    	rospy.sleep(0.05)

    def callback_laser(self, msg):
  # 120 degrees into 3 regions
  # receive a value of range between 0 and 0.1.
        regions = {
       	    'front':  min(min(msg.ranges[3:5]), 0.1),
        }

        #rospy.loginfo(regions)

        threshold_dist = 0.1
        cont = 0

        if regions['front'] >= threshold_dist:
            state_description = 'case 1 - no obstacle'
    	    cont = 1

        elif regions['front'] < threshold_dist:
            state_description = 'case 2 - obstacle'
            cont = 0

        self.senal = cont
        #print state_description

    def show_gazebo_models(self, blockName):
        try:
            model_coordinates = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)
            resp_coordinates = model_coordinates(blockName, '')
	    cord_x_block = resp_coordinates.pose.position.x
	    cord_z_block = resp_coordinates.pose.position.z
	    cord_y_block = resp_coordinates.pose.position.y

        except rospy.ServiceException as e:
            rospy.loginfo("Get Model State service call failed:  {0}".format(e))
    
        return cord_z_block, cord_y_block, cord_x_block

    def Mover_obj(self, name_obj, pose_obj):
        y=pose_obj
        state_msg = ModelState()
    	state_msg.model_name = name_obj
    	state_msg.pose.position.x =0.38
    	state_msg.pose.position.y = y
    	state_msg.pose.position.z = 0.813
    	state_msg.pose.orientation.x = 0
    	state_msg.pose.orientation.y = 0
    	state_msg.pose.orientation.z = 0
    	state_msg.pose.orientation.w = 0
	    
    	rospy.wait_for_service('/gazebo/set_model_state')
	   
    	try:
            set_state = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)
            resp = set_state(state_msg)
    	except rospy.ServiceException, e:
            print "Service call failed: %s" %e
	    
        rospy.sleep(0.1)

    def Mover_obj_ball(self, name_obj, pose_obj):
        y=pose_obj
        state_msg = ModelState()
    	state_msg.model_name = name_obj
    	state_msg.pose.position.x =0.355
    	state_msg.pose.position.y = y
    	state_msg.pose.position.z = 0.813
    	state_msg.pose.orientation.x = 0
    	state_msg.pose.orientation.y = 0
    	state_msg.pose.orientation.z = 0
    	state_msg.pose.orientation.w = 0
	    
    	rospy.wait_for_service('/gazebo/set_model_state')
	   
    	try:
            set_state = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)
            resp = set_state(state_msg)
    	except rospy.ServiceException, e:
            print "Service call failed: %s" %e
	    
        rospy.sleep(0.1)

    def mover_objetos(self):

    	cont = 0
    	cont1 = 0

    	[cord_z_0, cord_y_0, cord_x_0] = self.show_gazebo_models('ball')
    	[cord_z_1, cord_y_1, cord_x_1] = self.show_gazebo_models('ball_1')
    	[cord_z_2, cord_y_2, cord_x_2] = self.show_gazebo_models('block_red')
    	[cord_z_3, cord_y_3, cord_x_3] = self.show_gazebo_models('block_red_1')
    	[cord_z_4, cord_y_4, cord_x_4] = self.show_gazebo_models('block_red_2')
    	[cord_z_5, cord_y_5, cord_x_5] = self.show_gazebo_models('block_red_3')
    	[cord_z_6, cord_y_6, cord_x_6] = self.show_gazebo_models('block_blue')
    	[cord_z_7, cord_y_7, cord_x_7] = self.show_gazebo_models('block_blue_1')
    	[cord_z_8, cord_y_8, cord_x_8] = self.show_gazebo_models('block_blue_2')

	#print cord_z_0, cord_y_2, cord_y_4, cord_y_7

    	if self.senal == 1 and cord_z_6 > 0.82 and cord_y_3 >= 1.18 and cord_y_3 <= 1.23 and cord_y_1 >= 1.48 and cord_y_1 <= 1.51 and cord_y_5 >= 1.78 and cord_y_5 <= 1.85 and cord_y_8 >= 2.0 and cord_y_8 <= 2.2:
	    cont_0 = cord_y_3
	    cont_1 = cord_y_1
	    cont_2 = cord_y_5
	    cont_3 = cord_y_8
	    for c in range(30):
   	    	self.Mover_obj('block_red_1', cont_0)
   	    	self.Mover_obj_ball('ball_1', cont_1)
   	    	self.Mover_obj('block_red_3', cont_2)
   	    	self.Mover_obj('block_blue_2', cont_3)
	    	cont_0 = cont_0 - 0.01
	    	cont_1 = cont_1 - 0.01
	    	cont_2 = cont_2 - 0.01
	    	cont_3 = cont_3 - 0.01
   	    self.Mover_obj('block_red_1', 0.899)
	    inter1 = 1
	    inter2 = 0
	    cont = 0

        elif self.senal == 1 and cord_z_3 > 0.82 and cord_y_1 >= 1.18 and cord_y_1 <= 1.23 and cord_y_5 >= 1.48 and cord_y_5 <= 1.53 and cord_y_8 >= 1.78 and cord_y_8 <= 1.85:
	    cont_0 = cord_y_3
	    cont_1 = cord_y_1
	    cont_2 = cord_y_5
	    cont_3 = cord_y_8
	    for c in range(30):
   	    	self.Mover_obj_ball('ball_1', cont_1)
   	    	self.Mover_obj('block_red_3', cont_2)
   	    	self.Mover_obj('block_blue_2', cont_3)
	    	cont_0 = cont_0 - 0.01
	    	cont_1 = cont_1 - 0.01
	    	cont_2 = cont_2 - 0.01
	    	cont_3 = cont_3 - 0.01
   	    self.Mover_obj_ball('ball_1', 0.899)
	    inter1 = 1
	    inter2 = 1
	    cont = 0

        elif self.senal == 1 and cord_z_1 > 0.82 and cord_y_5 >= 1.18 and cord_y_5 <= 1.23 and cord_y_8 >= 1.48 and cord_y_8 <= 1.53:
	    cont_0 = cord_y_3
	    cont_1 = cord_y_1
	    cont_2 = cord_y_5
	    cont_3 = cord_y_8
	    for c in range(30):
   	    	self.Mover_obj('block_red_3', cont_2)
   	    	self.Mover_obj('block_blue_2', cont_3)
	    	cont_0 = cont_0 - 0.01
	    	cont_1 = cont_1 - 0.01
	    	cont_2 = cont_2 - 0.01
	    	cont_3 = cont_3 - 0.01
   	    self.Mover_obj('block_red_3', 0.899)
	    inter1 = 1
	    inter2 = 1
	    cont = 0

        elif self.senal == 1 and cord_z_5 > 0.82 and cord_y_8 >= 1.18 and cord_y_8 <= 1.23:
	    cont_0 = cord_y_3
	    cont_1 = cord_y_1
	    cont_2 = cord_y_5
	    cont_3 = cord_y_8
	    for c in range(30):
   	    	self.Mover_obj('block_blue_2', cont_3)
	    	cont_0 = cont_0 - 0.01
	    	cont_1 = cont_1 - 0.01
	    	cont_2 = cont_2 - 0.01
	    	cont_3 = cont_3 - 0.01
   	    self.Mover_obj('block_blue_2', 0.899)
	    inter1 = 1
	    inter2 = 1
	    cont = 0

	#elif:
	    #rospy.spin()

def main():
    #global senal, inter1, inter2
    rospy.init_node('reading_laser_2')
    while not rospy.is_shutdown():
    	ok = lector()
    	ok.mover_objetos()
    #sub= rospy.Subscriber("/robot/laser1/scan", LaserScan, callback_laser)
    #rospy.sleep(0.1)
    #rospy.spin()
    return 0

if __name__ == '__main__':
  main()
