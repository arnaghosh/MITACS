import numpy as np
import cv2, sys, os, time
from win32api import GetSystemMetrics
from libmpdev import *

valX = 0
valY = 0
maxX = -100;
maxY = -100;

class calibrate_mouse:
    first_time_called = 1;
    init_x = 0;
    init_y =0;
    width = GetSystemMetrics(0);
    height = GetSystemMetrics(1);
    def init(self):  
        self.getMouseMax();
        size = self.height,self.width,1;
        img = np.zeros(size, dtype = np.uint8);
        cv2.namedWindow("win");
        cv2.setMouseCallback("win",self.mousePos);
        self.first_time_called = 1;
        while(1):
            
            cv2.imshow("win",img);
            if cv2.waitKey(15) == 27:
                break;

            x_val = 255*(valX-self.init_x)/maxX;
            y_val = 255*(valY-self.init_y)/maxY;
            print x_val, y_val
            if x_val<0:
                x_val = 0;
            if x_val>255 :
                x_val = 255;
            if y_val<0:
                y_val = 0;
            if y_val>255 :
                y_val = 255;
            img.fill(x_val);
            #img.fill(y_val);
            cv2.imshow("win",img);
            
        print self.init_x, self.init_y;
        print maxX, maxY;
            
    def mousePos(self,event,x,y,flags,param):
        global valX, valY
        if self.first_time_called==1:
            self.init_x, self.init_y = x,y;
            self.first_time_called = 0;
        if event== cv2.EVENT_MOUSEMOVE:
            valX, valY = x,y;

    def getMouseMax(self):
        global maxX, maxY
        cv2.namedWindow("get max");
        im = np.zeros((self.height,self.width,1),dtype = np.uint8);
        cv2.imshow("get max",im);
        cv2.setMouseCallback("get max",self.mousePos);
        t0 = time.time();
        while(1):
            if valX>maxX :
                maxX = valX;
            if valY>maxY :
                maxY = valY;
            cv2.waitKey(1);
            t1 = time.time();
            if (t1-t0)>1.0 :
                break;
            
        cv2.destroyWindow("get max") ;           

class calibrate_BIOPAC:
    first_time_called = 1;
    init_x = 0;
    init_y =0;
    width = GetSystemMetrics(0);
    height = GetSystemMetrics(1);
    mp = 0;
    maxVal = -100;

    def init(self):
        self.mp = MP150();
        cv2.namedWindow("win");
        for i in range(100):
            randomValue = self.gripperVal();
            cv2.waitKey(15);
        cv2.destroyAllWindows();
        self.first_time_called = 1;

    def test(self):
        self.first_time_called = 1;
        self.getGripperMax();
        print "Release the gripper";
        cv2.waitKey(1000);
        size = self.height,self.width,1;
        img = np.zeros(size, dtype = np.uint8);        
        while(1): 
            cv2.imshow("win",img);
            if cv2.waitKey(15) == 27:
                break;
            valX = self.gripperVal();
            x_val = 255*(valX-self.init_x)/(self.maxVal - self.init_x);
            #print valX, x_val
            if x_val<0:
                x_val = 0;
            if x_val>255 :
                x_val = 255;
            img.fill(x_val);
            #img.fill(y_val);
            cv2.imshow("win",img);            
        print self.init_x, self.maxVal;
        
    def destroy(self):
        self.mp.close();
        
    def gripperVal(self):
        sample = self.mp.sample();
        if self.first_time_called==1:
            #print "first"
            self.init_x = sample[0];
            self.first_time_called = 0;
        return sample[0];
        
    def getGripperMax(self):
        print "Press as hard as you can";
        t0 = time.time();
        while(1):
            valX = self.gripperVal();
            if valX>self.maxVal :
                self.maxVal = valX;
            cv2.waitKey(15);
            t1 = time.time();
            if (t1-t0)>2.0 :
                break;
        print self.maxVal;    
        #cv2.destroyWindow("get max") ; 

            
if __name__ == '__main__':
    #Mouse = calibrate_mouse()
    #Mouse.init()
    BP_gripper = calibrate_BIOPAC();
    BP_gripper.init();
    BP_gripper.test();
    BP_gripper.destroy();
