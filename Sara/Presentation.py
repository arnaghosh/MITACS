#background image set -> done
#calibration and then live feedback part
#ready text and beep at start
import numpy as np
import cv2, sys, os
from win32api import GetSystemMetrics

class Present:
    def init(self):
        width = GetSystemMetrics(0);
        height = GetSystemMetrics(1)
        size = height, width,3;
        baseImg = np.zeros(size,dtype=np.uint8);
        cv2.rectangle(baseImg,(width/8,height/4),(3*width/8,height/2),(255,255,255),-1)
        cv2.rectangle(baseImg,(5*width/8,height/8),(7*width/8,3*height/8),(255,255,255),-1)
        pts = np.array([[3*width/8,height/4],[3*width/8,height/2],[5*width/8,3*height/8],[5*width/8,height/8]], np.int32);
        pts = pts.reshape((-1,1,2));
        cv2.fillPoly(baseImg,[pts],(255,255,255));
        cv2.circle(baseImg,(width/8,9*height/10),50,(255,255,0),-1);
        cv2.imshow("ppt",baseImg);
        cv2.waitKey(0);
        cv2.destroyAllWindows();

if __name__ == '__main__':
    ppt = Present()
    ppt.init()
