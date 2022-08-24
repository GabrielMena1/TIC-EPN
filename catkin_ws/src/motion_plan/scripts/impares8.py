#!/usr/bin/env python
# coding=utf-8

import argparse
import struct
import sys
import copy
#import sys
import rospy
import rospkg

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

#sys.path.append("/home/gabo/catkin_ws/src/motion_plan/scripts/ventana")
#from ventana import (valor1x,valor1y)


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

from Tkinter import *


raiz= Tk()
raiz.title("Interfaz de usuario")

global valor1x,valor1y
valor1x=IntVar()
valor1y=IntVar()
comentario=StringVar()    
global var   
var = 2
   
def ingresovalor1x():
    global var,valor1x,valor1y
      
    
    if valor1x.get() > -9 and valor1x.get() < 9 and valor1y.get() > -9 and valor1y.get() < 9 and var==2: 
        def load_gazebo_models(block2_pose=Pose(position=Point(x=valor1x.get(), y= valor1y.get(), z=2)),
                               block2_reference_frame="world"):
  
            model_path = rospkg.RosPack().get_path('robot_description')+"/models/"
    
    
            block2_xml = ''
            with open (model_path + "ball/pista.urdf", "r") as block2_file:
                block2_xml=block2_file.read().replace('\n', '')

    
            rospy.wait_for_service('/gazebo/spawn_urdf_model')
            try:
                spawn_urdf = rospy.ServiceProxy('/gazebo/spawn_urdf_model', SpawnModel)
                resp_urdf = spawn_urdf("CILI9", block2_xml, "/",
                                       block2_pose, block2_reference_frame)
            except rospy.ServiceException, e:
                rospy.logerr("Spawn URDF service call failed: {0}".format(e))        

        rospy.init_node('ObjetoCreadoSI')
        load_gazebo_models()
        comentario.set("Objeto ingresado correctamente")
        print (valor1x.get(),valor1y.get(),var)
        var = 3
    elif valor1x.get() > -9 and valor1x.get() < 9 and valor1y.get() > -9 and valor1y.get() < 9 and var==3:
        comentario.set("Crear nuevo objeto")   
    else:
        comentario.set("Coordenadas incorrectas")
        print ("Coordenada incorrecta")	
 
def otro():
    raiz.destroy()
    os.system('rosrun motion_plan ventana9.py')
      
    
    
principal=Frame(raiz, width=550, height=450)
principal.pack()

titulo=Label(principal, text="Escuela Politécnica Nacional", fg="blue", font=("Arial", 30))

titulo.grid(row=0, column=1, padx=200, pady=0)
imagen=PhotoImage(file="/home/gabo/catkin_ws/src/motion_plan/scripts/foto1.png")
Label(principal, image=imagen).grid(row=0, column=0)


titulo=Label(principal, text="Aplicación de algoritmos con certificados de barrera para prevenir colisiones en sistemas tipo enjambre  ", fg="blue", font=("Arial", 20)) #aumentar esto
titulo.grid(row=1, column=1, padx=0, pady=0)

Ingreso=Label(principal, text="Estudiante: Gabriel E. Mena", fg="Black", font=("Arial", 13),  padx=10, pady=10)
Ingreso.grid(row=0, column=1, sticky="ne")


Ingreso=Label(principal, text="Ingreso de datos obstáculos", fg="Red", font=("Arial", 17))
Ingreso.grid(row=2, column=1,pady=28)
Ingreso=Label(principal, text="Coordenada x:", fg="Black", font=("Arial", 17), pady=10)
Ingreso.grid(row=4, column=1,sticky="w")
cuadro1x=Entry(principal, textvariable=valor1x,font=("Arial", 17))
cuadro1x.grid(row=4, column=1)

Comentario=Label(principal, text="Comentario", fg="Black", font=("Arial", 17))
Comentario.grid(row=4, column=1,sticky="e",padx=200)
cuadro2x=Entry(principal, textvariable=comentario, width=30,font=("Arial", 17))
cuadro2x.grid(row=5, column=1,sticky="e", padx=20, pady=30)


Ingreso=Label(principal, text="Coordenada y:", fg="Black", font=("Arial", 17), pady=10)
Ingreso.grid(row=5, column=1,sticky="w")
cuadro1y=Entry(principal, textvariable=valor1y,font=("Arial", 17))
cuadro1y.grid(row=5, column=1)


botonObjeto1= Button(principal, text="Cargar Objeto 2", command=ingresovalor1x, font=("Arial", 20))
botonObjeto1.grid(row=6, column=1)


Ingreso=Label(principal, text="        ", fg="Black", font=("Arial", 17), pady=10)
Ingreso.grid(row=5, column=1,sticky="e")


botonObjeto2= Button(principal, text="Nuevo Objeto", command=otro,  font=("Arial", 20))
botonObjeto2.grid(row=6, column=1,sticky="e", padx=150)



Instrucciones=Label(principal, text="Instrucciones: Ingresar valores enteros dentro del rango [-8,8] para las siguientes coordenadas.", fg="Black", font=("Arial", 15), pady=10)
Instrucciones.grid(row=3, column=1)


raiz.mainloop()
