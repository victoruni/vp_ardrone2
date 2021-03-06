#!/usr/bin/env python
#-*-coding:utf-8 -*-
#
#  джойстик - для аварийной посадки или зависания
#
 
import roslib; roslib.load_manifest('vp_ardrone2')
import rospy
import subprocess
import shlex
import time
 
from ardrone_autonomy.msg import *
from ardrone_autonomy.srv import *
from sensor_msgs.msg import Joy
from std_msgs.msg import String
from std_msgs.msg import Empty
from std_msgs.msg import Int32
from geometry_msgs.msg import Twist
import std_srvs.srv
  
 
def controller(data):
    # проверка takeoff - кнопка start/10
    if(data.buttons[9]==1):  # взлет
        rospy.loginfo("взлет")
        pub1=rospy.Publisher('ardrone/takeoff', Empty)
        pub1.publish()
        time.sleep(1)
    elif(data.buttons[8]==1):  # посадка- кнопка back/9
        rospy.loginfo("посадка")
        pub1=rospy.Publisher('ardrone/land', Empty)
        pub1.publish()
        time.sleep(1)
    elif(data.buttons[5]==1):  # посадка- кнопка RB/6
        rospy.loginfo("посадка")
        pub1=rospy.Publisher('ardrone/land', Empty)
        pub1.publish()
        rospy.set_param("/vp_ardrone2/flag2",1)
        time.sleep(1)
    elif(data.buttons[4]==1):  # flattrim- кнопка RB/5
        rospy.loginfo("flattrim")
        rospy.set_param("/vp_ardrone2/flag2",1)
        serv1=rospy.ServiceProxy('ardrone/flattrim',std_srvs.srv.Empty)
        res1=serv1();
    else:             # другие клавиши
        pass
              
    #  
    #rospy.loginfo(data.axes)
    #rospy.loginfo(data.buttons)   
       
def listener():
   rospy.init_node('vp_ardrone2_joy_node') 
   rospy.loginfo("vp_ardrone2_joy - OK!")   
   if not rospy.has_param("/vp_ardrone2/flag2"):
     rospy.set_param("/vp_ardrone2/flag2",0) 
   sub = rospy.Subscriber("joy",Joy,controller)
   rospy.spin()
  
if __name__ == '__main__':
   listener()
