import threading, time, cv2
import numpy as np
from libmpdev import *
import matplotlib.pyplot as plt
from drawnow import *

globalDataValues = np.array([]);
globalTimeValues = np.array([]);
t0 =0;


class dataThread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self);
        self.threadID = threadID;
        self.name = name;
        self.mp = MP150();
        self.exit = 0;

    def run(self):
        global globalDataValues, globalTimeValues
        while(1):
            t1 = time.clock();
            samples = self.mp.sample();
            #print len(samples);
            globalDataValues = np.append(globalDataValues,100*(samples[0]+1.4)/6);
            globalTimeValues = np.append(globalTimeValues,(t1-t0));
            t11 = time.clock();
            #while(t11-t1<0.021):
            #    t11 = time.clock();
            time.sleep(0.02);
            if self.exit==1:
                break;

    def close(self):
        self.mp.close();

class presentThread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self);
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
    
    def run(self):
        if len(globalDataValues)==0:
            val = 0;
            self.data.append(val);
            self.time.append(0);
        else:
            val = globalDataValues[len(globalDataValues)-1];
            self.data.append(val);
            self.time.append(globalTimeValues[len(globalTimeValues)-1]);
        val_ = int(255*(val)/100);
        if val_<0:
            val_ = 0;
        if val_ > 255:
            val_ = 255;
        #print "presenting %s" %(val_);        
        cv2.rectangle(self.bg,(100,100),(200,200),(val_,val_,val_),-1);
        cv2.imshow("disp",self.bg);
        if cv2.waitKey(10)==27:
            return 0;

    def update(self):
        if len(globalDataValues)==0:
            val = 0;
            self.data.append(val);
            self.time.append(0);
        else:
            val = globalDataValues[len(globalDataValues)-1];
            self.data.append(val);
            self.time.append(globalTimeValues[len(globalTimeValues)-1]);
        val_ = int(255*(val)/100);
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
    dThread = dataThread(1,"BIOPAC");
    pThread = presentThread(2, "present");
    t0 = time.clock();
    dThread.start();
    pThread.start();
    while(1):
        #dThread.update();
        r = pThread.update();
        if r==0:
            dThread.exit =1;
            break;
    dThread.close();
    T = globalTimeValues.copy();
    D = globalDataValues.copy();
    for i in range(len(T)-1):
        j = i+1;
        #print (T[j]-T[i]);
        if j==len(T)-1:
            break;
        if D[j]==D[i]:
            D[j]=(D[i]+D[j+1])/2;
    plt.plot(globalTimeValues,globalDataValues, label='Recorded BIOPAC gripper');
    plt.legend(loc='best');
    plt.show();
    plt.plot(T,D);
    plt.show();
