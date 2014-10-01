#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  
#  Чтение из файла и выполнение команд сценария для ardrone 2.0
#

import roslib; roslib.load_manifest('vp_ardrone2') 
import rospy
from std_msgs.msg import Float32
from std_msgs.msg import String
from std_msgs.msg import Empty
import std_srvs.srv
from vp_ardrone2.srv import *
from ardrone_autonomy.msg import Navdata
from ardrone_autonomy.msg import *
from ardrone_autonomy.srv import *
import subprocess
import os
import math
from datetime import *
from geometry_msgs.msg import Twist

PATH_SCENARIO="/home/petin/catkin_ws/src/vp_ardrone2/scenario/"
FREQ=0.02
LZ3=0.05

def controller(data):

    rospy.set_param("/vp_ardrone2/flag1",0);
    rospy.set_param("/vp_ardrone2/flag2",0);
    rospy.set_param("/vp_ardrone2/flag3",0);

    #file1=open("scenario/"+data.data,"r")
    file1=open(PATH_SCENARIO+data.data,"r")
  
    # заполнение массива из файла
    Arr1=[]
    for stroka in file1.readlines():
      Arr1.append(stroka.split(";"))
    # перебор списка команд
    pub99=rospy.Publisher('/vp2_control',Float32)
    pub0=rospy.Publisher('/web_subscriber',String)
    for i in range(len(Arr1)):
      #for j in range(len(Arr1[i])):
        # TEST - вывод массива из файла на экран
        #print Arr1[i][j]
      # commands
      pub4=rospy.Publisher('vp_ardrone2/control_param', String)
      pub4.publish("0;0;0.0;0")
      pub0.publish(str(i))
      rospy.loginfo("command="+str(i))
      flag1=rospy.get_param("/vp_ardrone2/flag1");
      flag3=rospy.get_param("/vp_ardrone2/flag3");
      rospy.set_param("/vp_ardrone2/flag2",0);
      ######################  start  ############################
      if(Arr1[i][0]=='start' and flag1==0):  # start
        rospy.loginfo("start")
        serv1=rospy.ServiceProxy('ardrone/flattrim',std_srvs.srv.Empty)
        res1=serv1();
        rospy.sleep(1.0*float(Arr1[i][1]))
      ######################  wait  ############################
      elif(Arr1[i][0]=='wait' and flag1==0):  # wait
        rospy.loginfo("wait")
        rospy.sleep(1.0*float(Arr1[i][1]))
      ######################  takeoff ############################
      elif(Arr1[i][0]=='takeoff' and flag1==0):  # takeoff
        rospy.loginfo("takeoff")
        pub1=rospy.Publisher('ardrone/takeoff', Empty)
        pub1.publish()
        #pub1.publish()
        rospy.sleep(1.0*float(Arr1[i][1]))
      ######################  land  ############################
      elif(Arr1[i][0]=='land' and flag1==0):  # land
        rospy.loginfo("land")
        pub1=rospy.Publisher('ardrone/land', Empty)
        pub1.publish()
        rospy.sleep(1.0*float(Arr1[i][1]))
      ######################  PAUSE ############################
      elif(Arr1[i][0]=='pause' and flag1==0):  # ledanimation
        rospy.loginfo("pause")
        rospy.sleep(1.0*float(Arr1[i][1]))
      ######################  led  ############################
      elif(Arr1[i][0]=='led' and flag1==0):  # ledanimation
        rospy.loginfo("ledanim")
        serv1=rospy.ServiceProxy('ardrone/setledanimation', LedAnim)
        res1=serv1(int(Arr1[i][2]),float(Arr1[i][3]),int(Arr1[i][4]));
        rospy.loginfo(res1)
        rospy.sleep(1.0*float(Arr1[i][1]))
      ######################  fly  ############################
      elif(Arr1[i][0]=='fly' and flag1==0):  # flyanimation
        rospy.loginfo("flyanim")
        serv1=rospy.ServiceProxy('ardrone/setflightanimation',FlightAnim)
        res1=serv1(int(Arr1[i][2]),0);
        rospy.loginfo(res1)
        rospy.sleep(1.0*float(Arr1[i][1]))
      ######################  cmd_vel  ############################
      elif(Arr1[i][0]=='cmd_vel' and flag1==0):  # cmd_vel
        rospy.loginfo("cmd_vel")
        str_control=Arr1[i][6]+";"+Arr1[i][7]+";"+Arr1[i][8]+";"+Arr1[i][9]
        pub4=rospy.Publisher('vp_ardrone2/control_param', String)
        pub4.publish(str_control)
        d1=datetime.now()
        s=math.floor(float(Arr1[i][1]))
        rospy.loginfo(s)
        mcs=(float(Arr1[i][1])-s)*1000000
        rospy.loginfo(mcs)
        d2=datetime.now()+timedelta(seconds=int(s),microseconds=int(mcs))
        rospy.loginfo(d1)
        pub3=rospy.Publisher('cmd_vel', Twist)
        odom=Twist()
        ts=float(Arr1[i][1])
        count=0
        while d2>d1:
          d1=datetime.now()
          k=1.0
          #if FREQ*count/ts>=0.8:
          #   k=k*((1-FREQ*count/ts)*5)
          #odom.linear.x=float(Arr1[i][2])*k
          #odom.linear.y=float(Arr1[i][3])*k
          odom.linear.x=0.0
          odom.linear.y=0.0
          # проверка высоты
          flag2=rospy.get_param("/vp_ardrone2/flag2")
          if Arr1[i][4]>0 and flag2<1:
            odom.linear.z=float(Arr1[i][4])
          else:
            odom.linear.z=0.0
          odom.angular.x=0.0
          odom.angular.y=0.0
          odom.angular.z=float(Arr1[i][5])
          pub3.publish(odom)
          rospy.sleep(FREQ)
          count=count+1
        odom.linear.x=0.0
        odom.linear.y=0.0
        odom.linear.z=0.0
        odom.angular.x=0.0
        odom.angular.y=0.0
        odom.angular.z=0.0
        pub3.publish(odom)
        rospy.set_param("/vp_ardrone2/flag2",0);
        rospy.loginfo(d1)
        rospy.loginfo(d2)
      ######################  userfly1 - доводка до данного угла 
      elif(Arr1[i][0]=='userfly1' and flag1==0):  # userfly1
        rospy.loginfo("userfly1")
        #str_control=Arr1[i][6]+";"+Arr1[i][7]+";0;0"
        str_control=Arr1[i][6]+";"+Arr1[i][7]+";"+Arr1[i][8]+";"+Arr1[i][9]
        pub4=rospy.Publisher('vp_ardrone2/control_param', String)
        pub4.publish(str_control)
        d1=datetime.now()
        s=math.floor(float(Arr1[i][1]))
        rospy.loginfo(s)
        mcs=(float(Arr1[i][1])-s)*1000000
        rospy.loginfo(mcs)
        d2=datetime.now()+timedelta(seconds=int(s),microseconds=int(mcs))
        rospy.loginfo(d1)
        pub3=rospy.Publisher('cmd_vel', Twist)
        odom=Twist()
        ts=float(Arr1[i][1])
        count=0
        while d2>d1:
          d1=datetime.now()
          k=1.0
          #if FREQ*count/ts>=0.8:
          #   k=k*((1-FREQ*count/ts)*5)
          odom.linear.x=0.0
          odom.linear.y=0.0
          # проверка высоты
          flag2=rospy.get_param("/vp_ardrone2/flag2")
          if flag2==0:
            odom.linear.z=0.0
            odom.angular.z=0.0
          elif flag2==1:
            #odom.linear.z=float(Arr1[i][4])/10
            odom.linear.z=0.0
            odom.angular.z=0.1
          else:
            odom.linear.z=0.0
            odom.angular.z=0.0
          odom.angular.x=0.0
          odom.angular.y=0.0
          pub3.publish(odom)
          rospy.sleep(FREQ)
          count=count+1
        odom.linear.x=0.0
        odom.linear.y=0.0
        odom.linear.z=0.0
        odom.angular.x=0.0
        odom.angular.y=0.0
        odom.angular.z=0.0
        pub3.publish(odom)
        rospy.set_param("/vp_ardrone2/flag2",0);
        rospy.loginfo(d1)
        rospy.loginfo(d2)
      ######################  userfly2 - поднятие-опускание с поворотом 
      elif(Arr1[i][0]=='userfly2' and flag1==0):  # userfly2
        rospy.loginfo("userfly2")
        #str_control=Arr1[i][6]+";"+Arr1[i][7]+";0;0"
        str_control=Arr1[i][6]+";"+Arr1[i][7]+";"+Arr1[i][8]+";"+Arr1[i][9]
        pub4=rospy.Publisher('vp_ardrone2/control_param', String)
        pub4.publish(str_control)
        d1=datetime.now()
        s=math.floor(float(Arr1[i][1]))
        rospy.loginfo(s)
        mcs=(float(Arr1[i][1])-s)*1000000
        rospy.loginfo(mcs)
        d2=datetime.now()+timedelta(seconds=int(s),microseconds=int(mcs))
        rospy.loginfo(d1)
        pub3=rospy.Publisher('cmd_vel', Twist)
        odom=Twist()
        ts=float(Arr1[i][1])
        count=0
        while d2>d1:
          d1=datetime.now()
          k=1.0
          #if FREQ*count/ts>=0.8:
          #   k=k*((1-FREQ*count/ts)*5)
          odom.linear.x=0.0
          odom.linear.y=0.0
          # проверка высоты
          flag2=rospy.get_param("/vp_ardrone2/flag2")
          if flag2==0:
            odom.linear.z=float(Arr1[i][4])
            odom.angular.z=float(Arr1[i][5])
          #elif flag2==1:
          #  #rospy.set_param("/vp_ardrone2/flag2",2)
          #  str_control="0;0;"+Arr1[i][8]+";"+Arr1[i][9]
          #  pub4=rospy.Publisher('vp_ardrone2/control_param', String)
          #  pub4.publish(str_control)
          #  rospy.set_param("/vp_ardrone2/flag2",2)
          #elif flag2==1:
          #  #odom.linear.z=float(Arr1[i][4])/10
          #  odom.linear.z=0.0
          #  odom.angular.z=0.1
          else:
            odom.linear.z=0.0
            odom.angular.z=0.0
          odom.angular.x=0.0
          odom.angular.y=0.0
          pub3.publish(odom)
          rospy.sleep(FREQ)
          count=count+1
        odom.linear.x=0.0
        odom.linear.y=0.0
        odom.linear.z=0.0
        odom.angular.x=0.0
        odom.angular.y=0.0
        odom.angular.z=0.0
        pub3.publish(odom)
        rospy.set_param("/vp_ardrone2/flag2",0);
        rospy.loginfo(d1)
        rospy.loginfo(d2)
      ######################  userfly3  ############################
      elif(Arr1[i][0]=='userfly3' and flag1==0):  # userfly3
        rospy.loginfo("userfly3")    
        flag31=0
        lz=float(Arr1[i][5])
        str_control=Arr1[i][6]+";"+Arr1[i][7]+";"+Arr1[i][8]+";"+Arr1[i][9]
        pub4=rospy.Publisher('vp_ardrone2/control_param', String)
        pub4.publish(str_control)
        d1=datetime.now()
        s=math.floor(float(Arr1[i][1]))
        rospy.loginfo(s)
        mcs=(float(Arr1[i][1])-s)*1000000
        rospy.loginfo(mcs)
        d2=datetime.now()+timedelta(seconds=int(s),microseconds=int(mcs))
        rospy.loginfo(d1)
        pub3=rospy.Publisher('cmd_vel', Twist)
        odom=Twist()
        ts=float(Arr1[i][1])
        count=0
        rospy.set_param("/vp_ardrone2/flag3",1);
        while d2>d1:
          d1=datetime.now()
          k=1.0
          #if FREQ*count/ts>=0.8:
          #   k=k*((1-FREQ*count/ts)*5)
          odom.linear.x=0.0
          odom.linear.y=0.0
          # проверка высоты
          flag2=rospy.get_param("/vp_ardrone2/flag2")
          flag3=rospy.get_param("/vp_ardrone2/flag3")
          if flag2==0:
            odom.linear.z=float(Arr1[i][4])
            if flag3==1:
               lz=float(Arr1[i][5])
            elif flag3==2:
               lz=float(Arr1[i][5])*(-1.0)
            else:
               pass
	    odom.angular.z=lz
            pub99.publish(lz);
          #elif flag2==1:
          #  rospy.set_param("/vp_ardrone2/flag2",2)
          #  #str_control="0;0;"+Arr1[i][8]+";"+Arr1[i][9]
          #  str_control="0;0;0;0"
          #  pub4=rospy.Publisher('vp_ardrone2/control_param', String)
          #  pub4.publish(str_control)
          #  odom.linear.z=0.0
          #  odom.angular.z=0.0
          else:
            odom.linear.z=0.0
            odom.angular.z=0.0
          odom.angular.x=0.0
          odom.angular.y=0.0
          #odom.angular.z=float(Arr1[i][5])
          pub3.publish(odom)
          rospy.sleep(FREQ)
          count=count+1
        odom.linear.x=0.0
        odom.linear.y=0.0
        odom.linear.z=0.0
        odom.angular.x=0.0
        odom.angular.y=0.0
        odom.angular.z=0.0
        pub3.publish(odom)
        rospy.set_param("/vp_ardrone2/flag2",0);
        rospy.set_param("/vp_ardrone2/flag3",0);
        rospy.loginfo(d1)
        rospy.loginfo(d2)
      ######################  userfly4  ############################
      elif(Arr1[i][0]=='userfly4' and flag1==0):  # userfly4
        rospy.loginfo("userfly4")
        #str_control=Arr1[i][6]+";"+Arr1[i][7]+";0;0"
        str_control=Arr1[i][6]+";"+Arr1[i][7]+";"+Arr1[i][8]+";"+Arr1[i][9]
        pub4=rospy.Publisher('vp_ardrone2/control_param', String)
        pub4.publish(str_control)
        d1=datetime.now()
        s=math.floor(float(Arr1[i][1]))
        rospy.loginfo(s)
        mcs=(float(Arr1[i][1])-s)*1000000
        rospy.loginfo(mcs)
        d2=datetime.now()+timedelta(seconds=int(s),microseconds=int(mcs))
        rospy.loginfo(d1)
        pub3=rospy.Publisher('cmd_vel', Twist)
        odom=Twist()
        ts=float(Arr1[i][1])
        count=0
        while d2>d1:
          d1=datetime.now()
          k=1.0
          #if FREQ*count/ts>=0.8:
          #   k=k*((1-FREQ*count/ts)*5)
          odom.linear.x=0.0
          odom.linear.y=0.0
          # проверка высоты
          flag2=rospy.get_param("/vp_ardrone2/flag2")
          odom.linear.z=0.0
          odom.angular.z=float(Arr1[i][5])
          odom.angular.x=0.0
          odom.angular.y=0.0
          pub3.publish(odom)
          rospy.sleep(FREQ)
          count=count+1
        odom.linear.x=0.0
        odom.linear.y=0.0
        odom.linear.z=0.0
        odom.angular.x=0.0
        odom.angular.y=0.0
        odom.angular.z=0.0
        pub3.publish(odom)
        rospy.set_param("/vp_ardrone2/flag2",0);
        rospy.loginfo(d1)
        rospy.loginfo(d2)
      ######################  userfly5 - эмуляция 13 #######################
      elif(Arr1[i][0]=='userfly5' and flag1==0):  # userfly2
        rospy.loginfo("userfly5")
        #str_control=Arr1[i][6]+";"+Arr1[i][7]+";0;0"
        str_control=Arr1[i][6]+";"+Arr1[i][7]+";"+Arr1[i][8]+";"+Arr1[i][9]
        pub4=rospy.Publisher('vp_ardrone2/control_param', String)
        pub4.publish(str_control)
        d1=datetime.now()
        s=math.floor(float(Arr1[i][1]))
        rospy.loginfo(s)
        mcs=(float(Arr1[i][1])-s)*1000000
        rospy.loginfo(mcs)
        d2=datetime.now()+timedelta(seconds=int(s),microseconds=int(mcs))
        rospy.loginfo(d1)
        pub3=rospy.Publisher('cmd_vel', Twist)
        odom=Twist()
        ts=float(Arr1[i][1])
        count=0
        flag5=5
        vv=float(Arr1[i][3])
        while flag5<7:
          d1=datetime.now()
          k=1.0
          #if FREQ*count/ts>=0.8:
          #   k=k*((1-FREQ*count/ts)*5)
          odom.linear.x=0.0
          odom.linear.y=0.0
          # проверка высоты
          flag2=rospy.get_param("/vp_ardrone2/flag2")
          if flag5==0:
               count=count+1
               if count>15:
                 count=0
                 flag5=1
                 pub99.publish(float(1.0));
               odom.linear.x=float(Arr1[i][2])
               odom.linear.y=float(Arr1[i][3])*(-1)
          elif flag5==1:
               count=count+1
               if count>15:
                 count=0
                 flag5=2
                 pub99.publish(float(2.0));
               odom.linear.x=float(Arr1[i][2])
               odom.linear.y=float(Arr1[i][3])
          elif flag5==2:
               count=count+1
               if count>15:
                 count=0
                 flag5=3
                 pub99.publish(float(3.0));
               odom.linear.x=float(Arr1[i][2])*(-1)
               odom.linear.y=float(Arr1[i][3])
          elif flag5==3:
               count=count+1
               if count>15:
                 count=0
                 flag5=0
                 pub99.publish(float(4.0));
                 if flag2>0:
                   flag5=6
               odom.linear.x=float(Arr1[i][2])*(-1)
               odom.linear.y=float(Arr1[i][3])*(-1)
          elif flag5==5:
               count=count+1
               if count>15:
                 count=0
                 flag5=0
                 pub99.publish(float(4.0));
               odom.linear.x=float(Arr1[i][2])*(-1.2)
               odom.linear.y=0.0
          elif flag5==6:
               count=count+1
               if count>15:
                 count=0
                 flag5=7
                 pub99.publish(float(4.0));
               odom.linear.x=float(Arr1[i][2])
               odom.linear.y=0.0
          elif flag5==7:
               pass
          else:
               pass
          if flag2==0:
            odom.linear.z=float(Arr1[i][4])
            odom.angular.z=0.0
          else:
            odom.linear.z=0.0
            odom.angular.z=0.0
            odom.linear.x=0.0
            odom.linear.y=0.0
          odom.angular.x=0.0
          odom.angular.y=0.0
          pub3.publish(odom)
          rospy.sleep(FREQ)
        while d2>d1:
          d1=datetime.now()
          odom.linear.x=0.0
          odom.linear.y=0.0
          odom.linear.z=0.0
          odom.angular.x=0.0
          odom.angular.y=0.0
          odom.angular.z=0.0
          pub3.publish(odom)       
        odom.linear.x=0.0
        odom.linear.y=0.0
        odom.linear.z=0.0
        odom.angular.x=0.0
        odom.angular.y=0.0
        odom.angular.z=0.0
        pub3.publish(odom)
        rospy.set_param("/vp_ardrone2/flag2",0);
        rospy.loginfo(d1)
        rospy.loginfo(d2)
      ######################  hover  ############################
      elif(Arr1[i][0]=='hover' and flag1==0):  # hovering
        rospy.loginfo("hover")
        d1=datetime.now()
        s=math.floor(float(Arr1[i][1]))
        rospy.loginfo(s)
        mcs=(float(Arr1[i][1])-s)*1000000
        rospy.loginfo(mcs)
        d2=datetime.now()+timedelta(seconds=int(s),microseconds=int(mcs))
        rospy.loginfo(d1)
        pub3=rospy.Publisher('cmd_vel', Twist)
        odom=Twist()
        while d2>d1:
          d1=datetime.now()
          odom.linear.x=0.0
          odom.linear.y=0.0
          odom.linear.z=0.0
          odom.angular.x=0.0
          odom.angular.y=0.0
          odom.angular.z=0.0
          pub3.publish(odom)
          rospy.sleep(FREQ)
      else: 
        rospy.loginfo("unknown")
  
    file1.close();
    rospy.set_param("/vp_ardrone2/flag1",0);

def listener():
   rospy.init_node('web_publisher_node')
   if not rospy.has_param("/vp_ardrone2/flag1"):
     rospy.set_param("/vp_ardrone2/flag1",0) 
   if not rospy.has_param("/vp_ardrone2/flag2"):
     rospy.set_param("/vp_ardrone2/flag2",0) 
   if not rospy.has_param("/vp_ardrone2/flag3"):
     rospy.set_param("/vp_ardrone2/flag3",0) 
   sub = rospy.Subscriber("web_publisher",String,controller)
   rospy.spin()

if __name__ == '__main__':
       try:
           listener()
       except rospy.ROSInterruptException: pass
       except KeyboardInterrupt:
		sys.exit(1)
