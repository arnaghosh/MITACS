#TO DO:-

import numpy as np
import cv2, sys, os, time, win32api, wx, threading, win32gui
import win32ui, win32con, re
from libmpdev import *
import matplotlib.pyplot as plt

#these functions and variables are to write keystrokes to the Spike window
whndl=None;
def callback(hwnd,hwnds):
    if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
        hwnds[win32gui.GetClassName(hwnd)] = hwnd
    return True

def find_window_callback(hwnd, param):
    global whndl
    wildcard = param;
    #wndl = params[1];
    if re.match(wildcard,str(win32gui.GetWindowText(hwnd)))!=None:
        whndl = hwnd;
#this is where the functions end.

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
            if self.exit==1:
                break;
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
            self.globalDataValues = np.append(self.globalDataValues,samples[0]);
            self.lastDataValue = self.globalDataValues[len(self.globalDataValues)-1];
            self.globalTrialON = np.append(self.globalTrialON,self.trialON);
            self.globalTimeValues = np.append(self.globalTimeValues,(t1-self.t0));
            time.sleep(0.02);
            
        
    def close(self):
        self.exit = 1;
        if self.connection_closed==0:
            self.mp.close();
            self.connection_closed = 1;

class triggerThread(threading.Thread):
    def __init__(self,threadID,name):
        threading.Thread.__init__(self);
        print "trThread start";
        self.threadID = threadID;
        self.name = name;
        self.trigger = 0;
        self.portAddress=0x0D00 ;
        win32gui.EnumWindows(find_window_callback,".*Notepad.*");
        self.whndl = whndl;
        print self.whndl
        #self.whndl = win32gui.FindWindowEx(0,0,None, 'Untitled - Notepad');
        self.hwnds = {};
        win32gui.EnumChildWindows(self.whndl,callback,self.hwnds)
        self.whndl = self.hwnds['Edit']
        self.wnd = win32ui.CreateWindowFromHandle(self.whndl);
        
    
    def run(self):
        while(1):
            if self.trigger!=0:
                self.wnd.SendMessage(win32con.WM_CHAR, ord(str(self.trigger)),0); #send keypress here.-> self.trigger value
                #write to parallel port here. -> self.trigger value.
                self.trigger = 0;

