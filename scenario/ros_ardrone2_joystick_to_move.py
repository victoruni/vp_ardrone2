#!/usr/bin/env python
#-*-coding:utf-8 -*-



import roslib; roslib.load_manifest('vp_ardrone1')
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


def controller(data):

    # проверка takeoff - кнопка start/10
    if(data.buttons[7]==1):  # взлет
        rospy.loginfo("взлет")
        pub1=rospy.Publisher('ardrone/takeoff', Empty)
        pub1.publish()
        time.sleep(1)
    elif(data.buttons[6]==1):  # посадка- кнопка back/9
        rospy.loginfo("посадка")
        pub1=rospy.Publisher('ardrone/land', Empty)
        pub1.publish()
        time.sleep(1)
    elif(data.buttons[1]==1):  # следующая led анимация - кнопка B2
        num1=rospy.get_param("joystick_num1")
        num1=min(num1+1,13)   # 0...13 
        rospy.set_param("joystick_num1",num1)
        serv1=rospy.ServiceProxy('ardrone/setledanimation', LedAnim)
        res1=serv1(num1,1,5);
        rospy.loginfo("next led анимация"+str(num1))
        rospy.loginfo(res1)
        time.sleep(1)
    elif(data.buttons[0]==1):  # предыдущая led анимация - кнопка A1
        num1=rospy.get_param("joystick_num1")
        num1=max(num1-1,0)   # 0...13 
        rospy.set_param("joystick_num1",num1)
        serv1=rospy.ServiceProxy('ardrone/setledanimation', LedAnim)
        res1=serv1(num1,1,5);
        rospy.loginfo("prev led анимация"+str(num1))
        rospy.loginfo(res1)
        time.sleep(1)

    elif(data.buttons[5]==1):  # завис - кнопка RB6
        pub3=rospy.Publisher('cmd_vel', Twist)
        odom=Twist()
        odom.linear.x=0.0
        odom.linear.y=0.0
        odom.linear.z=0.0
        odom.angular.x=0.0
        odom.angular.y=0.0
        odom.angular.z=0.0
        pub3.publish(odom)
        rospy.loginfo("завис!!!!")
        rospy.set_param("ardrone1_digit",[[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0],         [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]]);
        time.sleep(1)

    elif(data.buttons[3]==1):  # следующая полетная анимация - кнопка Y4
        num2=rospy.get_param("joystick_num2")
        num2=min(num2+1,14)   # 0...18 (ограничено flip)
        rospy.set_param("joystick_num2",num2)
        serv1=rospy.ServiceProxy('ardrone/setflightanimation',FlightAnim)
        res1=serv1(num2,0);
        rospy.loginfo("next полетная анимация"+str(num2))
        rospy.loginfo(res1)
        time.sleep(1)
    elif(data.buttons[2]==1):  # предыдущая полетная анимация - кнопка X3
        num2=rospy.get_param("joystick_num2")
        num2=max(num2-1,0)   # 0...18 (ограничено flip)
        rospy.set_param("joystick_num2",num2)
        serv1=rospy.ServiceProxy('ardrone/setflightanimation',FlightAnim)
        res1=serv1(num2,0);
        rospy.loginfo("prev - полетная анимация"+str(num2))
        rospy.loginfo(res1)
        time.sleep(1)

    elif(data.axes[0]!=0.0 or data.axes[1]!=0.0 or data.axes[3]!=0.0 or data.axes[4]!=0.0):  # управление
        pub3=rospy.Publisher('cmd_vel', Twist)
        joistick_prev_odom=rospy.get_param("joystick_prev_odom")
        odom=Twist()
        odom.linear.x=data.axes[1]
        odom.linear.y=data.axes[0]
        odom.linear.z=data.axes[4]*(-1)
        odom.angular.x=0.0
        odom.angular.y=0.0
        odom.angular.z=data.axes[3]
        pub3.publish(odom)
        joistick_prev_odom[0]=data.axes[0]
        joistick_prev_odom[1]=data.axes[1]
        joistick_prev_odom[2]=data.axes[2]
        joistick_prev_odom[3]=data.axes[3]
        joistick_prev_odom[4]=data.axes[4]
        joistick_prev_odom[5]=data.axes[5]
        direction=""
        if(data.axes[1]>0.0):
           direction="forward"
        if(data.axes[1]<0.0):
           direction="back"
        if(data.axes[0]>0.0):
           direction="left"
        if(data.axes[0]<0.0):
           direction="right"
        if(data.axes[4]>0.0):
           direction="up"
        if(data.axes[4]<0.0):
           direction="down"
        if(data.axes[3]>0.0):
           direction="turn left"
        if(data.axes[3]<0.0):
           direction="turn right"
        rospy.set_param("joystick_prev_odom",joistick_prev_odom)
        rospy.set_param("ardrone1_digit",[[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0],         [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]]);
        rospy.loginfo("движение!!!!"+"  "+direction)
    else:             # останов джойстиками
        joistick_prev_odom=rospy.get_param("joystick_prev_odom")
        odom=Twist()
        if(joistick_prev_odom[0]!=data.axes[0] or joistick_prev_odom[1]!=data.axes[1] or 
           joistick_prev_odom[3]!=data.axes[3] or joistick_prev_odom[4]!=data.axes[4]):
             pub3=rospy.Publisher('cmd_vel', Twist)
             odom.linear.x=0.0
             odom.linear.y=0.0
             odom.linear.z=0.0
             odom.angular.x=0.0
             odom.angular.y=0.0
             odom.angular.z=0.0
             pub3.publish(odom)
             joistick_prev_odom[0]=0.0
             joistick_prev_odom[1]=0.0
             joistick_prev_odom[2]=0.0
             joistick_prev_odom[3]=0.0
             joistick_prev_odom[4]=0.0
             joistick_prev_odom[5]=0.0
             rospy.set_param("joystick_prev_odom",joistick_prev_odom)
             rospy.loginfo("останов по джойстику!!!!")
             rospy.set_param("ardrone1_digit",[[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0],         [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]]);
            
    #  
    #rospy.loginfo(data.axes)
    #rospy.loginfo(data.buttons)   
      
def listener():
   rospy.init_node('joyctick')
   if not rospy.has_param("joystick_num1"):
     rospy.set_param("joystick_num1",0) 
   if not rospy.has_param("joystick_num2"):
     rospy.set_param("joystick_num2",0) 
   if not rospy.has_param("joystick_prev_odom"):
     rospy.set_param("joystick_prev_odom",[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]) 
   if not rospy.has_param("ardrone1_digit"):
     rospy.set_param("ardrone1_digit",[[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0],         [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]]);
   
   sub = rospy.Subscriber("joy",Joy,controller)
   rospy.spin()
 
if __name__ == '__main__':
   listener()
   
