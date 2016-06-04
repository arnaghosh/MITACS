#include "stdafx.h"
#include <cstdio>
#include <stdlib.h>
#include <iostream>
#include <string>
#include <cstring>
#include <sstream>
#include <fstream>
#include <ctime>
#include <vector>
#include <opencv2\highgui\highgui.hpp>
#include <opencv2\imgproc\imgproc.hpp>
#include <Windows.h>

using namespace std;
//written for a monitor of default resolution 1366 X 768

#define movement_stop_thresh 2
int f_array[5] = { 3, 8, 6, 4, 1 };
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
	subject = atoi(argv[1]);
	int horiz, vert;
	horiz = atoi(argv[2]);
	vert = atoi(argv[3]);
	screen_conv(horiz, vert);
	cv::Mat im(vert, horiz, CV_8UC1, cv::Scalar(0));
	cv::namedWindow("test", 1);
	cv::imshow("test", im);
	cv::waitKey(0);

	ostringstream SubNum, blockNum;
	SubNum << subject;
	
	ifstream sequence("C:\\Users\\neuro\\Documents\\Visual Studio 2015\\Projects\\RecognitionTask\\recogTargets.txt");
	string line;
	int trial = 1;
	int temp = 0;
	while (getline(sequence, line)) {
		stringstream inp;
		inp.str(line);
		vector<int> iv;
		int num;
		while (inp >> num) {
			iv.push_back(num);
		}
		int i = iv[0];
		float t = 0.0;
		cv::Point center = select_center(i % 9);
		im = cv::Mat(vert, horiz, CV_8UC1, cv::Scalar(0));
		cv::circle(im, center, 50, cv::Scalar(255), 2);
		clock_t Start = clock();
		do {
			cv::setMouseCallback("test", CallBackFunc, NULL);
			cv::imshow("test", im);
			if (cv::waitKey(5) == 27) {
				cout << "Escaped" << endl;
				return 0;
			}				
			t = ((float)(clock() - Start) / CLOCKS_PER_SEC);
		} while (t<=1.0);
		if (trial % 7 == 0) {
			cout << "DONE" << endl;
			cin >> temp;
		}
		trial++;
	}
	//DatFile << trial << " " << 0 << " " << 0 << " " << 0.0 << endl;
	return 0;
}