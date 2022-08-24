#!/usr/bin/env python
# license removed for brevity
import rospy
import baxter_interface
import subprocess
import sense_p
import detector
import cv2  # openCV for image processing
from std_msgs.msg import String

def talker():
    #pub = rospy.Publisher('chatter', String, queue_size=10)
    rospy.init_node('Clasificacion', anonymous=True)
    gripper_left = baxter_interface.Gripper('left')
    gripper_right = baxter_interface.Gripper('right')
    gripper_left.open('electric')
    gripper_right.open('electric')
    #execfile("pick1.py")
    
    #while not rospy.is_shutdown():
    hello_str = "hello world %s" % rospy.get_time()
    rospy.loginfo(hello_str)

def clasificacion_1(objeto_form,objeto_color):
    if objeto_form == 'Rectangulo':
	if objeto_color == 'Rojo':
            subprocess.call(["rosrun","baxter_sim_examples","place11v.py"])
	    subprocess.call(["rosrun","baxter_sim_examples","YMCAStateMach_2.py"])
	if objeto_color == 'Azul':
	    subprocess.call(["rosrun","baxter_sim_examples","place11v.py"])
	    subprocess.call(["rosrun","baxter_sim_examples","YMCAStateMach_3.py"])
    else:
	if objeto_color == 'Verde':
            subprocess.call(["rosrun","baxter_sim_examples","place1v.py"])
	    subprocess.call(["rosrun","baxter_sim_examples","YMCAStateMach_7.py"]) 

def clasificacion_2(objeto_form,objeto_color):
    if objeto_form == 'Rectangulo':
	if objeto_color == 'Rojo':
            subprocess.call(["rosrun","baxter_sim_examples","place11v.py"])
	    subprocess.call(["rosrun","baxter_sim_examples","YMCAStateMach_5.py"])
	if objeto_color == 'Azul':
	    subprocess.call(["rosrun","baxter_sim_examples","place11v.py"])
	    subprocess.call(["rosrun","baxter_sim_examples","YMCAStateMach_6.py"])
    else:
	if objeto_color == 'Verde':
            subprocess.call(["rosrun","baxter_sim_examples","place1v.py"])
	    subprocess.call(["rosrun","baxter_sim_examples","YMCAStateMach_8.py"])  


if __name__ == '__main__':
    #talker()
    a=0
    subprocess.call(["rosrun","baxter_sim_examples","YMCAStateMach1.py"])
    
    while not rospy.is_shutdown():

    	find_obj = detector.image_to_initial_state()
    	rospy.init_node("image_to_initial_state", disable_signals=True, anonymous=True)
    	rospy.sleep(1)
    	find_obj_1 = find_obj.find_obj()

   	if find_obj_1 == 'Yes':

	    subprocess.call(["rosrun","baxter_sim_examples","pick1.py","-u"])
	    subprocess.call(["rosrun","baxter_sim_examples","YMCAStateMach_1v.py"])

            objeto_color = sense_p.image_to_initial_state()
            rospy.init_node("image_to_initial_state", disable_signals=True, anonymous=True)
            rospy.sleep(1)
            [objeto_color,objeto_form] = objeto_color.initial_color()
        
            clasificacion_1(objeto_form,objeto_color)
    	
	else:

	    subprocess.call(["rosrun","baxter_sim_examples","YMCAStateMach2.py"])
	
	find_obj = detector.image_to_initial_state()
    	rospy.init_node("image_to_initial_state", disable_signals=True, anonymous=True)
        rospy.sleep(1)
        find_obj_2 = find_obj.find_obj()

	if find_obj_2 == 'Yes':

            subprocess.call(["rosrun","baxter_sim_examples","pick2.py"])
	    subprocess.call(["rosrun","baxter_sim_examples","YMCAStateMach_4v.py"])
    
            objeto_color = sense_p.image_to_initial_state()
            rospy.init_node("image_to_initial_state", disable_signals=True, anonymous=True)
            rospy.sleep(1)
            [objeto_color,objeto_form] = objeto_color.initial_color()
    
            clasificacion_2(objeto_form,objeto_color)
    
    	else:
		
	    subprocess.call(["rosrun","baxter_sim_examples","YMCAStateMach1.py"])


