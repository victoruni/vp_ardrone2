#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  
#  Установка дополнительных параметров
#  для пользовательских фигур ardrone 2.0
#  получение данных из темы /ardrone/navdata
#  rotZ - угловое смещение по оси Z
#  altd - примерная высота в см
#

import roslib; roslib.load_manifest('vp_ardrone2') 
import rospy
from std_msgs.msg import String
from std_msgs.msg import Empty
from ardrone_autonomy.msg import Navdata

var_altd=0;
var_altd1=0;
var_rotZ=0;
var_rotZ1=0;

def controller(data):
    
    flag2=rospy.get_param("/vp_ardrone2/flag2")
    ####################### высота - движение вверх
    if int(var_altd1)==1 and int(data.altd) > int(var_altd):
       if flag2==0:
         rospy.set_param("/vp_ardrone2/flag2",1)
       #var_rotZ1=1
       #rospy.loginfo("****************var_altd=")
       #rospy.loginfo(int(var_altd))
       #rospy.loginfo("***************data.altd="+str(data.altd))
       #rospy.loginfo(int(var_altd))
       ####################### поворот #####################       
       if (abs(int(data.rotZ)) < abs(int(float(var_rotZ)))+10) and (abs(int(data.rotZ)) > abs(int(float(var_rotZ)))-10):
         rospy.set_param("/vp_ardrone2/flag2",2)
         rospy.loginfo(var_rotZ)
    ########### высота - движение вниз
    elif int(var_altd1)==2 and int(data.altd)<int(var_altd):
       if flag2==0:
         rospy.set_param("/vp_ardrone2/flag2",1)
       #var_rotZ1=1
       ####################### поворот #####################       
       if (abs(int(data.rotZ)) < abs(int(float(var_rotZ)))+10) and (abs(int(data.rotZ)) > abs(int(float(var_rotZ)))-10):
         rospy.set_param("/vp_ardrone2/flag2",2)
         rospy.loginfo(var_rotZ)
    else:
       pass
       #rospy.loginfo("data.altd="+str(data.altd))
       #rospy.loginfo("var_altd1="+str(var_altd1))
       #rospy.loginfo("var_altd="+str(var_altd))
 
    ####################### f3 #####################       
    #if (abs(int(data.rotZ)) > int(float(var_rotZ))) and (float(data.rotZ)>0.0):
    #     rospy.set_param("/vp_ardrone2/flag3",2)
    #     rospy.loginfo(var_rotZ)
    #elif (abs(int(data.rotZ)) > int(float(var_rotZ))) and (float(data.rotZ)<0.0):
    #     rospy.set_param("/vp_ardrone2/flag3",1)
    #     rospy.loginfo(var_rotZ)
    #else:
    #   pass
   
       

def controller2(data):
    
    global var_altd;
    global var_rotZ;
    global var_altd1;
    global var_rotZ1;

    Arr1=data.data.split(";")
    var_altd=Arr1[0];
    var_altd1=Arr1[1];
    var_rotZ=Arr1[2];
    var_rotZ1=Arr1[3];
    rospy.loginfo(var_altd)
    
    

def listener():
   rospy.init_node('vp_ardrone2_setparam_dop_node')
   sub1 = rospy.Subscriber("/ardrone/navdata",Navdata,controller)
   sub2 = rospy.Subscriber("/vp_ardrone2/control_param",String,controller2)
   rospy.spin()

if __name__ == '__main__':
       try:
           listener()
       except rospy.ROSInterruptException: pass
       except KeyboardInterrupt:
		sys.exit(1)
