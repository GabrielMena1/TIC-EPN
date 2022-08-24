#! /usr/bin/env python

import rospy
import math
import os
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
pub3 = None

from gazebo_msgs.srv import (
    GetModelState,
    SetModelState,
    SpawnModel,
    DeleteModel,
)


def callback_laser(msg):
  # 120 degrees into 3 regions
  regions = {
    'right':  min(min(msg.ranges[0:2]), 10),
    'front':  min(min(msg.ranges[3:5]), 10),
    'left':   min(min(msg.ranges[6:9]), 10),
  }
  
  take_action(regions)
  
def take_action(regions):
  threshold_dist = 1.5
  linear_speed = 0.6
  angular_speed = 1

  msg = Twist()
  linear_x = 0
  angular_z = 0
  
  state_description = ''
  
  if regions['front'] > threshold_dist and regions['left'] > threshold_dist and regions['right'] > threshold_dist:
    state_description = 'case 1 - no obstacle'
  #  linear_x = linear_speed
 #   angular_z = 0

    def mover_objetos1():
    
      [cord_z_0, cord_y_0, cord_x_0] = show_gazebo_models1('robot5')
    def show_gazebo_models1(blockName):
      global valorx1,valory1
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
      return cord_z_block, cord_y_block, cord_x_block
    def mover_objetos2():
    
      [cord_z_0, cord_y_0, cord_x_0] = show_gazebo_models2('robot3')

    def show_gazebo_models2(blockName):
      global valorx2,valory2,otro1
      try:
        model_coordinates = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)
        resp_coordinates = model_coordinates(blockName, '')
        cord_x_block = resp_coordinates.pose.position.x
        cord_z_block = resp_coordinates.pose.position.z
        cord_y_block = resp_coordinates.pose.position.y
        valorx2=cord_x_block
        valory2=cord_y_block
        valorz2=cord_z_block
      except rospy.ServiceException as e:
        rospy.loginfo("Get Model State service call failed:  {0}".format(e))
   
 
      otro1=math.sqrt((valorx1-valorx2)*(valorx1-valorx2)+(valory1-valory2)*(valory1-valory2))
      return cord_z_block, cord_y_block, cord_x_block

    def mover_objetos3():
    
      [cord_z_0, cord_y_0, cord_x_0] = show_gazebo_models3('robot3')

    def show_gazebo_models3(blockName):
      global valorx3,valory3,otro2
      try:
        model_coordinates = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)
        resp_coordinates = model_coordinates(blockName, '')
        cord_x_block = resp_coordinates.pose.position.x
        cord_z_block = resp_coordinates.pose.position.z
        cord_y_block = resp_coordinates.pose.position.y
        valorx3=cord_x_block
        valory3=cord_y_block
        valorz3=cord_z_block
      except rospy.ServiceException as e:
        rospy.loginfo("Get Model State service call failed:  {0}".format(e))
   
 
      otro2=math.sqrt((valorx1-valorx3)*(valorx1-valorx3)+(valory1-valory3)*(valory1-valory3))

      
     
      return cord_z_block, cord_y_block, cord_x_block

    mover_objetos1()
    mover_objetos2()
    mover_objetos3()
    print(otro1,otro2)
    if valorx3 > valorx1-2.5 and valorx3< valorx1+2.5 and valory3 > valory1-2.5 and valory3 < valory1+2.5: 
      print ("*************************ROBOT OBRERO 1*************************")
                 
                   
      print("Coordenadas del objeto encontrado",valorx1, valory1)
      os.system('rosrun motion_plan algoritmo3parar.py')
    if otro2 < otro1:
      linear_x = linear_speed
      angular_z = 0
    else:
      linear_x = 0
      angular_z = 1

  elif regions['front'] < threshold_dist and regions['left'] < threshold_dist and regions['right'] < threshold_dist:
    state_description = 'case 7 - front and left and right'
    linear_x = -linear_speed
    angular_z = angular_speed # Increase this angular speed for avoiding obstacle faster
  elif regions['front'] < threshold_dist and regions['left'] > threshold_dist and regions['right'] > threshold_dist:
    state_description = 'case 2 - front'
    linear_x = 0
    angular_z = angular_speed
  elif regions['front'] > threshold_dist and regions['left'] > threshold_dist and regions['right'] < threshold_dist:
    state_description = 'case 3 - right'
    linear_x = 0
    angular_z = -angular_speed
  elif regions['front'] > threshold_dist and regions['left'] < threshold_dist and regions['right'] > threshold_dist:
    state_description = 'case 4 - left'
    linear_x = 0
    angular_z = angular_speed
  elif regions['front'] < threshold_dist and regions['left'] > threshold_dist and regions['right'] < threshold_dist:
    state_description = 'case 5 - front and right'
    linear_x = 0
    angular_z = -angular_speed
  elif regions['front'] < threshold_dist and regions['left'] < threshold_dist and regions['right'] > threshold_dist:
    state_description = 'case 6 - front and left'
    linear_x = 0
    angular_z = angular_speed
  elif regions['front'] > threshold_dist and regions['left'] < threshold_dist and regions['right'] < threshold_dist:
    state_description = 'case 8 - left and right'
    linear_x = linear_speed
    angular_z = 0
  else:
    state_description = 'unknown case'
    rospy.loginfo(regions)

  def mover_objetos1():
    
    [cord_z_0, cord_y_0, cord_x_0] = show_gazebo_models1('robot5')


  def show_gazebo_models1(blockName):
    global valorx1,valory1
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
    print("------- ESFERA VERDE ENCONTRADA POR EL ROBOT EXPLORADOR------------")
    print("***Estado Robot Explorador: En Espera")
    print("***Coordenadas esfera:", valorx1, valory1)
   # print(math.sqrt(valorx1*valorx1) )
    

 
    return cord_z_block, cord_y_block, cord_x_block


  def mover_objetos2():
    
    [cord_z_0, cord_y_0, cord_x_0] = show_gazebo_models2('robot2')


  def show_gazebo_models2(blockName):
    global valorx1,valory1,valorx2,valory2 
    try:
      model_coordinates = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)
      resp_coordinates = model_coordinates(blockName, '')
      cord_x_block = resp_coordinates.pose.position.x
      cord_z_block = resp_coordinates.pose.position.z
      cord_y_block = resp_coordinates.pose.position.y
      valorx2=cord_x_block
      valory2=cord_y_block
      valorz2=cord_z_block
    except rospy.ServiceException as e:
      rospy.loginfo("Get Model State service call failed:  {0}".format(e))
   
    print("***Coordenadas Robot obrero 1:", valorx2, valory2)
    m=math.sqrt((valorx1-valorx2)*(valorx1-valorx2)+(valory1-valory2)*(valory1-valory2))
  #  man= 5.337465637546467
    print("       Estado robot obrero 1: Buscando")
    print("       Distancia entre robot 1 y esfera verde:",m)
   # print("   Distancia entre robots obreros:",man)
  

 
    return cord_z_block, cord_y_block, cord_x_block


  def mover_objetos3():
    
    [cord_z_0, cord_y_0, cord_x_0] = show_gazebo_models3('robot2')


  def show_gazebo_models3(blockName):
    global valorx2,valory2
    try:
      model_coordinates = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)
      resp_coordinates = model_coordinates(blockName, '')
      cord_x_block = resp_coordinates.pose.position.x
      cord_z_block = resp_coordinates.pose.position.z
      cord_y_block = resp_coordinates.pose.position.y
      valorx3=cord_x_block
      valory3=cord_y_block
      valorz3=cord_z_block
    except rospy.ServiceException as e:
      rospy.loginfo("Get Model State service call failed:  {0}".format(e))
   
    print("***Coordenadas Robot obrero 2:", valorx3, valory3)
    man=math.sqrt((valorx3-valorx2)*(valorx3-valorx2)+(valory3-valory2)*(valory3-valory2))
    
    print("       Estado robot obrero 3: Buscando")
    print("***Distancia entre robots obreros:",man)


 
    return cord_z_block, cord_y_block, cord_x_block


       
  #rospy.loginfo(state_description)
  msg.linear.x = linear_x
  msg.angular.z = angular_z
  pub3.publish(msg)
  mover_objetos1()
  mover_objetos2()
  mover_objetos3()
def main():
  global pub3
  
  rospy.init_node('reading3_laser3')
  
  #print("hola")
  
  pub3 = rospy.Publisher('/cmd3_vel3', Twist, queue_size=1)
  
  sub3 = rospy.Subscriber('/robot3/laser3/scan3', LaserScan, callback_laser)
  
  rospy.spin()

if __name__ == '__main__':
  main()
