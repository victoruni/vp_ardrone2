#include <ros/ros.h>
#include <image_transport/image_transport.h>
#include <cv_bridge/cv_bridge.h>
#include <sensor_msgs/image_encodings.h>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>

namespace enc = sensor_msgs::image_encodings;

static const char WINDOW[] = "Image window";

class ImageConverter
{
  ros::NodeHandle nh_;
  image_transport::ImageTransport it_;
  image_transport::Subscriber image_sub_;
  image_transport::Publisher image_pub_;
  
public:
  ImageConverter()
    : it_(nh_)
  {
    image_pub_ = it_.advertise("image_converter1", 1);
    image_sub_ = it_.subscribe("ardrone/bottom/image_raw", 1, &ImageConverter::imageCb, this);

    cv::namedWindow(WINDOW);
  }

  ~ImageConverter()
  {
    cv::destroyWindow(WINDOW);
  }

  void imageCb(const sensor_msgs::ImageConstPtr& msg)
  {
    cv::Mat img_in;
    cv::Mat img_out;
    cv::Mat img_hsv;
    cv::Mat img_hue;
    cv::Mat img_sat;
    cv::Mat img_bin;
    IplImage *cv_input_;
    IplImage cv_output_;

    cv_bridge::CvImagePtr cv_ptr;
    try
    {
      cv_ptr = cv_bridge::toCvCopy(msg, enc::BGR8);
    }
    catch (cv_bridge::Exception& e)
    {
      ROS_ERROR("cv_bridge exception: %s", e.what());
      return;
    }

    if (cv_ptr->image.rows > 60 && cv_ptr->image.cols > 60)
      cv::circle(cv_ptr->image, cv::Point(50, 50), 10, CV_RGB(255,0,0));
    
    img_in = cv::Mat (cv_ptr->image).clone();
    img_out = img_in.clone ();
    // Convert Input image from BGR to HSV
    cv::cvtColor (img_in, img_hsv, CV_BGR2HSV);
    // Zero Matrices
    img_hue = cv::Mat::zeros(img_hsv.rows, img_hsv.cols, CV_8U);
    img_sat = cv::Mat::zeros(img_hsv.rows, img_hsv.cols, CV_8U);
    img_bin = cv::Mat::zeros(img_hsv.rows, img_hsv.cols, CV_8U);
    // HSV Channel 0 -> img_hue_ & HSV Channel 1 -> img_sat_
    int from_to[] = { 0,0, 1,1};
    cv::Mat img_split[] = { img_hue, img_sat};
    cv::mixChannels(&img_hsv, 3,img_split,2,from_to,2);

    for(int i = 0; i < img_out.rows; i++)
    {
      for(int j = 0; j < img_out.cols; j++)
      {
        // The output pixel is white if the input pixel
        // hue is orange and saturation is reasonable
; 
          }
      }
    }

    // Display HSV Image in HighGUI window
    cv::imshow ("WINDOW", img_hsv);    
    //cv::Split (img_in, img_b, img_g, img_r, 0);
    //

    //cv::setImageROI(cv_prt->image, cv::rect(0, 0,170, 140));
    //cv::addS(cv_prt->image,cv::scalar(50),cv_prt->image)
    //    
    //cv::imshow(WINDOW, cv_ptr->image);
    cv::waitKey(3);
    
    image_pub_.publish(cv_ptr->toImageMsg());
  }
};

int main(int argc, char** argv)
{
  ros::init(argc, argv, "image_converter1");
  ImageConverter ic;
  ros::spin();
  return 0;
}
