from PyDAQmx import *
from PyDAQmx.DAQmxCallBack import *
import matplotlib.pyplot as plt
import time
import numpy as np
import threading, time, cv2
from drawnow import *

mutex=threading.Lock();

class dataCollect(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self);
        self.threadID = threadID;
        self.name = name;
        self.dataArray = np.array([]);
        self.timeArray = np.array([]);
        DAQmxResetDevice('dev1');
        self.taskhandle = TaskHandle();
        DAQmxCreateTask("",byref(self.taskhandle));
        DAQmxCreateAIVoltageChan(self.taskhandle,"Dev1/ai0","",DAQmx_Val_Cfg_Default, -10,10,DAQmx_Val_Volts,None);
        DAQmxCfgSampClkTiming(self.taskhandle,"",50,DAQmx_Val_Rising, DAQmx_Val_ContSamps,100)
        self.exit = 0;

    def run(self):
        DAQmxStartTask(self.taskhandle);
        while(1):
            reads = int32()
            temp = np.zeros((1),dtype=np.float64);
            t1= time.clock();
            DAQmxReadAnalogF64(self.taskhandle,1,10,DAQmx_Val_GroupByChannel,temp,10000,byref(reads),None);
            t12 = time.clock();
            #print "time diff",(t12-t1);
            mutex.acquire();
            #print temp
            #print "reads", reads
            self.dataArray = np.append(self.dataArray,temp[len(temp)-1]);
            self.timeArray = np.append(self.timeArray,(t1-t0));
            mutex.release();
            #time.sleep(0.02);
            if self.exit==1:
                if self.taskhandle:
                    print self.taskhandle;
                    #DAQmxStopTask(self.taskhandle);
                break;

    def close(self):
        if self.taskhandle:
            DAQmxClearTask(self.taskhandle);
    

class presentThread:
    def __init__(self, threadID, name):
        self.threadID = threadID;
        self.name = name;
        self.bg = np.zeros((640,480,3),dtype=np.uint8);
        cv2.imshow("disp",self.bg);        
        self.exit = 0;
        self.data = [];
        self.time = [];

    def makeFig(self):
        plt.title("Live Plot");
        plt.grid(True);
        plt.ylabel("Gripper Data percent");
        plt.xlabel("Time");
        plt.plot(self.time,self.data,label='Real Time BIOPAC gripper');
        plt.legend(loc='best');
    
    def run(self, dThread):
        mutex.acquire();
        if len(dThread.dataArray)==0:
            val = 0;
            self.data.append(val);
            self.time.append(0);
        else:
            val = dThread.dataArray[len(dThread.dataArray)-1];
            self.data.append(val);
            self.time.append(dThread.timeArray[len(dThread.timeArray)-1]);
        mutex.release();
        val_ = int(255*(val+2)/10);
        if val_<0:
            val_ = 0;
        if val_ > 255:
            val_ = 255;
        #print "presenting %s" %(val_);        
        cv2.rectangle(self.bg,(100,100),(200,200),(val_,val_,val_),-1);
        cv2.imshow("disp",self.bg);
        
        if cv2.waitKey(10)==27:
            return 0;

    def update(self, dThread):
        mutex.acquire();
        if len(dThread.dataArray)==0:
            val = 0;
            self.data.append(val);
            self.time.append(0);
        else:
            val = dThread.dataArray[len(dThread.dataArray)-1];
            self.data.append(val);
            self.time.append(dThread.timeArray[len(dThread.timeArray)-1]);
        mutex.release();
        val_ = int(255*(val+2)/10);
        print val_, val
        if val_<0:
            val_ = 0;
        if val_ > 255:
            val_ = 255;
        #print "presenting %s" %(val_);        
        cv2.rectangle(self.bg,(100,100),(200,200),(val_,val_,val_),-1);
        cv2.imshow("disp",self.bg);
        if cv2.waitKey(10)==27:
            return 0;
        drawnow(self.makeFig);
        plt.pause(0.00001);
        if (len(self.data)>100):
            self.data.pop(0);
            self.time.pop(0);
        return 1;


if __name__ == '__main__':    
    dThread = dataCollect(1,"BIOPAC");
    pThread = presentThread(2, "present");
    t0 = time.clock();
    pThread.run(dThread);
    dThread.start();
    while(1):
        #dThread.update();
        r = pThread.update(dThread);
        if r==0:
            dThread.exit =1;
            break;
    dThread.close();
    T = dThread.timeArray.copy();
    D = dThread.dataArray.copy();
    for i in range(len(T)-1):
        j = i+1;
        #print (T[j]-T[i]);
        if j==len(T)-1:
            break;
        if D[j]==D[i]:
            D[j]=(D[i]+D[j+1])/2;
    plt.plot(dThread.timeArray,dThread.dataArray, label='Recorded BIOPAC gripper');
    plt.legend(loc='best');
    plt.show();
    plt.plot(T,D);
    plt.show();
