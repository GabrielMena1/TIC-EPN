#!/usr/bin/env python


import argparse
import struct
import sys
import copy
import sys
sys.path.append("/home/gabo/catkin_ws/src/motion_plan/scripts/ventana")
from ventana import (valor1x,valor1y)


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

#def llamado():
  #  from ventana import var
   # global var
   # print (var)
   
def load_gazebo_models(block2_pose=Pose(position=Point(x=valor1x.get(), y= valor1y.get(), z=1)),
                       block2_reference_frame="world"):
    # Get Models' Path
    model_path = rospkg.RosPack().get_path('robot_description')+"/models/"
    
    # Load sphere1 URDF
    block2_xml = ''
    with open (model_path + "ball/pista.urdf", "r") as block2_file:
        block2_xml=block2_file.read().replace('\n', '')

    

    # Spawn Block2 URDF
    rospy.wait_for_service('/gazebo/spawn_urdf_model')
    try:
        spawn_urdf = rospy.ServiceProxy('/gazebo/spawn_urdf_model', SpawnModel)
        resp_urdf = spawn_urdf("ball2", block2_xml, "/",
                               block2_pose, block2_reference_frame)
    except rospy.ServiceException, e:
        rospy.logerr("Spawn URDF service call failed: {0}".format(e))

  

def main():
    rospy.init_node("mundo2")
    # Load Gazebo Models via Spawning Services
    # Note that the models reference is the /world frame
    # and the IK operates with respect to the /base frame
   # llamado()
    load_gazebo_models()
    #llamado()
    # Remove models from the scene on shutdown
    #rospy.on_shutdown(delete_gazebo_models)

    # Wait for the All Clear from emulator startup
    #rospy.wait_for_message("/robot/sim/started", Empty)
    

    #while not rospy.is_shutdown():
   #     print("\nObjetos en escena...")
    #    #pnp.pick(block_poses[idx])
    #    print("\nPlacing...")
    #    #idx = (idx+1) % len(block_poses)
    #    #pnp.place(block_poses[idx])
   # return 0


if __name__ == '__main__':
    sys.exit(main())
