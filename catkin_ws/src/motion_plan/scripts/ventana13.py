#!/usr/bin/env python
# coding=utf-8

import rospy
import roslib
import sys
import os
#sys.path.append("/home/gabo/catkin_ws/src/motion_plan/scripts/mundo_v.py")
from Tkinter import *



    
global var   
var = 13
print(var)    

def pares():

    raiz.destroy()
    os.system('rosrun motion_plan pares13.py')
    
def impares():
    
    raiz.destroy()
    os.system('rosrun motion_plan impares13.py')


raiz= Tk()
raiz.title("Interfaz de usuario")
      

    
principal=Frame(raiz, width=550, height=450)
principal.pack()

titulo=Label(principal, text="Escuela Politécnica Nacional", fg="blue", font=("Arial", 30))
titulo.grid(row=0, column=1, padx=200, pady=0)

titulo=Label(principal, text="Aplicación de algoritmos con certificados de barrera para prevenir colisiones en sistemas tipo enjambre  ", fg="blue", font=("Arial", 20)) #aumentar esto
titulo.grid(row=1, column=1, padx=0, pady=0)

Ingreso=Label(principal, text="Estudiante: Gabriel E. Mena ", fg="Black", font=("Arial", 13),  padx=10, pady=10)
Ingreso.grid(row=0, column=1, sticky="ne")






imagen=PhotoImage(file="/home/gabo/catkin_ws/src/motion_plan/scripts/foto1.png")
Label(principal, image=imagen).grid(row=0, column=0,sticky="e")

Ingreso=Label(principal, text="Seleccione el obstáculo a ingresar", fg="Red", font=("Arial", 17))
Ingreso.grid(row=2, column=1,padx=0, pady=30)
Ingreso=Label(principal, text="Esfera de color blanco:", fg="Black", font=("Arial", 17),  padx=10, pady=10)
Ingreso.grid(row=3, column=1, sticky="w")
    
Ingreso=Label(principal, text="Cilindro de color rojo:", fg="Black", font=("Arial", 17), padx=10, pady=10)
Ingreso.grid(row=4, column=1, sticky="w")
    
    

botonObjeto1= Button(principal, text="Primer objeto", command=pares,  font=("Arial", 20))
botonObjeto1.grid(row=3, column=1)
imagen1=PhotoImage(file="/home/gabo/catkin_ws/src/motion_plan/scripts/esfera.png")
Label(principal, image=imagen1).grid(row=3, column=1,sticky="e")

botonObjeto2= Button(principal, text="Segundo objeto", command=impares, font=("Arial", 20))
botonObjeto2.grid(row=4, column=1)
imagen2=PhotoImage(file="/home/gabo/catkin_ws/src/motion_plan/scripts/cilindro.png")
Label(principal, image=imagen2).grid(row=4, column=1,sticky="e")


    
def main():
    
  rospy.init_node('ventana1',anonymous= True)
  raiz.mainloop()	
 
  
  rospy.spin()

if __name__ == '__main__':
  main()
