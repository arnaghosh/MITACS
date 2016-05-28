#TO DO:-

import numpy as np
import cv2, sys, os, time, win32api, wx, threading
from libmpdev import *
import matplotlib.pyplot as plt

globalDataValues = np.array([]);
globalTimeValues = np.array([]);
globalTrialON = np.array([]);
lastDataValue = -1.4;
t0 = 0;

class dataThread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self);
        self.threadID = threadID;
        self.name = name;
        self.mp = MP150();
        self.trialON = 0;
        self.exit = 0;
        self.pause = 0;

    def run(self):
        global globalDataValues, globalTimeValues, globalTrialON, t0, lastDataValue
        while(1):
            if self.pause ==1:
                time.sleep(1);
                self.pause = 0;
                t0 = time.clock();
            t1 = time.clock();
            samples = self.mp.sample();
            #print len(samples);
            globalDataValues = np.append(globalDataValues,samples[0]);
            lastDataValue = globalDataValues[len(globalDataValues)-1];
            globalTrialON = np.append(globalTrialON,self.trialON);
            globalTimeValues = np.append(globalTimeValues,(t1-t0));
            time.sleep(0.02);
            if self.exit==1:
                break;

    def close(self):
        self.mp.close();

class Present_PERFORM:
    app = wx.App(False);
    sizes = [wx.Display(i).GetGeometry().GetSize() for i in range(wx.Display.GetCount())]
    width1 = sizes[1].GetWidth();
    height1 = sizes[1].GetHeight();
    width2 = sizes[0].GetWidth();
    height2 = sizes[0].GetHeight();

    def init(self):
        self.filename = raw_input("Enter filename to be saved : ");
        cv2.namedWindow("display");
        cv2.namedWindow("operator");
        self.basImg1 = np.zeros((self.height1,self.width1,3),dtype=np.uint8);
        self.basImg2 = np.zeros((self.height2,self.width2,3),dtype=np.uint8);
        cv2.imshow("display",self.basImg1);
        cv2.imshow("operator",self.basImg2);
        self.val = 0;
        self.constMax = 6;
        self.constBufferTime = 0; #in seconds
        self.maxVal = -100;
        self.init = 0;
        #self.mp = MP150();
        self.dataValues = np.array([]);
        self.timeValues = np.array([]);

    def gripperInitVal(self):
        for i in range(100):
            self.gripperVal();
            randomValue = self.val;
            cv2.waitKey(15);
            self.gripperVal();
        self.init = self.val;
        
    def gripperVal(self):
        if len(globalDataValues)>=1:
            self.val = lastDataValue;
        else:
            self.val = -1.4;

    def gripperInit(self):
        init2 = self.basImg1.copy();
        init3 = self.basImg2.copy();
        cv2.putText(init2, "Release the gripper and relax",(int(self.width1/5),int(self.height1/3)),cv2.FONT_HERSHEY_PLAIN,6,(255,255,255),3);
        cv2.putText(init3, "Press Enter when ready",(int(self.width2/5),int(self.height2/3)),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),3);
        cv2.imshow("display",init2);
        cv2.waitKey(3000);
        cv2.imshow("operator",init3);
        while(1):            
            if cv2.waitKey(15)==13:
                break;
        self.gripperInitVal();
        cv2.imshow("display",self.basImg1);
        cv2.imshow("operator",self.basImg2);

    def getGripperMax(self):
        max2 = self.basImg1.copy();
        max3 = self.basImg2.copy();
        cv2.putText(max2, "Get ready to Squeeze as hard as you ",(int(self.width1/10),int(self.height1/3)),cv2.FONT_HERSHEY_PLAIN,6,(255,255,255),3);
        cv2.putText(max2, "can for 5 seconds",(int(self.width1/4),int(self.height1/2)),cv2.FONT_HERSHEY_PLAIN,6,(255,255,255),3);
        cv2.putText(max3, "Press Enter when ready",(int(self.width2/5),int(self.height2/3)),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),3);
        cv2.imshow("display",max2);
        cv2.waitKey(2000);
        cv2.imshow("operator",max3);
        while(1):
            if cv2.waitKey(30)==13:
                break;
        max2 = self.basImg1.copy();
        max3 = self.basImg2.copy();
        cv2.putText(max2, "READY",(int(2*self.width1/5),int(self.height1/3)),cv2.FONT_HERSHEY_PLAIN,6,(255,255,255),3);
        cv2.putText(max3, "READY",(int(2*self.width2/5),int(self.height2/3)),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),3);
        cv2.imshow("display",max2);
        cv2.imshow("operator",max3);
        cv2.waitKey(1000);
        max2 = self.basImg1.copy();
        max3 = self.basImg2.copy();
        cv2.putText(max2, "SET",(int(2*self.width1/5),int(self.height1/3)),cv2.FONT_HERSHEY_PLAIN,6,(255,255,255),3);
        cv2.putText(max3, "SET",(int(2*self.width2/5),int(self.height2/3)),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),3);
        cv2.imshow("display",max2);
        cv2.imshow("operator",max3);
        cv2.waitKey(1000);
        max2 = self.basImg1.copy();
        max3 = self.basImg2.copy();
        cv2.putText(max2, "GO",(int(2*self.width1/5),int(self.height1/3)),cv2.FONT_HERSHEY_PLAIN,6,(255,255,255),3);
        cv2.putText(max3, "GO",(int(2*self.width2/5),int(self.height2/3)),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),3);
        cv2.imshow("display",max2);
        cv2.imshow("operator",max3);
        cv2.waitKey(500);
        maxImg1 = self.basImg1.copy();
        maxImg2 = self.basImg2.copy();
        cv2.rectangle(maxImg1, (int(2*self.width1/5),int(0.1*self.height1)),(int(3*self.width1/5),int(0.9*self.height1)),(255,255,255),-1);
        cv2.rectangle(maxImg2, (int(self.width2/3),int(0.1*self.height2)),(int(2*self.width2/3),int(0.9*self.height2)),(255,255,255),-1);
        cv2.rectangle(maxImg1, (int(2*self.width1/5),int(0.8*self.height1)),(int(3*self.width1/5),int(0.9*self.height1)),(255,0,0),-1);
        cv2.rectangle(maxImg2, (int(self.width2/3),int(0.8*self.height2)),(int(2*self.width2/3),int(0.9*self.height2)),(255,0,0),-1);
        t01 = time.time();
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
            cv2.waitKey(10);
            if self.val>self.maxVal:
                self.maxVal = self.val;
            t1= time.time();
            if (t1-t01)>=5.0:
                break;
        cv2.imshow("display",self.basImg1);
        cv2.imshow("operator",self.basImg2);

    def drawTarget(self,img1,img2,percentTarget):
        percentTarget_scaled = percentTarget*100/60;
        height1, width1, ch1 = img1.shape;
        height2, width2, ch2 = img2.shape;
        H = percentTarget_scaled-1; #change initial value to allow target to rise or appear directly.
        while(H<=percentTarget_scaled):
            h1 = H*0.7*height1/100;
            h2 = H*0.7*height2/100;
            cv2.rectangle(img1,(int(2*width1/5),int(0.8*height1-h1)),(int(3*width1/5),int(0.8*height1)),(0,0,255),-1);
            cv2.rectangle(img2,(int(width2/3),int(0.8*height2-h2)),(int(2*width2/3),int(0.8*height2)),(0,0,255),-1);
            H = H+5;
            cv2.imshow("display",img1);
            cv2.imshow("operator",img2);
            cv2.waitKey(10);
        
    def gripperTask(self, totalTrials, dThread):
        global globalDataValues, globalTimeValues, globalTrialON, t0
        task2 = self.basImg1.copy();
        task3 = self.basImg2.copy();
        cv2.putText(task2, "Squeeze to reach the red target bar ",(int(self.width1/10),int(self.height1/3)),cv2.FONT_HERSHEY_PLAIN,6,(255,255,255),3);
        cv2.putText(task2, "and hold for 3 seconds",(int(self.width1/4),int(self.height1/2)),cv2.FONT_HERSHEY_PLAIN,6,(255,255,255),3);
        cv2.putText(task3, "Press Enter when ready",(int(self.width2/5),int(self.height2/3)),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),3);
        cv2.imshow("display",task2);
        cv2.waitKey(2000);
        cv2.imshow("operator",task3);
        while(1):
            if cv2.waitKey(30)==13:
                break;
        
        trialNo = 1;
        dThread.pause = 1;
        globalDataValues = np.empty(0);
        globalTimeValues = np.empty(0);
        globalTrialON = np.empty(0);
        
        while( trialNo<= totalTrials):
            task2 = self.basImg1.copy();
            task3 = self.basImg2.copy();
            cv2.putText(task2, "READY",(int(2*self.width1/5),int(self.height1/3)),cv2.FONT_HERSHEY_PLAIN,6,(255,255,255),3);
            cv2.putText(task3, "READY",(int(2*self.width2/5),int(self.height2/3)),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),3);
            cv2.imshow("display",task2);
            cv2.imshow("operator",task3);
            cv2.waitKey(1000);
            task2 = self.basImg1.copy();
            task3 = self.basImg2.copy();    
            cv2.putText(task2, "SET",(int(2*self.width1/5),int(self.height1/3)),cv2.FONT_HERSHEY_PLAIN,6,(255,255,255),3);
            cv2.putText(task3, "SET",(int(2*self.width2/5),int(self.height2/3)),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),3);
            cv2.imshow("display",task2);
            cv2.imshow("operator",task3);
            cv2.waitKey(1000);
            task2 = self.basImg1.copy();
            task3 = self.basImg2.copy(); 
            cv2.putText(task2, "GO",(int(2*self.width1/5),int(self.height1/3)),cv2.FONT_HERSHEY_PLAIN,6,(255,255,255),3);
            cv2.putText(task3, "GO",(int(2*self.width2/5),int(self.height2/3)),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),3);
            cv2.imshow("display",task2);
            cv2.imshow("operator",task3);
            t03 = time.time();
            cv2.waitKey(500);
            if trialNo==1:
                while(1):
                    if cv2.waitKey(10)==61:
                        break;
            taskImg1 = self.basImg1.copy();
            taskImg2 = self.basImg2.copy();
            cv2.rectangle(taskImg1, (int(2*self.width1/5),int(0.1*self.height1)),(int(3*self.width1/5),int(0.9*self.height1)),(255,255,255),-1);
            cv2.rectangle(taskImg1, (int(2*self.width1/5),int(0.8*self.height1)),(int(3*self.width1/5),int(0.9*self.height1)),(255,0,0),-1);
            cv2.rectangle(taskImg2, (int(self.width2/3),int(0.1*self.height2)),(int(2*self.width2/3),int(0.9*self.height2)),(255,255,255),-1);
            cv2.rectangle(taskImg2, (int(self.width2/3),int(0.8*self.height2)),(int(2*self.width2/3),int(0.9*self.height2)),(255,0,0),-1);
            percentTarget = 30; #in percentage
            self.drawTarget(taskImg1,taskImg2,percentTarget);
            t01 = time.time();
            dThread.trialON = 1;
            while(1):
                task2 = taskImg1.copy();
                task3 = taskImg2.copy();
                self.gripperVal();
                current_pos = (self.val-self.init)*1.0/(self.maxVal - self.init);
                current_pos_scaled = current_pos*1.0/0.6;
                if current_pos_scaled<0:
                    current_pos_scaled = 0;
                if current_pos_scaled >1:
                    current_pos_scaled = 1;
                    
                rect_height1 = current_pos_scaled*(0.7*self.height1);
                rect_height2 = current_pos_scaled*(0.7*self.height2);
                #print rect_height1, rect_height2;
                cv2.rectangle(task2, (int(5*self.width1/11),int(0.8*self.height1-rect_height1)),(int(6*self.width1/11),int(0.8*self.height1)),(255,0,0),-1);
                cv2.rectangle(task3, (int(4*self.width2/9),int(0.8*self.height2-rect_height2)),(int(5*self.width2/9),int(0.8*self.height2)),(255,0,0),-1);
                cv2.imshow("display",task2);
                cv2.imshow("operator",task3);
                if cv2.waitKey(10)==27:
                    trialNo = totalTrials+1;
                    break;
                t11 = time.time();
                if (t11-t01)> 3.0:
                    break;
            dThread.trialON = 0;
            s = "Trial "+str(trialNo)+" done.";
            trialNo = trialNo + 1;
            task2 = self.basImg1.copy();
            task3 = self.basImg2.copy();            
            
            cv2.putText(task3, s,(int(self.width2/5),int(self.height2/3)),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),3);
            cv2.imshow("display",task2);
            cv2.imshow("operator",task3);
            jitter_time = int(np.random.uniform(2500));
            t_0 = time.clock();
            t_1 = time.clock();
            while((t_1 - t_0)*1000<=jitter_time):
                t_1 = time.clock();
                cv2.waitKey(10);
        dThread.exit = 1;
        dThread.close();
        self.filename = "data\\"+self.filename+".txt";
        for i in range(len(globalDataValues)):
            if i==0:
                continue;
            if globalTrialON[i]==1 and globalTrialON[i-1]==0:
                t_ref = globalTimeValues[i];
            if globalTrialON[i]==1:
                self.dataValues = np.append(self.dataValues,globalDataValues[i]);
                self.timeValues = np.append(self.timeValues,globalTimeValues[i]-t_ref);

        self.dataValues = self.dataValues - self.init;
        np.savetxt(self.filename,(self.dataValues,self.timeValues),newline='\n');
            
    def plotGripperData(self):
        global globalDataValues, globalTrialON
        d = [];
        t = [];
        t1 = [];
        trialNo =1;
        labels=[];
        for i in range(len(self.dataValues)):
            d_temp = self.dataValues[i];
            t_temp = self.timeValues[i];
            if i==0:
                d.append(d_temp);
                t.append(t_temp);
                continue;
            if i==len(self.dataValues)-1:
                d.append(d_temp);
                t.append(t_temp);
                s = 'Trial '+str(trialNo);
                labels.append(plt.plot(t,d,label=s));
                continue;
            if t_temp<3.0 and t_temp>0.001:
                d.append(d_temp);
                t.append(t_temp);
            else:
                if t_temp>=3.0:
                    d.append(d_temp);
                    t.append(t_temp);
                    d_temp = self.dataValues[i+1];
                    t_temp = self.timeValues[i+1];
                    i=i+1;
                print d_temp,t_temp;
                s = 'Trial '+str(trialNo);
                labels.append(plt.plot(t,d,label=s));
                d=[d_temp];
                t1 = t;
                t=[t_temp];
                trialNo = trialNo+1;
        ref = [0.3*(self.maxVal-self.init)]*len(t1);
        labels.append(plt.plot(t1,ref,label='Target'));
        plt.legend(loc='best');
        plt.xlabel('Time');
        plt.ylabel('Gripper Value');
        plt.show();
        plt.cla();
        labels = [];
        print len(globalDataValues), len(globalTrialON), len(globalTimeValues);
        globalDataValues = globalDataValues - self.init;
        globalTrialON = globalTrialON*(0.3*(self.maxVal-self.init));
        labels.append(plt.plot(globalTimeValues,globalDataValues,label="Gripper data"));
        labels.append(plt.plot(globalTimeValues,globalTrialON,label="Target shown"));
        plt.legend(loc='best');
        plt.xlabel('Time');
        plt.ylabel('Analog Value in gripper scale');
        plt.show();
                
    
if __name__=='__main__':
    dThread = dataThread(1,"BIOPAC");
    obj = Present_PERFORM();
    obj.init();
    #try:
    t0 = time.clock();
    dThread.start();
    obj.gripperInit();
    print obj.init;
    obj.getGripperMax();
    T_start = time.clock();
    obj.gripperTask(50,dThread);
    T_end = time.clock();
    print (T_end-T_start);
    cv2.destroyAllWindows();
    obj.plotGripperData();
        

    #except:
        #print ValueError;
        #cv2.destroyAllWindows();
        #obj.mp.close();
