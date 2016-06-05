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
#include <process.h>
#include <WinUser.h>
#include <windef.h>
#include <mutex>
#include <opencv2\highgui\highgui.hpp>
#include <opencv2\imgproc\imgproc.hpp>

using namespace std;
//written for a monitor of default resolution 1366 X 768

#define movement_stop_thresh 2
#define monitor_pix_per_mm 4.25
POINT p;
int f_array[5] = { 3, 8, 6, 4, 1 };
int px = 0, py = 0;
float screen_conv_ratio_h = 1.0;
float screen_conv_ratio_v = 1.0;
vector<float> global_trial, global_x, global_y, global_t;
mutex m;
int end_thread = 0;
int pause_thread = 0;
float t = 0.0, prev_t = -1;
clock_t Start;
int trial = 0;
//to track the mousePoint
void CaptureMousePosition(void *param) {
	
	while (1) {
		if (end_thread)break;
		if (pause_thread)continue;
		t = ((float)(clock() - Start) / CLOCKS_PER_SEC);
		if (prev_t == t)continue;
		GetCursorPos(&p);
		m.lock();
		global_trial.push_back(trial);
		global_x.push_back(p.x-9.0);
		global_y.push_back(p.y-30.0);
		global_t.push_back(t);
		prev_t = t;
		m.unlock();
	}
	_endthread();
}

void getMousePointFromVector(int old_x,int old_y) {
	m.lock();
	int length_of_vec = global_x.size();
	if (length_of_vec == 0 || length_of_vec>global_x.size()) {
		px = old_x;
		py = old_y;
	}
	else {
		px = global_x[length_of_vec - 1];
		py = global_y[length_of_vec - 1];
	}
	m.unlock();
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
	dayNo = atoi(argv[2]);
	block = atoi(argv[3]);
	int horiz, vert;
	horiz = atoi(argv[4]);
	vert = atoi(argv[5]);
	screen_conv(horiz, vert);
	cv::Mat im(vert, horiz, CV_8UC1, cv::Scalar(0));
	cv::namedWindow("test", 1);
	cv::imshow("test", im);
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
		Start = clock();
		_beginthread(CaptureMousePosition, 0, NULL);
		clock_t t1,t2;
		float cont_stay = 0;
		for (int i = 0; i < 5; i++) {
			cv::Point center = select_center(f_array[i] % 9);
			im = cv::Mat(vert, horiz, CV_8UC1, cv::Scalar(0));
			cv::circle(im, center, 50, cv::Scalar(255), 2);
			//int continuous_stay = 0;
			int movement_stopped = 0;
			t2 = clock();
			do {
				getMousePointFromVector(old_curx,old_cury);
				cv::imshow("test", im);
				if (cv::waitKey(5) == 27) {
					end_thread = 1;
					return 0;
				}
				t1 = clock();
				if (dist(center, cv::Point(px, py)) < 50) {
					cont_stay+=(t1-t2);
					if (dist(cv::Point(old_curx, old_cury), cv::Point(px, py)) <= movement_stop_thresh)
						movement_stopped++;
					else
						movement_stopped = 0;
				}
				else {
					cont_stay = 0;
					movement_stopped = 0;
				}
				t2 = clock();
				old_curx = px;
				old_cury = py;
			} while (cont_stay<200 || movement_stopped<10);
		}
		end_thread = 1;
		return 0;
	}
	string s;
	if (dayNo <= 5) s = "C:\\Users\\neuro\\Documents\\Arna\\Tracker\\Data\\Subject " + SubNum.str() + "\\Subject" + SubNum.str() + day + "Block" + blockNum.str() + "_Data.txt";
	else s = "C:\\Users\\neuro\\Documents\\Arna\\Tracker\\Data\\Subject " + SubNum.str() + "\\Subject" + SubNum.str() + day + "Data.txt";
	ifstream sequence("C:\\Users\\neuro\\Documents\\Visual Studio 2015\\Projects\\MohandTracker\\Mohands(4,6,5).txt");
	string line;
	Start = clock();
	_beginthread(CaptureMousePosition, 0, NULL);
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

		cv::Point center = select_center(i % 9);
		im = cv::Mat(vert, horiz, CV_8UC1, cv::Scalar(0));
		cv::circle(im, center, 50, cv::Scalar(255), 2);
		
		int continuous_stay = 0;
		int movement_stopped = 0;
		do {
			getMousePointFromVector(old_curx, old_cury);
			cv::imshow("test", im);
			if (cv::waitKey(5) == 27) {
				end_thread = 1;
				return 0;
			}
			if (dist(center, cv::Point(px, py)) < 50) {
				continuous_stay++;
				if (dist(cv::Point(old_curx, old_cury), cv::Point(px, py)) <= movement_stop_thresh) {
					movement_stopped++;
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
			
		} while (continuous_stay<15 || movement_stopped<10);
		m.lock();
		trial++;
		Start = clock();
		m.unlock();
	}

	end_thread = 1;
	cv::destroyAllWindows();
	ofstream DatFile(s.c_str());
	for (int i = 1; i < global_x.size(); i++) {
		DatFile << global_trial[i] << " " << (global_x[i])/monitor_pix_per_mm << " " << (global_y[i])/monitor_pix_per_mm << " " << global_t[i] << endl;
	}
	return 0;
}
