// MohandTracker.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <cstdio>
#include <iostream>
#include <string>
#include <cstring>
#include <sstream>
#include <fstream>
#include <ctime>
#include <vector>
#include <Windows.h>
#include <opencv2\highgui\highgui.hpp>
#include <opencv2\imgproc\imgproc.hpp>

using namespace std;
//written for a monitor of default resolution 1366 X 768

#define movement_stop_thresh 2
int px = 0, py = 0;
float screen_conv_ratio_h = 1.0;
float screen_conv_ratio_v = 1.0;

//to track the mousePoint
void CallBackFunc(int event, int x, int y, int flags, void* userdata)
{
	if (event == CV_EVENT_MOUSEMOVE)
	{
		px = x; py = y;
		//cout << "Mouse move over the window - position (" << x << ", " << y << ")" << endl;

	}
}

void screen_conv(int horiz, int vert) {
	screen_conv_ratio_h = (1.0*horiz) / 1366;
	screen_conv_ratio_v = (1.0*vert) / 768;
}

//Select circle center from ID
cv::Point select_center(int i) {
	switch (i) {
	case 0: return cv::Point(683 * screen_conv_ratio_h, 71 * screen_conv_ratio_v);
	case 1: return cv::Point(994 * screen_conv_ratio_h, 157 * screen_conv_ratio_v);
	case 2: return cv::Point(1052 * screen_conv_ratio_h, 384 * screen_conv_ratio_v);
	case 3: return cv::Point(994 * screen_conv_ratio_h, 602 * screen_conv_ratio_v);
	case 4: return cv::Point(683 * screen_conv_ratio_h, 693 * screen_conv_ratio_v);
	case 5: return cv::Point(466 * screen_conv_ratio_h, 602 * screen_conv_ratio_v);
	case 6: return cv::Point(243 * screen_conv_ratio_h, 384 * screen_conv_ratio_v);
	case 7: return cv::Point(466 * screen_conv_ratio_h, 157 * screen_conv_ratio_v);
	default: return cv::Point(683 * screen_conv_ratio_h, 384 * screen_conv_ratio_v);
	}
}

//distance function
int dist(cv::Point p1, cv::Point p2) {
	return sqrt((p1.x - p2.x)*(p1.x - p2.x) + (p1.y - p2.y)*(p1.y - p2.y));
}


int main(int argc, char** argv) {
	int subject, dayNo, block;
	//cout<<"Enter Subject No.: ";
	//cin>>subject;
	subject = atoi(argv[1]);
	//cout<<"Enter Day No.: ";
	//cin>>dayNo;
	dayNo = atoi(argv[2]);
	block = atoi(argv[3]);
	int horiz, vert;
	//cout<<"Enter Screen resolution:"<<endl<<"Horizontal: ";
	//cin>>horiz;
	horiz = atoi(argv[4]);
	//cout<<"Vertical: ";
	//cin>>vert;
	vert = atoi(argv[5]);
	screen_conv(horiz, vert);
	cv::Mat im(vert, horiz, CV_8UC1, cv::Scalar(0));
	cv::namedWindow("test", 1);
	//cv::setWindowProperty("test",CV_WND_PROP_FULLSCREEN,CV_WINDOW_FULLSCREEN);
	cv::imshow("test", im);
	cv::setMouseCallback("test", CallBackFunc, NULL);
	cv::waitKey(0);

	ostringstream SubNum, blockNum;
	SubNum << subject;
	blockNum << block;
	string day;
	switch (dayNo) {
	case 1: day = "_Day1_"; break;
	case 2: day = "_Day2_"; break;
	case 3: day = "_Day3_"; break;
	case 4: day = "_Day4_"; break;
	case 5: day = "_Day5_"; break;
	case 6: day = "_Baseline_"; break;
	case 7: day = "_Performance_"; break;
	default: day = "_Familiarisation_";
	}
	SetCursorPos(horiz / 2, vert / 2);
	int old_curx = (int)horiz / 2;
	int old_cury = (int)vert / 2;
	if (dayNo > 7) {
		for (int i = 0; i < 10; i++) {
			cv::Point center = select_center(i % 9);
			im = cv::Mat(vert, horiz, CV_8UC1, cv::Scalar(0));
			cv::circle(im, center, 50, cv::Scalar(255), 2);
			int continuous_stay = 0;
			int movement_stopped = 0;
			do {
				cv::setMouseCallback("test", CallBackFunc, NULL);
				cv::imshow("test", im);
				if (cv::waitKey(5) == 27) {
					return 0;
				}
				if (dist(center, cv::Point(px, py)) < 50) {
					continuous_stay++;
					if (dist(cv::Point(old_curx, old_cury), cv::Point(px, py)) <= movement_stop_thresh)
						movement_stopped++;
					else
						movement_stopped = 0;
				}
				else {
					continuous_stay = 0;
					movement_stopped = 0;
				}
				old_curx = px;
				old_cury = py;
			} while (continuous_stay<15 || movement_stopped<10);
		}
		return 0;
	}
	string s;
	if (dayNo <= 5) s = "C:\\Users\\neuro\\Documents\\Arna\\Tracker\\Data\\Subject " + SubNum.str() + "\\Subject" + SubNum.str() + day + "Block" + blockNum.str() + "_Data.txt";
	else s = "C:\\Users\\neuro\\Documents\\Arna\\Tracker\\Data\\Subject " + SubNum.str() + "\\Subject" + SubNum.str() + day + "Data.txt";
	ofstream DatFile(s.c_str());
	ifstream sequence("C:\\Users\\neuro\\Documents\\Visual Studio 2015\\Projects\\MohandTracker\\Mohands(2,2,2).txt");
	string line;
	int trial = 0;
	while (getline(sequence, line)) {
		if (trial == 0)cout << "Started" << endl;
		stringstream inp;
		inp.str(line);
		vector<int> iv;
		int num;
		while (inp >> num) {
			iv.push_back(num);
		}
		int i;
		if (dayNo <= 5) i = iv[(5 * (dayNo - 1) + block - 1) % iv.size()];
		else i = iv[(25 + dayNo % 2) % iv.size()];
		float t = 0.0;
		cv::Point center = select_center(i % 9);
		//cout<<"drawing Circle "<<i<<" at "<<center.x<<center.y<<endl;
		im = cv::Mat(vert, horiz, CV_8UC1, cv::Scalar(0));
		cv::circle(im, center, 50, cv::Scalar(255), 2);
		clock_t Start = clock();
		int continuous_stay = 0;
		int movement_stopped = 0;
		do {
			cv::setMouseCallback("test", CallBackFunc, NULL);
			cv::imshow("test", im);
			//cout<<dist(center,cv::Point(px,py))<<endl;
			if (cv::waitKey(5) == 27) {
				return 0;
			}
			if (dist(center, cv::Point(px, py)) < 50) {
				continuous_stay++;
				if (dist(cv::Point(old_curx, old_cury), cv::Point(px, py)) <= movement_stop_thresh) {
					movement_stopped++;
					//cout << "stopped ";
				}
				else
					movement_stopped = 0;
			}
			else {
				continuous_stay = 0;
				movement_stopped = 0;
			}
			old_curx = px;
			old_cury = py;
			DatFile << trial << " " << px << " " << py << " " << t << endl;
			t = ((float)(clock() - Start) / CLOCKS_PER_SEC);
		} while (continuous_stay<15 || movement_stopped<10);
		trial++;
	}
	//DatFile << trial << " " << 0 << " " << 0 << " " << 0.0 << endl;
	return 0;
}
