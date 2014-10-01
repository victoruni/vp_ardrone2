#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  
#  Чтение из файла и выполнение команд сценария для ardrone 2.0
#

import roslib; roslib.load_manifest('vp_ardrone2') 
import rospy
from std_msgs.msg import Empty
from ardrone_autonomy.msg import *
from geometry_msgs.msg import Twist


def controller(data):

    rospy.set_param("/vp_ardrone2/flag1",1);
    rospy.loginfo("STOP_ARDRONE")
    pub3=rospy.Publisher('cmd_vel', Twist)
    odom=Twist()
    odom.linear.x=0.0
    odom.linear.y=0.0
    odom.linear.z=0.0
    odom.angular.x=0.0
    odom.angular.y=0.0
    odom.angular.z=0.0
    pub3.publish(odom)


def listener():
   rospy.init_node('web_publisher_node2')
   sub = rospy.Subscriber("web_publisher2",Empty,controller)
   rospy.spin()

if __name__ == '__main__':
       try:
           listener()
       except rospy.ROSInterruptException: pass
       except KeyboardInterrupt:
		sys.exit(1)
