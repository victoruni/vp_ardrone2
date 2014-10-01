#!/usr/bin/env python
import roslib
roslib.load_manifest('vp_ardrone2')
import sys
import rospy
import cv
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class image_converter:

  def __init__(self):
    self.image_pub = rospy.Publisher("image_converter1",Image)

    cv.NamedWindow("Image window", 1)
    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("ardrone/image_raw",Image,self.callback)

  def callback(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv(data, "bgr8")
    except CvBridgeError, e:
      print e

    #(cols,rows) = cv.GetSize(cv_image)
    #if cols > 60 and rows > 60 :
    #  cv.Circle(cv_image, (50,50), 10, 255)

    #######################################
    #img1=cv.CreateImage((150,150),8,3)
    #cv.Rectangle(cv_image, (60,60),(70,90), (255,0,255))
    #sub1=cv.GetSubRect(cv_image,(60,60,150,150))
    #save1=cv.CloneMat(sub1)
    #sub2=cv.GetSubRect(img1,(0,0,150,150))
    #cv.Copy(save1,sub2)
    storage=cv.CreateMemStorage(0)
    img=cv.CreateImage((cv.GetSize(cv_image)[1],cv.GetSize(cv_image)[1]),8,3)    
    img1=cv.CreateImage((cv.GetSize(cv_image)[1],cv.GetSize(cv_image)[1]),8,3)    
    #img=cv.CreateImage(cv.GetSize(cv_image),8,3)    
    img_r=cv.CreateImage(cv.GetSize(img),8,1)
    img_g=cv.CreateImage(cv.GetSize(img),8,1)
    img_b=cv.CreateImage(cv.GetSize(img),8,1)
    img_g1=cv.CreateImage(cv.GetSize(img),8,1)
    img_g2=cv.CreateImage(cv.GetSize(img),8,1)

    img2=cv.LoadImage("/home/petin/catkin_ws/src/vp_ardrone2/ris1.jpg",cv.CV_LOAD_IMAGE_GRAYSCALE)
    
    
    sub1=cv.GetSubRect(cv_image,(0,0,cv.GetSize(cv_image)[1],cv.GetSize(cv_image)[1]))
    save1=cv.CloneMat(sub1)
    sub2=cv.GetSubRect(img,(0,0,cv.GetSize(cv_image)[1],cv.GetSize(cv_image)[1]))
    cv.Copy(save1,sub2)

    #cv.CvtColor(img, img1, cv.CV_BGR2HSV)
    #cv.CvtPixToPlane(img1,img_h,img_s,img_v,None)
    #cv.CvtColor(img, gray, cv.CV_BGR2GRAY)
    #cv.Smooth(gray,gray,cv.CV_GAUSSIAN,5,5)
    cv.Split(img,img_b,img_g,img_r,None)
    #
    #cv.ShowImage("Image window1", img)
    #cv.ShowImage("Image windowb", img_b)
    #cv.ShowImage("Image windowg", img_g)
    #cv.ShowImage("Image windowr", img_r)
    #
    cv.InRangeS(img_g, cv.Scalar(180), cv.Scalar(255), img_g1);
    #cv.InRangeS(img_s, cv.Scalar(135), cv.Scalar(255), img_s1);
    #cv.InRangeS(img_b, cv.Scalar(0), cv.Scalar(61), img_b1);
    #cv.Invert(img_g1,img_g2,cv.CV_SVD)
    cv.Smooth(img2,img2,cv.CV_GAUSSIAN,9,9)
    #
    cv.ShowImage("Image windowh1", img_g1)
    #cv.ShowImage("Image windowg1", img_h1)
    #cv.ShowImage("Image windowr1", img_r1)
    #cv.ShowImage("Image gray", gray)
    # search circle
    storage = cv.CreateMat(img2.width, 1, cv.CV_32FC3)
    cv.ShowImage("Image window1", img2)
    cv.HoughCircles(img2, storage, cv.CV_HOUGH_GRADIENT, 2, 100, 100, 50, 10, 400)
    #rospy.loginfo(storage.width)
    for i in xrange(storage.width - 1):
      radius = storage[i, 2]
      center = (storage[i, 0], storage[i, 1])
      rospy.loginfo('444')
      cv.Circle(cv_image, center, radius, (0, 0, 255), 3, 10, 200)
    #search_circle=cv.HoughCircles(img_g1,np.asarray(storage),3,10,150)
    #for res in search_circles:
    #   p = float (cv.GetSeqElem(res))
    #   pt = cv.Point( cv.Round( p[0] ), cv.Round( p[1] ) );
    #   cv.Circle( cv_image, pt, cv.Round( p[2] ), 255 );
    #
    #cv.And(img_g,img_r,img_a)
    #cv.And(img_a,img_b,img_a)
     #
    cv.ShowImage("Image window", cv_image)
    cv.WaitKey(3)

    try:
      self.image_pub.publish(self.bridge.cv_to_imgmsg(cv_image, "bgr8"))
    except CvBridgeError, e:
      print e

def main(args):
  ic = image_converter()
  rospy.init_node('image_converter1', anonymous=True)
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print "Shutting down"
  cv.DestroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
