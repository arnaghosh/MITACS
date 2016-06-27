import numpy as np
import cv2, sys, os, time, win32api, wx, threading, win32gui
import win32ui, win32con, re, pywinauto, win32com.client
from libmpdev import *
import matplotlib.pyplot as plt

mutex = threading.Lock();
class dataThread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self);
        print "dThread start";
        self.threadID = threadID;
        self.name = name;
        self.mp = MP150();
        self.trialON = 0;
        self.exit = 0;
        self.pause = 0;
        self.no_action = 0;
        self.connection_closed = 0;
        self.globalDataValues = np.array([]);
        self.globalTimeValues = np.array([]);
        self.globalTrialON = np.array([]);
        self.lastDataValue = -1.4;
        self.t0 = 0;

    def run(self):
        while(1):
            t1= time.clock();
            mutex.acquire();
            #print temp
            if self.no_action==1:
                continue;
            if self.pause ==1:
                self.pause = 0;
                self.globalDataValues = np.empty(0);
                self.globalTimeValues = np.empty(0);
                self.globalTrialON = np.empty(0);
                self.t0 = time.clock();
            t1 = time.clock();
            samples = self.mp.sample();
            #print len(samples);
            self.globalDataValues = np.append(self.globalDataValues,samples[0]);  #temp[len(temp)-1]
            self.lastDataValue = self.globalDataValues[len(self.globalDataValues)-1];
            self.globalTrialON = np.append(self.globalTrialON,self.trialON);
            self.globalTimeValues = np.append(self.globalTimeValues,(t1-self.t0));
            time.sleep(0.02);
            mutex.release();
            if self.exit==1:
                break;
        print "dThread closing";
            
        
    def close(self):
        self.exit = 1;
        if self.connection_closed==0:
            self.connection_closed = 1;
            self.mp.close();


