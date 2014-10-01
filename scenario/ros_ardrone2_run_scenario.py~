#!/usr/bin/env python
#-*-coding:utf-8 -*-

# 
#  Слушатель ros_vp_ardrone2_sub_start
#  чтение сообщений из темы vp_ardrone2_sub_start
#  получение команды старта из WebSockets
#  для чтения и выполнения сценария команд для ardront 2.0
#  



import roslib; roslib.load_manifest('vp_ardrone2')
import rospy
import subprocess
import shlex

from ardrone_autonomy.msg import *
from ardrone_autonomy.srv import *
from std_msgs.msg import String
from std_msgs.msg import Empty
from std_msgs.msg import Int32
from geometry_msgs.msg import Twist


def controller(data):

    if(data.data>0):
      command = data.data
    if(command/100000==1):  # ArDrone 2.0
      ### приветствие
      rospy.loginfo("ArDrone 2.0")
      if((command%100000)/10000==1):  # привет - анимация 
        rospy.loginfo("привет")
        serv1=rospy.ServiceProxy('ardrone/setledanimation', LedAnim)
        res1=serv1(1,4,3);
        rospy.loginfo(res1)
        # параметры
      elif((command%100000)/10000==2):  # пока - анимация
        rospy.loginfo("пока")
        serv1=rospy.ServiceProxy('ardrone/setledanimation', LedAnim)
        res1=serv1(2,4,3);
        rospy.loginfo(res1)
      elif((command%100000)/10000==3):  # молодец - анимация
        rospy.loginfo("молодец")
        serv1=rospy.ServiceProxy('ardrone/setledanimation', LedAnim)
        res1=serv1(3,4,5);
        rospy.loginfo(res1)
      ### взлет, посадка
      elif((command%10000)/1000==1):  # взлет
        rospy.loginfo("взлет")
        pub1=rospy.Publisher('ardrone/takeoff', Empty)
        pub1.publish()
        # параметры
      elif((command%10000)/1000==2):  # посадка
        rospy.loginfo("посадка")
        pub2=rospy.Publisher('ardrone/land', Empty)
        pub2.publish()
      elif((command%10000)/1000==3):  # заснуть, сброс
        rospy.loginfo("заснуть")
        pub2=rospy.Publisher('ardrone/reset', Empty)
        pub2.publish()
      elif((command%10000)/1000==4):  # на базу
        rospy.loginfo("на базу!!!!")
      ### зависнуть

      ### dance анимация
      elif((command%1000)/100==9):  # полетная анимация
        rospy.loginfo("flight анимации - па !!!!")
        serv1=rospy.ServiceProxy('ardrone/setflightanimation',FlightAnim)
        res1=serv1((command%100)/10,0);
        rospy.loginfo(res1)
      

    elif(command/100000==2):  # iRobot
      rospy.loginfo("iRorot Robert")
      
def listener():
   rospy.init_node('ros_ardrone1_command')
   sub = rospy.Subscriber("ardrone1_command",Int32,controller)
   rospy.spin()
 
if __name__ == '__main__':
   listener()
   
