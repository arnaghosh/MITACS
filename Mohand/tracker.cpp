// 1. draw circles and track mouse point - done
// 2. write the coordinates of mousepoint to a file - done
// 3. Plot the data and analyse further

#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <cstdio>
#include <iostream>
#include <string>
#include <cstring>
#include <sstream>
#include <fstream>
#include <ctime>

using namespace std;

//written for a monitor of default resolution 1366 X 768

int px=0,py=0;
float screen_conv_ratio_h = 1.0;
float screen_conv_ratio_v = 1.0;

//to track the mousePoint
void CallBackFunc(int event, int x, int y, int flags, void* userdata)
{
     if ( event == CV_EVENT_MOUSEMOVE )
     {
          px=x;py=y;
          //cout << "Mouse move over the window - position (" << x << ", " << y << ")" << endl;

     }
}

//Select circle center from ID
cv::Point select_center(int i){
  switch(i){
    case 0: return cv::Point(683*screen_conv_ratio_h,71*screen_conv_ratio_v);
    case 1: return cv::Point(994*screen_conv_ratio_h,157*screen_conv_ratio_v);
    case 2: return cv::Point(1052*screen_conv_ratio_h,384*screen_conv_ratio_v);
    case 3: return cv::Point(994*screen_conv_ratio_h,602*screen_conv_ratio_v);
    case 4: return cv::Point(683*screen_conv_ratio_h,693*screen_conv_ratio_v);
    case 5: return cv::Point(466*screen_conv_ratio_h,602*screen_conv_ratio_v);
    case 6: return cv::Point(243*screen_conv_ratio_h,384*screen_conv_ratio_v);
    case 7: return cv::Point(466*screen_conv_ratio_h,157*screen_conv_ratio_v);
    default: return cv::Point(683*screen_conv_ratio_h,384*screen_conv_ratio_v);
  }
}

//distance function
int dist(cv::Point p1, cv::Point p2){
    return sqrt((p1.x-p2.x)*(p1.x-p2.x) + (p1.y-p2.y)*(p1.y-p2.y));
}


int main(){
  int subject, dayNo;
  cout<<"Enter Subject No.: ";
  cin>>subject;
  cout<<"Enter Day No.: ";
  cin>>dayNo;
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
  string day;
  switch(dayNo){
    case 0: day = "_EarlyPractice_";break;
    case 1: day = "_Day1_";break;
    case 2: day = "_Day2_";break;
    default: day = "_Day3_";
  }
  string s = "Data/Subject"+SubNum.str()+day+"Data.txt";
  ofstream DatFile(s.c_str());
  ifstream sequence("Mohands(2,2,2).txt");
  string line;

  int trial=0;
  while(getline(sequence,line)){
      stringstream inp;
      inp.str(line);
      int i;
      inp>>i;
      float t=0.0;
      cv::Point center = select_center(i);
      //cout<<"drawing Circle "<<i<<" at "<<center.x<<center.y<<endl;
      im = cv::Mat(vert,horiz,CV_8UC1,cv::Scalar(0));
      cv::circle(im,center,50,cv::Scalar(255),2);
      clock_t Start = clock();
      do{
          cv::setMouseCallback("test",CallBackFunc,NULL);
          cv::imshow("test",im);
          //cout<<dist(center,cv::Point(px,py))<<endl;
          if(cv::waitKey(50)==27){
            return 0;
          }
          if(trial>0)DatFile<<trial<<" "<<px<<" "<<py<<" "<<t<<endl;
          t=((float)(clock()-Start)/CLOCKS_PER_SEC);
      }while(dist(center,cv::Point(px,py))>25);
      trial++;
  }
  return 0;
}
