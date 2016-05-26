#TO DO:-
#1. wait for trigger from MRI scanner 
import numpy as np
import cv2, sys, os, time, win32api
from win32api import GetSystemMetrics
from calib import *

class Present_PERFORM:
    width = 640;#GetSystemMetrics(0);
    height = 480;#GetSystemMetrics(1);

    def init(self):
        cv2.namedWindow("display");
        cv2.namedWindow("operator");
        self.basImg = np.zeros((self.height,self.width,3),dtype=np.uint8);
        cv2.imshow("display",self.basImg);
        cv2.imshow("operator",self.basImg);
        self.valX = 0;
        self.valY = 0;
        self.constMax = 1000;#self.width;
        self.maxX = 0;
        self.maxY = 0;
        self.initX = 0;
        self.initY = 0;

    def mouseInitPos(self):
        self.initX, self.initY = win32api.GetCursorPos();
        
    def mousePos(self):
        self.valX, self.valY = win32api.GetCursorPos();

    def mouseInit(self):
        initImg = np.zeros((self.height,self.width,3),dtype=np.uint8);
        init2 = initImg.copy();
        init3 = initImg.copy();
        cv2.putText(init2, "Release the gripper and relax",(int(self.width/5),int(self.height/3)),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),3);
        cv2.putText(init3, "Press Enter when ready",(int(self.width/5),int(self.height/3)),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),3);
        cv2.imshow("display",init2);
        cv2.waitKey(3000);
        cv2.imshow("operator",init3);
        while(1):            
            if cv2.waitKey(30)==13:
                break;
        t0 = time.time();
        #cv2.setMouseCallback("display",self.mouseInitPos);
        while(1):
            #self.initX = self.valX;
            #self.initY = self.valY;
            self.mouseInitPos();
            t1 = time.time();
            if(t1-t0)>=0.6:
                break;
            cv2.waitKey(5);
        cv2.imshow("display",initImg);
        cv2.imshow("operator",initImg);

    def getMouseMax(self):
        maxImg = np.zeros((self.height,self.width,3),dtype=np.uint8);
        max2 = maxImg.copy();
        max3 = maxImg.copy();
        cv2.putText(max2, "Get ready to Squeeze as hard as you can for 3 seconds",(int(self.width/10),int(self.height/3)),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),3);
        cv2.putText(max3, "Press Enter when ready",(int(self.width/5),int(self.height/3)),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),3);
        cv2.imshow("display",max2);
        cv2.waitKey(5000);
        cv2.imshow("operator",max3);
        while(1):
            if cv2.waitKey(30)==13:
                break;
        max2 = maxImg.copy();
        cv2.putText(max2, "READY",(int(self.width/3),int(self.height/3)),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),3);
        cv2.imshow("display",max2);
        cv2.imshow("operator",max2);
        cv2.waitKey(1000);
        max2 = maxImg.copy();
        cv2.putText(max2, "SET",(int(self.width/3),int(self.height/3)),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),3);
        cv2.imshow("display",max2);
        cv2.imshow("operator",max2);
        cv2.waitKey(1000);
        max2 = maxImg.copy();
        cv2.putText(max2, "GO",(int(self.width/3),int(self.height/3)),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),3);
        cv2.imshow("display",max2);
        cv2.imshow("operator",max2);
        cv2.waitKey(1000);
        cv2.rectangle(maxImg, (int(self.width/3),int(0.1*self.height)),(int(2*self.width/3),self.height),(255,255,255),-1);
        cv2.rectangle(maxImg, (int(self.width/3),int(0.9*self.height)),(int(2*self.width/3),self.height),(255,0,0),-1);
        t0 = time.time();
        #cv2.setMouseCallback("display",self.mousePos);
        while(1):
            max2 = maxImg.copy();
            self.mousePos();
            rect_height = (self.valX-self.initX)*(0.8*self.height)/(self.constMax - self.initX);
            #rect_height = (self.valY-self.initY)*(0.1*self.height)/(self.constMax - self.initY);
            cv2.rectangle(max2, (int(4*self.width/9),int(0.9*self.height-rect_height)),(int(5*self.width/9),int(0.9*self.height)),(255,0,0),-1);
            cv2.imshow("display",max2);
            cv2.imshow("operator",max2);
            if self.valX>self.maxX:
                self.maxX = self.valX;
            if self.valY>self.maxY:
                self.maxY = self.valY;
            cv2.waitKey(1);
            t1= time.time();
            if (t1-t0)>=3.0:
                break;
            cv2.waitKey(5);
        maxImg = np.zeros((self.height,self.width,3),dtype=np.uint8);
        cv2.imshow("display",maxImg);
        cv2.imshow("operator",maxImg);

    def drawTarget(self,img,percentTarget):
        H = 0;
        while(H<=percentTarget*0.9*self.height/100):
            cv2.rectangle(img,(int(self.width/3),int(0.9*self.height-H)),(int(2*self.width/3),int(0.9*self.height)),(0,0,255),-1);
            H = H+10;
            cv2.imshow("display",img);
            cv2.imshow("operator",img);
            cv2.waitKey(30);
        
    def mouseTask(self, totalTrials):
        taskImg = np.zeros((self.height,self.width,3),dtype=np.uint8);
        task2 = taskImg.copy();
        task3 = taskImg.copy();
        cv2.putText(task2, "Squeeze to reach the red target bar and hold for 3 seconds",(int(self.width/10),int(self.height/3)),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),3);
        cv2.putText(task3, "Press Enter when ready",(int(self.width/5),int(self.height/3)),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),3);
        cv2.imshow("display",task2);
        cv2.waitKey(5000);
        cv2.imshow("operator",task3);
        while(1):
            if cv2.waitKey(30)==13:
                break;
        task2 = taskImg.copy();
        trialNo = 1;
        while( trialNo<= totalTrials):
            cv2.putText(task2, "READY",(int(self.width/3),int(self.height/3)),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),3);
            cv2.imshow("display",task2);
            cv2.imshow("operator",task2);
            cv2.waitKey(1000);
            task2 = taskImg.copy();
            cv2.putText(task2, "SET",(int(self.width/3),int(self.height/3)),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),3);
            cv2.imshow("display",task2);
            cv2.imshow("operator",task2);
            cv2.waitKey(1000);
            task2 = taskImg.copy();
            cv2.putText(task2, "GO",(int(self.width/3),int(self.height/3)),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),3);
            cv2.imshow("display",task2);
            cv2.imshow("operator",task2);
            cv2.waitKey(1000);
            #wait for trigger from MRI scanner
            cv2.rectangle(taskImg, (int(self.width/3),int(0.1*self.height)),(int(2*self.width/3),self.height),(255,255,255),-1);
            cv2.rectangle(taskImg, (int(self.width/3),int(0.9*self.height)),(int(2*self.width/3),self.height),(255,0,0),-1);
            percentTarget = 30; #in percentage
            self.drawTarget(taskImg,percentTarget);
            target_reached = 0;
            t0 = 0;
            t1 = 0;
            #cv2.setMouseCallback("display",self.mousePos);
            while(1):
                task2 = taskImg.copy();
                self.mousePos();
                current_pos = (self.valX-self.initX)*1.0/(self.maxX - self.initX);
                #current_pos = (self.valY-self.initY)*1.0/(self.maxY - self.initY);
                if current_pos<0:
                    current_pos = 0;
                if current_pos >1:
                    current_pos = 1;
                rect_height = current_pos*(0.8*self.height);
                cv2.rectangle(task2, (int(4*self.width/9),int(0.9*self.height-rect_height)),(int(5*self.width/9),int(0.9*self.height)),(255,0,0),-1);
                cv2.imshow("display",task2);
                cv2.imshow("operator",task2);
                if abs((100*current_pos) - percentTarget)<5:
                    if target_reached==0:
                        t0 = time.time();
                        target_reached =1;
                    else:
                        t1 = time.time();
                    if (t1-t0)>= 3.0:
                        break;
                else:
                    target_reached =0;
                cv2.waitKey(1);
            s = "Trial "+str(trialNo)+" done.";
            trialNo = trialNo + 1;
            taskImg = np.zeros((self.height,self.width,3),dtype=np.uint8);
            task2 = taskImg.copy();            
            if trialNo<totalTrials:
                cv2.putText(taskImg, "Well Done! Release the gripper and Get ready for the next trial",(int(self.width/10),int(self.height/3)),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),3);
            else:
                cv2.putText(taskImg, "Well Done! Release the gripper and Relax",(int(self.width/10),int(self.height/3)),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),3);
            cv2.putText(task2, s,(int(self.width/5),int(self.height/3)),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),3);
            cv2.imshow("display",taskImg);
            cv2.imshow("operator",task2);
            cv2.waitKey(2000);

if __name__=='__main__':
    #print win32api.GetCursorPos();
    obj = Present_PERFORM();
    obj.init();
    obj.mouseInit();
    print obj.initX;
    obj.getMouseMax();
    obj.mouseTask(1);
