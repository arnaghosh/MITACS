#TO DO:-
#1. change scale of target to max 60%
#2. Add a jitter time of 1-2 seconds after each trial.
#3. Center all text and make them big.
import numpy as np
import cv2, sys, os, time, win32api, wx
from libmpdev import *

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
        self.val = 0;
        self.constMax = 6;
        self.maxVal = -100;
        self.init = 0;
        self.mp = MP150();        

    def gripperInitVal(self):
        for i in range(100):
            randomValue = self.gripperVal();
            cv2.waitKey(15);
        self.init = self.mp.sample()[0];
        
    def gripperVal(self):
        sample = self.mp.sample();
        self.val = sample[0];

    def gripperInit(self):
        init2 = self.basImg1.copy();
        init3 = self.basImg2.copy();
        cv2.putText(init2, "Release the gripper and relax",(int(self.width1/5),int(self.height1/3)),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),3);
        cv2.putText(init3, "Press Enter when ready",(int(self.width2/5),int(self.height2/3)),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),3);
        cv2.imshow("display",init2);
        cv2.waitKey(3000);
        cv2.imshow("operator",init3);
        while(1):            
            if cv2.waitKey(15)==13:
                break;
        t0 = time.time();
        while(1):
            self.gripperInitVal();
            t1 = time.time();
            if(t1-t0)>=0.5:
                break;
            cv2.waitKey(5);
        cv2.imshow("display",self.basImg1);
        cv2.imshow("operator",self.basImg2);

    def getGripperMax(self):
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
        cv2.rectangle(maxImg1, (int(2*self.width1/5),int(0.1*self.height1)),(int(3*self.width1/5),self.height1),(255,255,255),-1);
        cv2.rectangle(maxImg2, (int(self.width2/3),int(0.1*self.height2)),(int(2*self.width2/3),self.height2),(255,255,255),-1);
        cv2.rectangle(maxImg1, (int(2*self.width1/5),int(0.9*self.height1)),(int(3*self.width1/5),self.height1),(255,0,0),-1);
        cv2.rectangle(maxImg2, (int(self.width2/3),int(0.9*self.height2)),(int(2*self.width2/3),self.height2),(255,0,0),-1);
        t0 = time.time();
        while(1):
            max2 = maxImg1.copy();
            max3 = maxImg2.copy();
            self.gripperVal();
            rect_height1 = (self.val-self.init)*(0.8*self.height1)/(self.constMax - self.init);
            rect_height2 = (self.val-self.init)*(0.8*self.height2)/(self.constMax - self.init);
            cv2.rectangle(max2, (int(5*self.width1/11),int(0.9*self.height1-rect_height1)),(int(6*self.width1/11),int(0.9*self.height1)),(255,0,0),-1);
            cv2.rectangle(max3, (int(4*self.width2/9),int(0.9*self.height2-rect_height2)),(int(5*self.width2/9),int(0.9*self.height2)),(255,0,0),-1);
            cv2.imshow("display",max2);
            cv2.imshow("operator",max3);
            cv2.waitKey(5);
            if self.val>self.maxVal:
                self.maxVal = self.val;
            t1= time.time();
            if (t1-t0)>=3.0:
                break;
        cv2.imshow("display",self.basImg1);
        cv2.imshow("operator",self.basImg2);

    def drawTarget(self,img1,img2,percentTarget):
        height1, width1, ch1 = img1.shape;
        height2, width2, ch2 = img2.shape;
        H = 0;
        while(H<=percentTarget):
            h1 = H*0.9*height1/100;
            h2 = H*0.9*height2/100;
            cv2.rectangle(img1,(int(2*width1/5),int(0.9*height1-h1)),(int(3*width1/5),int(0.9*height1)),(0,0,255),-1);
            cv2.rectangle(img2,(int(width2/3),int(0.9*height2-h2)),(int(2*width2/3),int(0.9*height2)),(0,0,255),-1);
            H = H+5;
            cv2.imshow("display",img1);
            cv2.imshow("operator",img2);
            cv2.waitKey(10);
        
    def gripperTask(self, totalTrials):
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
        
        trialNo = 1;
        while( trialNo<= totalTrials):
            task2 = self.basImg1.copy();
            task3 = self.basImg2.copy();
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
            cv2.waitKey(500);
            while(1):
                if cv2.waitKey(15)==61:
                    break;
            taskImg1 = self.basImg1.copy();
            taskImg2 = self.basImg2.copy();
            cv2.rectangle(taskImg1, (int(2*self.width1/5),int(0.1*self.height1)),(int(3*self.width1/5),self.height1),(255,255,255),-1);
            cv2.rectangle(taskImg1, (int(2*self.width1/5),int(0.9*self.height1)),(int(3*self.width1/5),self.height1),(255,0,0),-1);
            cv2.rectangle(taskImg2, (int(self.width2/3),int(0.1*self.height2)),(int(2*self.width2/3),self.height2),(255,255,255),-1);
            cv2.rectangle(taskImg2, (int(self.width2/3),int(0.9*self.height2)),(int(2*self.width2/3),self.height2),(255,0,0),-1);
            percentTarget = 30; #in percentage
            self.drawTarget(taskImg1,taskImg2,percentTarget);
            target_reached = 0;
            t0 = 0;
            t1 = 0;
            while(1):
                task2 = taskImg1.copy();
                task3 = taskImg2.copy();
                self.gripperVal();
                current_pos = (self.val-self.init)*1.0/(self.maxVal - self.init);
                if current_pos<0:
                    current_pos = 0;
                if current_pos >1:
                    current_pos = 1;
                rect_height1 = current_pos*(0.8*self.height1);
                rect_height2 = current_pos*(0.8*self.height2);
                #print rect_height1, rect_height2;
                cv2.rectangle(task2, (int(5*self.width1/11),int(0.9*self.height1-rect_height1)),(int(6*self.width1/11),int(0.9*self.height1)),(255,0,0),-1);
                cv2.rectangle(task3, (int(4*self.width2/9),int(0.9*self.height2-rect_height2)),(int(5*self.width2/9),int(0.9*self.height2)),(255,0,0),-1);
                cv2.imshow("display",task2);
                cv2.imshow("operator",task3);
                if cv2.waitKey(5)==27:
                    trialNo = totalTrials+1;
                    break;
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
            if trialNo<=totalTrials:
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
    try:
        obj.gripperInit();
        print obj.init;
        obj.getGripperMax();
        obj.gripperTask(2);
        cv2.destroyAllWindows();
        obj.mp.close();

    except:
        print ValueError;
        cv2.destroyAllWindows();
        obj.mp.close();