class Present_PERFORM_hold:
    app = wx.App(False);
    sizes = [wx.Display(i).GetGeometry().GetSize() for i in range(wx.Display.GetCount())]
    width1 = sizes[wx.Display.GetCount()-1].GetWidth();
    height1 = sizes[wx.Display.GetCount()-1].GetHeight();
    width2 = sizes[0].GetWidth();
    height2 = sizes[0].GetHeight();

    def init(self, fname):
        self.filename = fname;
        cv2.namedWindow("display");
        cv2.namedWindow("operator");
        self.basImg1 = np.zeros((self.height1,self.width1,3),dtype=np.uint8);
        self.basImg2 = np.zeros((self.height2,self.width2,3),dtype=np.uint8);
        cv2.imshow("display",self.basImg1);
        cv2.imshow("operator",self.basImg2);
        self.val = 0;
        self.constMax = 10;
        self.displayMaxForTask = 30.0 #in percent MVC
        self.constDummyTime = 0;#2; #in seconds = Tr = 2seconds.
        self.maxVal = -100;
        self.init = 0;
        #self.mp = MP150();
        self.dataValues = np.array([]);
        self.timeValues = np.array([]);

    def gripperInitVal(self, dThread):
        for i in range(100):
            self.gripperVal(dThread);
            randomValue = self.val;
            cv2.waitKey(15);
            self.gripperVal(dThread);
        self.init = self.val;
        
    def gripperVal(self, dThread):
        if len(dThread.globalDataValues)>=1:
            self.val = dThread.lastDataValue;
        else:
            self.val = -1.4;

    def gripperInit(self, dThread):
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
        self.gripperInitVal(dThread);
        cv2.imshow("display",self.basImg1);
        cv2.imshow("operator",self.basImg2);

    def getGripperMax(self, dThread):
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
            self.gripperVal(dThread);
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
        percentTarget_scaled = percentTarget*100/self.displayMaxForTask; 
        height1, width1, ch1 = img1.shape;
        height2, width2, ch2 = img2.shape;
        H = percentTarget_scaled; #change initial value to allow target to rise or appear directly.
        h1 = H*0.7*height1/100;
        h2 = H*0.7*height2/100;
        cv2.rectangle(img1,(int(2*width1/5),int(0.8*height1-h1)),(int(3*width1/5),int(0.8*height1)),(0,0,255),-1);
        cv2.rectangle(img2,(int(width2/3),int(0.8*height2-h2)),(int(2*width2/3),int(0.8*height2)),(0,0,255),-1);
        cv2.imshow("display",img1);
        cv2.imshow("operator",img2);
        cv2.waitKey(10);
        
    def gripperTask(self, totalTrials, dThread, trThread):
        jitter_time_array = np.loadtxt("data\\Jitter_time.txt");
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
        
        while( trialNo<= totalTrials):
            task2 = self.basImg1.copy();
            task3 = self.basImg2.copy();
            cv2.putText(task2, "READY",(int(2*self.width1/5),int(self.height1/3)),cv2.FONT_HERSHEY_PLAIN,6,(255,255,255),3);
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
            cv2.putText(task2, "SET",(int(2*self.width1/5),int(self.height1/3)),cv2.FONT_HERSHEY_PLAIN,6,(255,255,255),3);
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
            cv2.putText(task2, "GO",(int(2*self.width1/5),int(self.height1/3)),cv2.FONT_HERSHEY_PLAIN,6,(255,255,255),3);
            cv2.putText(task3, "GO",(int(2*self.width2/5),int(self.height2/3)),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),3);
            cv2.imshow("display",task2);
            cv2.imshow("operator",task3);
            t03 = time.time();
            t0_2 = time.clock();
            t1_2 = time.clock();
            while((t1_2 - t0_2)*1000<=500):
                t1_2 = time.clock();
                cv2.waitKey(10);
            #if trialNo==1:
                #while(1):
                    #if cv2.waitKey(10)==61:
                        #time.sleep(4*self.constDummyTime+0.001);
                        #break;
            taskImg1 = self.basImg1.copy();
            taskImg2 = self.basImg2.copy();
            cv2.rectangle(taskImg1, (int(2*self.width1/5),int(0.1*self.height1)),(int(3*self.width1/5),int(0.9*self.height1)),(255,255,255),-1);
            cv2.rectangle(taskImg1, (int(2*self.width1/5),int(0.8*self.height1)),(int(3*self.width1/5),int(0.9*self.height1)),(255,0,0),-1);
            cv2.rectangle(taskImg2, (int(self.width2/3),int(0.1*self.height2)),(int(2*self.width2/3),int(0.9*self.height2)),(255,255,255),-1);
            cv2.rectangle(taskImg2, (int(self.width2/3),int(0.8*self.height2)),(int(2*self.width2/3),int(0.9*self.height2)),(255,0,0),-1);
            percentTarget = 15; #in percentage
            self.drawTarget(taskImg1,taskImg2,percentTarget);
            t01 = time.time();
            trThread.trigger = 1;
            dThread.trialON = 1;
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
                if (t11-t01)> 3.5:
                    break;
            trThread.trigger = 2;
            dThread.trialON = 0;
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
        self.AllDatafilename = folder_name+self.filename+"_allData.txt";
        self.filename = folder_name+self.filename+".txt";
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
        ref = [0.15*(self.maxVal-self.init)]*len(t1);
        labels.append(plt.plot(t1,ref,label='Target'));
        plt.legend(loc='best');
        plt.xlabel('Time');
        plt.ylabel('Gripper Value');
        plt.show();
        plt.cla();
        labels = [];
        print len(dThread.globalDataValues), len(dThread.globalTrialON), len(dThread.globalTimeValues);
        dThread.globalDataValues = dThread.globalDataValues - self.init;
        dThread.globalTrialON = dThread.globalTrialON*(0.15*(self.maxVal-self.init));
        labels.append(plt.plot(dThread.globalTimeValues,dThread.globalDataValues,label="Gripper data"));
        labels.append(plt.plot(dThread.globalTimeValues,dThread.globalTrialON,label="Target shown"));
        plt.legend(loc='best');
        plt.xlabel('Time');
        plt.ylabel('Analog Value in gripper scale');
        plt.show();
                
    
if __name__=='__main__':
    fname = raw_input("Enter filename to be saved : ");
    dThread = dataThread(1,"BIOPAC");
    trThread = triggerThread(2,"Trigger");
    obj = Present_PERFORM_hold();
    obj.init(fname);
    #try:
    dThread.t0 = time.clock();
    dThread.start();
    trThread.start();
    obj.gripperInit(dThread);
    print obj.init;
    obj.getGripperMax(dThread);
    #print obj.maxVal;
    T_start = time.clock();
    obj.gripperTask(5,dThread,trThread);
    T_end = time.clock();
    dThread.exit = 1;
    dThread.close();
    print (T_end-T_start);
    cv2.destroyAllWindows();
    obj.plotGripperData(dThread);
        

    #except:
        #print ValueError;
        #cv2.destroyAllWindows();
        #obj.mp.close();