class holdTask:
    app = wx.App(False);
    sizes = [wx.Display(i).GetGeometry().GetSize() for i in range(wx.Display.GetCount())]
    width1 = sizes[wx.Display.GetCount()-1].GetWidth();
    height1 = sizes[wx.Display.GetCount()-1].GetHeight();
    width11 = sizes[0].GetWidth();
    height11 = sizes[0].GetHeight();
    width2 = sizes[0].GetWidth()/2;
    height2 = sizes[0].GetHeight()/2;

    def init(self, fname, timeAfterExercise):
        self.filename = fname;
        self.timeAfterExercise = timeAfterExercise;
        cv2.namedWindow("display");
        cv2.namedWindow("operator");
        self.basImg1 = np.zeros((self.height1,self.width1,3),dtype=np.uint8);
        self.basImg11 = np.zeros((self.height11,self.width11,3),dtype=np.uint8);
        self.basImg2 = np.zeros((self.height2,self.width2,3),dtype=np.uint8);
        cv2.imshow("display",self.basImg1);
        cv2.imshow("operator",self.basImg2);
        self.val = 0;
        self.constMax = 10;
        self.constTarget = 15.0; #in percent MVC
        self.displayMaxForTask = 30.0 #in percent MVC
        self.constDummyTime = 2; #in seconds = Tr = 2seconds.
        self.maxVal = -100;
        self.init = 0;
        #self.mp = MP150();
        self.dataValues = np.array([]);
        self.timeValues = np.array([]);

    def gripperInitVal(self, dThread):
        for i in range(100):
            self.gripperVal(dThread);
            randomValue = self.val;
            cv2.waitKey(5);
            self.gripperVal(dThread);
        self.init = self.val;
        
    def gripperVal(self, dThread):
        mutex.acquire();
        if len(dThread.globalDataValues)>=1:
            self.val = dThread.lastDataValue;
        else:
            self.val = -1.4;
        mutex.release();

    def gripperInit(self, dThread):
        init1 = self.basImg11.copy();
        init2 = self.basImg1.copy();
        init3 = self.basImg2.copy();
        cv2.putText(init1, "Release the gripper ",(int(self.width11/10),int(self.height11/3)),cv2.FONT_HERSHEY_PLAIN,6,(255,255,255),2);
        cv2.putText(init1, "and relax",(int(self.width11/3),int(2*self.height11/3)),cv2.FONT_HERSHEY_PLAIN,6,(255,255,255),2);
        init2[int((self.height1-self.height11)/2):int((self.height1+self.height11)/2),int((self.width1-self.width11)/2):int((self.width1+self.width11)/2)] = init1;
        #cv2.putText(init2, "Release the gripper and relax",(int(self.width2/5),int(self.height2/3)),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),3);
        cv2.putText(init3, "Press Enter when ready",(int(self.width2/5),int(self.height2/3)),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),3);
        cv2.imshow("display",init2);
        cv2.waitKey(1000);
        cv2.imshow("operator",init3);
        while(1):            
            if cv2.waitKey(15)==13:
                break;
        self.gripperInitVal(dThread);
        cv2.imshow("display",self.basImg1);
        cv2.imshow("operator",self.basImg2);

    def getGripperMax(self, dThread):
        max1 = self.basImg11.copy();
        max2 = self.basImg1.copy();
        max3 = self.basImg2.copy();
        cv2.putText(max1, "Get ready to Squeeze ",(int(self.width11/8),int(self.height11/4)),cv2.FONT_HERSHEY_PLAIN,6,(255,255,255),2);
        cv2.putText(max1, "as hard as you",(int(self.width11/6),int(self.height11/2)),cv2.FONT_HERSHEY_PLAIN,6,(255,255,255),2);
        cv2.putText(max1, "can for 5 sec",(int(self.width11/6),int(3*self.height11/4)),cv2.FONT_HERSHEY_PLAIN,6,(255,255,255),2);
        max2[int((self.height1-self.height11)/2):int((self.height1+self.height11)/2),int((self.width1-self.width11)/2):int((self.width1+self.width11)/2)] = max1;
        cv2.putText(max3, "Press Enter when ready",(int(self.width2/5),int(self.height2/3)),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),3);
        cv2.imshow("display",max2);
        cv2.waitKey(2000);
        cv2.imshow("operator",max3);
        while(1):
            if cv2.waitKey(30)==13:
                break;
        max1 = self.basImg11.copy();
        max2 = self.basImg1.copy();
        max3 = self.basImg2.copy();
        cv2.putText(max1, "READY",(int(2*self.width11/4),int(self.height11/3)),cv2.FONT_HERSHEY_PLAIN,6,(255,255,255),2);
        max2[int((self.height1-self.height11)/2):int((self.height1+self.height11)/2),int((self.width1-self.width11)/2):int((self.width1+self.width11)/2)] = max1;
        cv2.putText(max3, "READY",(int(2*self.width2/5),int(self.height2/3)),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),3);
        cv2.imshow("display",max2);
        cv2.imshow("operator",max3);
        cv2.waitKey(1000);
        max1 = self.basImg11.copy();
        max2 = self.basImg1.copy();
        max3 = self.basImg2.copy();
        cv2.putText(max1, "SET",(int(2*self.width11/4),int(self.height11/3)),cv2.FONT_HERSHEY_PLAIN,6,(255,255,255),2);
        max2[int((self.height1-self.height11)/2):int((self.height1+self.height11)/2),int((self.width1-self.width11)/2):int((self.width1+self.width11)/2)] = max1;
        cv2.putText(max3, "SET",(int(2*self.width2/5),int(self.height2/3)),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),3);
        cv2.imshow("display",max2);
        cv2.imshow("operator",max3);
        cv2.waitKey(1000);
        max1 = self.basImg11.copy();
        max2 = self.basImg1.copy();
        max3 = self.basImg2.copy();
        cv2.putText(max1, "GO",(int(2*self.width11/4),int(self.height11/3)),cv2.FONT_HERSHEY_PLAIN,6,(255,255,255),2);
        max2[int((self.height1-self.height11)/2):int((self.height1+self.height11)/2),int((self.width1-self.width11)/2):int((self.width1+self.width11)/2)] = max1;
        cv2.putText(max3, "GO",(int(2*self.width2/5),int(self.height2/3)),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),3);
        cv2.imshow("display",max2);
        cv2.imshow("operator",max3);
        cv2.waitKey(500);
        maxImg11 = self.basImg11.copy();
        maxImg1 = self.basImg1.copy();
        maxImg2 = self.basImg2.copy();
        cv2.rectangle(maxImg11, (int(2*self.width11/5),int(0.1*self.height11)),(int(3*self.width11/5),int(0.9*self.height11)),(255,255,255),-1);
        cv2.rectangle(maxImg2, (int(self.width2/3),int(0.1*self.height2)),(int(2*self.width2/3),int(0.9*self.height2)),(255,255,255),-1);
        cv2.rectangle(maxImg11, (int(2*self.width11/5),int(0.8*self.height11)),(int(3*self.width11/5),int(0.9*self.height11)),(255,0,0),-1);
        cv2.rectangle(maxImg2, (int(self.width2/3),int(0.8*self.height2)),(int(2*self.width2/3),int(0.9*self.height2)),(255,0,0),-1);
        maxImg1[int((self.height1-self.height11)/2):int((self.height1+self.height11)/2),int((self.width1-self.width11)/2):int((self.width1+self.width11)/2)] = maxImg11;
        t01 = time.time();
        while(1):
            max1 = maxImg11.copy();
            max2 = maxImg1.copy();
            max3 = maxImg2.copy();
            self.gripperVal(dThread);
            rect_height11 = (self.val-self.init)*(0.8*self.height11)/(self.constMax - self.init);
            rect_height2 = (self.val-self.init)*(0.8*self.height2)/(self.constMax - self.init);
            cv2.rectangle(max1, (int(5*self.width11/11),int(0.9*self.height11-rect_height11)),(int(6*self.width11/11),int(0.9*self.height11)),(255,0,0),-1);
            cv2.rectangle(max3, (int(4*self.width2/9),int(0.9*self.height2-rect_height2)),(int(5*self.width2/9),int(0.9*self.height2)),(255,0,0),-1);
            max2[int((self.height1-self.height11)/2):int((self.height1+self.height11)/2),int((self.width1-self.width11)/2):int((self.width1+self.width11)/2)] = max1;
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
        percentTarget_scaled = percentTarget*100/self.displayMaxForTask;
        img11 = img1[int((self.height1-self.height11)/2):int((self.height1+self.height11)/2),int((self.width1-self.width11)/2):int((self.width1+self.width11)/2)];
        height1, width1, ch1 = img1.shape;
        height11, width11, ch11 = img11.shape;
        height2, width2, ch2 = img2.shape;
        H = percentTarget_scaled; #change initial value to allow target to rise or appear directly.
        h11 = H*0.7*height11/100;
        h2 = H*0.7*height2/100;
        cv2.rectangle(img11,(int(2*width11/5),int(0.8*height11-h11)),(int(3*width11/5),int(0.8*height11)),(0,0,255),-1);
        cv2.rectangle(img2,(int(width2/3),int(0.8*height2-h2)),(int(2*width2/3),int(0.8*height2)),(0,0,255),-1);
        img1[int((self.height1-self.height11)/2):int((self.height1+self.height11)/2),int((self.width1-self.width11)/2):int((self.width1+self.width11)/2)] = img11;
        cv2.imshow("display",img1);
        cv2.imshow("operator",img2);
        cv2.waitKey(10);

    def gripperTask(self, totalTrials, dThread):
        t_overhead_start = time.clock();
        jitter_time_array = np.loadtxt("data\\Jitter_time.txt");
        task1 = self.basImg11.copy();
        task2 = self.basImg1.copy();
        task3 = self.basImg2.copy();
        cv2.putText(task1, "Squeeze to reach the ",(int(self.width11/8),int(self.height11/4)),cv2.FONT_HERSHEY_PLAIN,6,(255,255,255),2);
        cv2.putText(task1, "red target bar and",(int(self.width11/6),int(self.height11/2)),cv2.FONT_HERSHEY_PLAIN,6,(255,255,255),2);
        cv2.putText(task1, "hold for 3 seconds",(int(self.width11/6),int(3*self.height11/4)),cv2.FONT_HERSHEY_PLAIN,6,(255,255,255),2);
        task2[int((self.height1-self.height11)/2):int((self.height1+self.height11)/2),int((self.width1-self.width11)/2):int((self.width1+self.width11)/2)] = task1;
        cv2.putText(task3, "Press Enter when ready",(int(self.width2/5),int(self.height2/3)),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),3);
        cv2.imshow("display",task2);
        cv2.waitKey(2000);
        cv2.imshow("operator",task3);
        while(1):
            if cv2.waitKey(30)==13:
                break;
        
        trialNo = 1;
        mutex.acquire();
        dThread.pause = 1;
        mutex.release();
        
        while( trialNo<= totalTrials):
            task2 = self.basImg1.copy();
            task3 = self.basImg2.copy();
            #cv2.putText(task2, "READY",(int(2*self.width1/5),int(self.height1/3)),cv2.FONT_HERSHEY_PLAIN,6,(255,255,255),3);
            cv2.putText(task3, "READY",(int(2*self.width2/5),int(self.height2/3)),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),3);
            cv2.imshow("display",task2);
            cv2.imshow("operator",task3);
            t0_2 = time.clock();
            t1_2 = time.clock();
            while((t1_2 - t0_2)<=1):
                t1_2 = time.clock();
                cv2.waitKey(10);
            task2 = self.basImg1.copy();
            task3 = self.basImg2.copy();    
            #cv2.putText(task2, "SET",(int(2*self.width1/5),int(self.height1/3)),cv2.FONT_HERSHEY_PLAIN,6,(255,255,255),3);
            cv2.putText(task3, "SET",(int(2*self.width2/5),int(self.height2/3)),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),3);
            cv2.imshow("display",task2);
            cv2.imshow("operator",task3);
            t0_2 = time.clock();
            t1_2 = time.clock();
            while((t1_2 - t0_2)<=1):
                t1_2 = time.clock();
                cv2.waitKey(10);
            task2 = self.basImg1.copy();
            task3 = self.basImg2.copy(); 
            #cv2.putText(task2, "GO",(int(2*self.width1/5),int(self.height1/3)),cv2.FONT_HERSHEY_PLAIN,6,(255,255,255),3);
            cv2.putText(task3, "GO",(int(2*self.width2/5),int(self.height2/3)),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),3);
            cv2.imshow("display",task2);
            cv2.imshow("operator",task3);
            t03 = time.time();
            t0_2 = time.clock();
            t1_2 = time.clock();
            while((t1_2 - t0_2)*1000<=500):
                t1_2 = time.clock();
                cv2.waitKey(10);
            if trialNo==1:
                while(1):
                    if cv2.waitKey(10)==61:
                        t0_2 = time.clock();
                        print "overhead=",(t0_2-t_overhead_start);
                        task3 = self.basImg2.copy(); 
                        cv2.putText(task3, "Waiting for Dummies",(int(self.width2/5),int(self.height2/3)),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),3);
                        cv2.imshow("operator",task3);
                        cv2.waitKey(5);
                        t1_2 = time.clock();
                        time.sleep(4*self.constDummyTime+0.001-(t1_2-t0_2));
                        break;
            taskImg1 = self.basImg1.copy();
            taskImg11 = taskImg1[int((self.height1-self.height11)/2):int((self.height1+self.height11)/2),int((self.width1-self.width11)/2):int((self.width1+self.width11)/2)];
            taskImg2 = self.basImg2.copy();
            cv2.rectangle(taskImg11, (int(2*self.width11/5),int(0.1*self.height11)),(int(3*self.width11/5),int(0.9*self.height11)),(255,255,255),-1);
            cv2.rectangle(taskImg11, (int(2*self.width11/5),int(0.8*self.height11)),(int(3*self.width11/5),int(0.9*self.height11)),(255,0,0),-1);
            taskImg1[int((self.height1-self.height11)/2):int((self.height1+self.height11)/2),int((self.width1-self.width11)/2):int((self.width1+self.width11)/2)] = taskImg11;
            cv2.rectangle(taskImg2, (int(self.width2/3),int(0.1*self.height2)),(int(2*self.width2/3),int(0.9*self.height2)),(255,255,255),-1);
            cv2.rectangle(taskImg2, (int(self.width2/3),int(0.8*self.height2)),(int(2*self.width2/3),int(0.9*self.height2)),(255,0,0),-1);
            percentTarget = self.constTarget; #in percentage
            self.drawTarget(taskImg1,taskImg2,percentTarget);
            t01 = time.time();
            mutex.acquire();
            dThread.trialON = 1;
            mutex.release();
            while(1):
                task2 = taskImg1.copy();
                task3 = taskImg2.copy();
                self.gripperVal(dThread);
                current_pos = (self.val-self.init)*1.0/(self.maxVal - self.init);
                current_pos_scaled = current_pos*100.0/self.displayMaxForTask;
                if current_pos_scaled<0:
                    current_pos_scaled = 0;
                if current_pos_scaled >1:
                    current_pos_scaled = 1;
                    
                rect_height1 = current_pos_scaled*(0.7*self.height11);
                rect_height2 = current_pos_scaled*(0.7*self.height2);
                #print rect_height1, rect_height2;
                task1 = task2[int((self.height1-self.height11)/2):int((self.height1+self.height11)/2),int((self.width1-self.width11)/2):int((self.width1+self.width11)/2)];
                cv2.rectangle(task1, (int(5*self.width11/11),int(0.8*self.height11-rect_height1)),(int(6*self.width11/11),int(0.8*self.height11)),(255,0,0),-1);
                task2[int((self.height1-self.height11)/2):int((self.height1+self.height11)/2),int((self.width1-self.width11)/2):int((self.width1+self.width11)/2)] = task1;
                cv2.rectangle(task3, (int(4*self.width2/9),int(0.8*self.height2-rect_height2)),(int(5*self.width2/9),int(0.8*self.height2)),(255,0,0),-1);
                cv2.imshow("display",task2);
                cv2.imshow("operator",task3);
                if cv2.waitKey(10)==27:
                    trialNo = totalTrials+1;
                    mutex.acquire();
                    dThread.trialON = 0;
                    mutex.release();
                    break;
                t11 = time.time();
                if (t11-t01)> 3.5:
                    mutex.acquire();
                    dThread.trialON = 0;
                    mutex.release();
                    break;
            s = "Trial "+str(trialNo)+" done.";
            jitter_time = jitter_time_array[trialNo-1];
            trialNo = trialNo + 1;
            task2 = self.basImg1.copy();
            task3 = self.basImg2.copy();            
            
            cv2.putText(task3, s,(int(self.width2/5),int(self.height2/3)),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),3);
            cv2.imshow("display",task2);
            cv2.imshow("operator",task3);
            t_0 = time.clock();
            t_1 = time.clock();
            while((t_1 - t_0)*1000<=jitter_time):
                t_1 = time.clock();
                cv2.waitKey(10);
        folder_name = "data\\"+self.filename+"\\";
        self.ensure_dir(folder_name);
        self.AllDatafilename = folder_name+self.filename+"_"+self.timeAfterExercise+"_allData.txt";
        self.filename = folder_name+self.filename+"_"+self.timeAfterExercise+".txt";
        mutex.acquire();
        for i in range(len(dThread.globalDataValues)):
            if i==0:
                continue;
            if dThread.globalTrialON[i]==1 and dThread.globalTrialON[i-1]==0:
                t_ref = dThread.globalTimeValues[i];
            if dThread.globalTrialON[i]==1:
                if (dThread.globalTimeValues[i]-t_ref)>3.5 and (self.timeValues[len(self.timeValues)-1]>=3.5):
                    dThread.globalTrialON[i]=0;
                    continue;
                self.dataValues = np.append(self.dataValues,dThread.globalDataValues[i]);
                self.timeValues = np.append(self.timeValues,dThread.globalTimeValues[i]-t_ref);

        self.dataValues = self.dataValues - self.init;
        np.savetxt(self.filename,np.column_stack((self.dataValues,self.timeValues)),newline='\n');
        np.savetxt(self.AllDatafilename,np.column_stack((dThread.globalDataValues,dThread.globalTrialON,dThread.globalTimeValues)),newline='\n');
        mutex.release();
            
    def ensure_dir(self,f):
        d = os.path.dirname(f)
        print os.path.exists(d)
        if not os.path.exists(d):
            os.makedirs(d)

    def plotGripperData(self, dThread):
        d = [];
        t = [];
        t1 = [];
        trialNo =1;
        labels=[];
        already_done = 0;
        for i in range(len(self.dataValues)):
            if already_done==1:
                already_done=0;
                continue;            
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
            if t_temp<3.5 and t_temp>0.001:
                d.append(d_temp);
                t.append(t_temp);
            else:
                if t_temp>=3.5:
                    d.append(d_temp);
                    t.append(t_temp);
                    d_temp = self.dataValues[i+1];
                    t_temp = self.timeValues[i+1];
                    already_done=1;
                #print d_temp,t_temp;
                s = 'Trial '+str(trialNo);
                labels.append(plt.plot(t,d,label=s));
                d=[d_temp];
                t1 = t;
                t=[t_temp];
                trialNo = trialNo+1;
        ref = [self.constTarget*(self.maxVal-self.init)/100]*len(t1);
        labels.append(plt.plot(t1,ref,label='Target'));
        plt.legend(loc='best');
        plt.xlabel('Time');
        plt.ylabel('Gripper Value');
        plt.show();
        plt.cla();
        labels = [];
        print len(dThread.globalDataValues), len(dThread.globalTrialON), len(dThread.globalTimeValues);
        dThread.globalDataValues = dThread.globalDataValues - self.init;
        dThread.globalTrialON = dThread.globalTrialON*(self.constTarget*(self.maxVal-self.init)/100);
        labels.append(plt.plot(dThread.globalTimeValues,dThread.globalDataValues,label="Gripper data"));
        labels.append(plt.plot(dThread.globalTimeValues,dThread.globalTrialON,label="Target shown"));
        plt.legend(loc='best');
        plt.xlabel('Time');
        plt.ylabel('Analog Value in gripper scale');
        plt.show();
                
if __name__=='__main__':
    fname = raw_input("Enter filename to be saved : ");
    dThread = dataThread(1,"BIOPAC");
    timeAfterExercise = 30;
    obj = holdTask();
    obj.init(fname, str(timeAfterExercise));
    #try:
    mutex.acquire();
    dThread.t0 = time.clock();
    dThread.start();
    mutex.release();
    obj.gripperInit(dThread);
    print obj.init;
    obj.getGripperMax(dThread);
    #print obj.maxVal;
    T_start = time.clock();
    obj.gripperTask(5,dThread);
    T_end = time.clock();
    print (T_end-T_start);
    mutex.acquire();
    dThread.exit = 1;
    dThread.close();
    mutex.release();
    cv2.destroyAllWindows();
    obj.plotGripperData(dThread);
    print mutex.locked();
