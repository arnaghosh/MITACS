#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <cstdio>
#include <iostream>
#include <string>
#include <cstring>
#include <sstream>
#include <fstream>

using namespace std;

//written for a monitor of default resolution 1366 X 768

int px=0,py=0;
float screen_conv_ratio = 1.0;

void CallBackFunc(int event, int x, int y, int flags, void* userdata)
{
     if ( event == CV_EVENT_MOUSEMOVE )
     {
          px=x;py=y;
          //cout << "Mouse move over the window - position (" << x << ", " << y << ")" << endl;

     }
}

cv::Point select_center(int i){
  switch(i){
    case 0: return cv::Point(683*screen_conv_ratio,384*screen_conv_ratio);
    case 1: return cv::Point(483*screen_conv_ratio,384*screen_conv_ratio);
    case 2: return cv::Point(883*screen_conv_ratio,384*screen_conv_ratio);
    case 3: return cv::Point(683*screen_conv_ratio,184*screen_conv_ratio);
    case 4: return cv::Point(683*screen_conv_ratio,584*screen_conv_ratio);
    default: return cv::Point(883*screen_conv_ratio,584*screen_conv_ratio);
  }
}

int dist(cv::Point p1, cv::Point p2){
    return sqrt((p1.x-p2.x)*(p1.x-p2.x) + (p1.y-p2.y)*(p1.y-p2.y));
}


int main(){
  int subject;
  cout<<"Enter Subject No.: ";
  cin>>subject;
  int horiz,vert;
  cout<<"Enter Screen resolution:"<<endl<<"Horizontal: ";
  cin>>horiz;
  cout<<"Vertical: ";
  cin>>vert;
  cv::Mat im(vert,horiz,CV_8UC1,cv::Scalar(0));
  cv::namedWindow("test",1);
  //cv::setWindowProperty("test",CV_WND_PROP_FULLSCREEN,CV_WINDOW_FULLSCREEN);
  cv::imshow("test",im);
  cv::setMouseCallback("test",CallBackFunc,NULL);
  cv::waitKey(0);

  ostringstream SubNum;
  SubNum<<subject;
  string s = "Data/Subject"+SubNum.str()+"_Data.txt";
  ofstream DatFile(s.c_str());

  for(int i=0;i<5;i++){
      float t=0.0;
      cv::Point center = select_center(i);
      cout<<"drawing Circle "<<i<<" at "<<center.x<<center.y<<endl;
      im = cv::Mat(vert,horiz,CV_8UC1,cv::Scalar(0));
      cv::circle(im,center,50,cv::Scalar(255),2);
      do{
          cv::setMouseCallback("test",CallBackFunc,NULL);
          cv::imshow("test",im);
          cout<<dist(center,cv::Point(px,py))<<endl;
          if(cv::waitKey(50)==27){
            return 0;
          }
          DatFile<<i<<" "<<px<<", "<<py<<endl;
          t+=0.05;
      }while(dist(center,cv::Point(px,py))>25);
  }
  return 0;
}
