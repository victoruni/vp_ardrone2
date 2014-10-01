#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  
#  Сервис выдачи списка файлов сценариев и
#   списка команд сценария для шоу ardrone 2.0
#

import roslib; roslib.load_manifest('vp_ardrone2')

from vp_ardrone2.srv import *
import rospy
import os

PATH_SCENARIO="/home/petin/catkin_ws/src/vp_ardrone2/scenario/"

def handle_vp_ardrone2_get_scenario(req):
    if req.resp=="list":
      allfiles=os.listdir(PATH_SCENARIO)
      scnfiles=filter(lambda x:x.endswith('.txt'),allfiles)
      print "Server answer - list "+" ".join(scnfiles)
      return VpArdroneGetScenarioResponse(";".join(scnfiles))
    else:
      arr1=[]
      #file1=open("scenario/"+req.resp,"r")
      file1=open(PATH_SCENARIO+req.resp,"r")
      for stroka in file1.readlines():
        arr1.append(stroka.replace("\r","").replace("\n",""))
      #scn=file1.read()
      file1.close()
      #print "Server in - "+" "+req.resp+scn
      print "Server in - "+"&".join(arr1)
      return VpArdroneGetScenarioResponse("&".join(arr1))

def vp_ardrone2_get_scenario_server():
    rospy.init_node('vp_ardrone2_get_scenario_server')
    s = rospy.Service('vp_ardrone2_get_scenario', VpArdroneGetScenario, handle_vp_ardrone2_get_scenario)
    print "Ready server vp_ardrone2_get_scenario."
    rospy.spin()

if __name__ == "__main__":
    vp_ardrone2_get_scenario_server()
