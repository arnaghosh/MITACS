#TO DO:-
#1. wait for trigger from MRI scanner 
import numpy as np
import cv2, sys, os, time, win32api, wx
from calib import *

class Present_PERFORM:
    app = wx.App(False);
    sizes = [wx.Display(i).GetGeometry().GetSize() for i in range(wx.Display.GetCount())]
    width1 = sizes[1].GetWidth();
    height1 = sizes[1].GetHeight();
    width2 = sizes[0].GetWidth();
    height2 = sizes[0].GetHeight();

    def init(self):
        cv2.namedWindow("display");
        cv2.namedWindow("operator");
        self.basImg1 = np.zeros((self.height1,self.width1,3),dtype=np.uint8);
        self.basImg2 = np.zeros((self.height2,self.width2,3),dtype=np.uint8);
        cv2.imshow("display",self.basImg1);
        cv2.imshow("operator",self.basImg2);
        self.valX = 0;
        self.valY = 0;
        self.constMax = 3000;
        self.maxX = 0;
        self.maxY = 0;
        self.initX = 0;
        self.initY = 0;
        

    def mouseInitPos(self):
        self.initX, self.initY = win32api.GetCursorPos();
        
    def mousePos(self):
        self.valX, self.valY = win32api.GetCursorPos();

    def mouseInit(self):
        init2 = self.basImg1.copy();
        init3 = self.basImg2.copy();
        cv2.putText(init2, "Release the gripper and relax",(int(self.width1/5),int(self.height1/3)),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),3);
        cv2.putText(init3, "Press Enter when ready",(int(self.width2/5),int(self.height2/3)),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),3);
        cv2.imshow("display",init2);
        cv2.waitKey(3000);
        cv2.imshow("operator",init3);
        while(1):            
            if cv2.waitKey(30)==13:
                break;
        t0 = time.time();
        while(1):
            self.mouseInitPos();
            t1 = time.time();
            if(t1-t0)>=0.6:
                break;
            cv2.waitKey(5);
        cv2.imshow("display",self.basImg1);
        cv2.imshow("operator",self.basImg2);

    def getMouseMax(self):
        max2 = self.basImg1.copy();
        max3 = self.basImg2.copy();
        cv2.putText(max2, "Get ready to Squeeze as hard as you can for 3 seconds",(int(self.width1/10),int(self.height1/3)),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),3);
        cv2.putText(max3, "Press Enter when ready",(int(self.width2/5),int(self.height2/3)),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),3);
        cv2.imshow("display",max2);
        cv2.waitKey(2000);
        cv2.imshow("operator",max3);
        while(1):
            if cv2.waitKey(30)==13:
                break;
        max2 = self.basImg1.copy();
        max3 = self.basImg2.copy();
        cv2.putText(max2, "READY",(int(self.width1/3),int(self.height1/3)),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),3);
        cv2.putText(max3, "READY",(int(self.width2/3),int(self.height2/3)),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),3);
        cv2.imshow("display",max2);
        cv2.imshow("operator",max3);
        cv2.waitKey(1000);
        max2 = self.basImg1.copy();
        max3 = self.basImg2.copy();
        cv2.putText(max2, "SET",(int(self.width1/3),int(self.height1/3)),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),3);
        cv2.putText(max3, "SET",(int(self.width2/3),int(self.height2/3)),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),3);
        cv2.imshow("display",max2);
        cv2.imshow("operator",max3);
        cv2.waitKey(1000);
        max2 = self.basImg1.copy();
        max3 = self.basImg2.copy();
        cv2.putText(max2, "GO",(int(self.width1/3),int(self.height1/3)),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),3);
        cv2.putText(max3, "GO",(int(self.width2/3),int(self.height2/3)),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),3);
        cv2.imshow("display",max2);
        cv2.imshow("operator",max3);
        cv2.waitKey(1000);
        maxImg1 = self.basImg1.copy();
        maxImg2 = self.basImg2.copy();
        cv2.rectangle(maxImg1, (int(self.width1/3),int(0.1*self.height1)),(int(2*self.width1/3),self.height1),(255,255,255),-1);
        cv2.rectangle(maxImg2, (int(self.width2/3),int(0.1*self.height2)),(int(2*self.width2/3),self.height2),(255,255,255),-1);
        cv2.rectangle(maxImg1, (int(self.width1/3),int(0.9*self.height1)),(int(2*self.width1/3),self.height1),(255,0,0),-1);
        cv2.rectangle(maxImg2, (int(self.width2/3),int(0.9*self.height2)),(int(2*self.width2/3),self.height2),(255,0,0),-1);
        t0 = time.time();
        #cv2.setMouseCallback("display",self.mousePos);
        while(1):
            max2 = maxImg1.copy();
            max3 = maxImg2.copy();
            self.mousePos();
            rect_height1 = (self.valX-self.initX)*(0.8*self.height1)/(self.constMax - self.initX);
            rect_height2 = (self.valX-self.initX)*(0.8*self.height2)/(self.constMax - self.initX);
            #rect_height1 = (self.valY-self.initY)*(0.1*self.height1)/(self.constMax - self.initY);
            #rect_height2 = (self.valY-self.initY)*(0.1*self.height2)/(self.constMax - self.initY);
            cv2.rectangle(max2, (int(4*self.width1/9),int(0.9*self.height1-rect_height1)),(int(5*self.width1/9),int(0.9*self.height1)),(255,0,0),-1);
            cv2.rectangle(max3, (int(4*self.width2/9),int(0.9*self.height2-rect_height2)),(int(5*self.width2/9),int(0.9*self.height2)),(255,0,0),-1);
            cv2.imshow("display",max2);
            cv2.imshow("operator",max3);
            cv2.waitKey(5);
            if self.valX>self.maxX:
                self.maxX = self.valX;
            if self.valY>self.maxY:
                self.maxY = self.valY;
            cv2.waitKey(1);
            t1= time.time();
            if (t1-t0)>=3.0:
                break;
        cv2.imshow("display",self.basImg1);
        cv2.imshow("operator",self.basImg2);

    def drawTarget(self,img,percentTarget,win):
        height, width, ch = img.shape;
        H = 0;
        while(H<=percentTarget*0.9*height/100):
            cv2.rectangle(img,(int(width/3),int(0.9*height-H)),(int(2*width/3),int(0.9*height)),(0,0,255),-1);
            H = H+10;
            cv2.imshow(win,img);
            cv2.waitKey(10);
        
    def mouseTask(self, totalTrials):
        task2 = self.basImg1.copy();
        task3 = self.basImg2.copy();
        cv2.putText(task2, "Squeeze to reach the red target bar and hold for 3 seconds",(int(self.width1/10),int(self.height1/3)),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),3);
        cv2.putText(task3, "Press Enter when ready",(int(self.width2/5),int(self.height2/3)),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),3);
        cv2.imshow("display",task2);
        cv2.waitKey(2000);
        cv2.imshow("operator",task3);
        while(1):
            if cv2.waitKey(30)==13:
                break;
        task2 = self.basImg1.copy();
        task3 = self.basImg2.copy();
        trialNo = 1;
        while( trialNo<= totalTrials):
            cv2.putText(task2, "READY",(int(self.width1/3),int(self.height1/3)),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),3);
            cv2.putText(task3, "READY",(int(self.width2/3),int(self.height2/3)),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),3);
            cv2.imshow("display",task2);
            cv2.imshow("operator",task3);
            cv2.waitKey(1000);
            task2 = self.basImg1.copy();
            task3 = self.basImg2.copy();    
            cv2.putText(task2, "SET",(int(self.width1/3),int(self.height1/3)),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),3);
            cv2.putText(task3, "SET",(int(self.width2/3),int(self.height2/3)),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),3);
            cv2.imshow("display",task2);
            cv2.imshow("operator",task3);
            cv2.waitKey(1000);
            task2 = self.basImg1.copy();
            task3 = self.basImg2.copy(); 
            cv2.putText(task2, "GO",(int(self.width1/3),int(self.height1/3)),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),3);
            cv2.putText(task3, "GO",(int(self.width2/3),int(self.height2/3)),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),3);
            cv2.imshow("display",task2);
            cv2.imshow("operator",task3);
            cv2.waitKey(1000);
            while(1):
                if cv2.waitKey(15)==61:
                    break;
            taskImg1 = self.basImg1.copy();
            taskImg2 = self.basImg2.copy();
            cv2.rectangle(taskImg1, (int(self.width1/3),int(0.1*self.height1)),(int(2*self.width1/3),self.height1),(255,255,255),-1);
            cv2.rectangle(taskImg1, (int(self.width1/3),int(0.9*self.height1)),(int(2*self.width1/3),self.height1),(255,0,0),-1);
            cv2.rectangle(taskImg2, (int(self.width2/3),int(0.1*self.height2)),(int(2*self.width2/3),self.height2),(255,255,255),-1);
            cv2.rectangle(taskImg2, (int(self.width2/3),int(0.9*self.height2)),(int(2*self.width2/3),self.height2),(255,0,0),-1);
            percentTarget = 30; #in percentage
            self.drawTarget(taskImg1,percentTarget,"display");
            self.drawTarget(taskImg2,percentTarget,"operator");
            target_reached = 0;
            t0 = 0;
            t1 = 0;
            #cv2.setMouseCallback("display",self.mousePos);
            while(1):
                task2 = taskImg1.copy();
                task3 = taskImg2.copy();
                self.mousePos();
                current_pos = (self.valX-self.initX)*1.0/(self.maxX - self.initX);
                #current_pos = (self.valY-self.initY)*1.0/(self.maxY - self.initY);
                if current_pos<0:
                    current_pos = 0;
                if current_pos >1:
                    current_pos = 1;
                rect_height1 = current_pos*(0.8*self.height1);
                rect_height2 = current_pos*(0.8*self.height2);
                #print rect_height1, rect_height2;
                cv2.rectangle(task2, (int(4*self.width1/9),int(0.9*self.height1-rect_height1)),(int(5*self.width1/9),int(0.9*self.height1)),(255,0,0),-1);
                cv2.rectangle(task3, (int(4*self.width2/9),int(0.9*self.height2-rect_height2)),(int(5*self.width2/9),int(0.9*self.height2)),(255,0,0),-1);
                cv2.imshow("display",task2);
                cv2.imshow("operator",task3);
                cv2.waitKey(5);
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
            s = "Trial "+str(trialNo)+" done.";
            trialNo = trialNo + 1;
            task2 = self.basImg1.copy();
            task3 = self.basImg2.copy();            
            if trialNo<totalTrials:
                cv2.putText(task2, "Well Done! Release the gripper and Get ready for the next trial",(int(self.width1/10),int(self.height1/3)),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),3);
            else:
                cv2.putText(task2, "Well Done! Release the gripper and Relax",(int(self.width1/10),int(self.height1/3)),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),3);
            cv2.putText(task3, s,(int(self.width2/5),int(self.height2/3)),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),3);
            cv2.imshow("display",task2);
            cv2.imshow("operator",task3);
            cv2.waitKey(2000);

if __name__=='__main__':
    obj = Present_PERFORM();
    obj.init();
    obj.mouseInit();
    print obj.initX;
    obj.getMouseMax();
    obj.mouseTask(1);
