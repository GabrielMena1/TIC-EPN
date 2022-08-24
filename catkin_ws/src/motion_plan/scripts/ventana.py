#!/usr/bin/env python
# coding=utf-8

import argparse
import struct
import sys
import copy
#import sys
#sys.path.append("/home/gabo/catkin_ws/src/motion_plan/scripts/ventana")



import rospy
import rospkg
import os
from gazebo_msgs.srv import (
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
from std_msgs.msg import String




#import sys
#sys.path.append("/home/gabo/catkin_ws/src/motion_plan/scripts/mundo_v.py")
from Tkinter import *


raiz= Tk()
raiz.title("Interfaz de usuario")

valor1x=IntVar()
valor1y=IntVar()
    
global var   
var = 1
print(var)    
def ingresovalor1x():
    global var
    var= var+1  
    
    if var == 2:
        def load_gazebo_models(block2_pose=Pose(position=Point(x=valor1x.get(), y= valor1y.get(), z=1)),
                               block2_reference_frame="world"):
    # Get Models' Path
            model_path = rospkg.RosPack().get_path('robot_description')+"/models/"
    
    # Load sphere1 URDF
            block2_xml = ''
            with open (model_path + "ball/model.urdf", "r") as block2_file:
                block2_xml=block2_file.read().replace('\n', '')

    

    # Spawn Block2 URDF
            rospy.wait_for_service('/gazebo/spawn_urdf_model')
            try:
                spawn_urdf = rospy.ServiceProxy('/gazebo/spawn_urdf_model', SpawnModel)
                resp_urdf = spawn_urdf("ball", block2_xml, "/",
                                       block2_pose, block2_reference_frame)
            except rospy.ServiceException, e:
                rospy.logerr("Spawn URDF service call failed: {0}".format(e))        

	#def main():
	pub = rospy.Publisher('chatter', String, queue_size=10)
        rospy.init_node('mundo',anonymous= True)
        load_gazebo_models()
        print (valor1x.get(),valor1y.get(),var)
        rospy.ROSInterruptException  
    elif var == 3:
        os.system('rosrun motion_plan mundov2.py')
    

        print (valor1x.get(),valor1y.get(),var)
        
    else:
        print (var)
    
principal=Frame(raiz, width=550, height=450)
principal.pack()

titulo=Label(principal, text="Escuela Politécnica Nacional", fg="blue", font=("Arial", 40))
#titulo.place(x=0, y=10)
titulo.grid(row=0, column=1, padx=200, pady=10)
imagen=PhotoImage(file="/home/gabo/catkin_ws/src/motion_plan/scripts/foto1.png")
#Label(principal, image=imagen).place(x=0, y=0)
Label(principal, image=imagen).grid(row=0, column=0)

Ingreso=Label(principal, text="Ingreso de datos obstáculos", fg="Red", font=("Arial", 20))
Ingreso.grid(row=1, column=1)
Ingreso=Label(principal, text="Coordenada x Objeto 1", fg="Black", font=("Arial", 20))
Ingreso.grid(row=2, column=0)
cuadro1x=Entry(principal, textvariable=valor1x)
cuadro1x.grid(row=2, column=1)


Ingreso=Label(principal, text="Coordenada y Objeto 1", fg="Black", font=("Arial", 20))
Ingreso.grid(row=3, column=0)
cuadro1y=Entry(principal, textvariable=valor1y)
cuadro1y.grid(row=3, column=1)


Ingreso=Label(principal, text="Coordenada x Objeto 2", fg="Black", font=("Arial", 20))
Ingreso.grid(row=4, column=0)
cuadro2x=Entry(principal)
cuadro2x.grid(row=4, column=1)

Ingreso=Label(principal, text="Coordenada y Objeto 2", fg="Black", font=("Arial", 20))
Ingreso.grid(row=5, column=0)
cuadro2y=Entry(principal)
cuadro2y.grid(row=5, column=1)


botonObjeto1= Button(raiz, text="Cargar Objeto 1", command=ingresovalor1x)
botonObjeto1.pack()


botonObjeto2= Button(raiz, text="Cargar Objeto 2")
botonObjeto2.pack()

raiz.mainloop()
