from gripperMax import gripperMax
from holdTask import holdTask
from motorLearningTask import motorLearningTask
from task_GUI_prog import Ui_MainWindow
from PyQt4 import QtGui
import numpy as np
import cv2, sys, os, time, win32api, wx, threading, win32gui
import win32ui, win32con, re, pywinauto, win32com.client
from libmpdev import *
import matplotlib.pyplot as plt
#from psychopy import core
#from ctypes import windll

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
            mutex.acquire();
            if self.exit==1:
                mutex.release();
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
            mutex.release();
        print "dThread closing";
            
        
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
        self.portAddress = 0xD050;
        win32gui.EnumWindows(find_window_callback,".*Notepad.*"); #Spike2 -
        self.whndl = whndl;
        print self.whndl
        title = str(win32gui.GetWindowText(self.whndl));
        print title
        #self.whndl = win32gui.FindWindowEx(0,0,None, title);
        #self.hwnds = {};
        #win32gui.EnumChildWindows(self.whndl,callback,self.hwnds)
        #print self.hwnds;
        #self.whndl = self.hwnds['AfxWnd110u']
        #self.wnd = win32ui.CreateWindowFromHandle(self.whndl);
        self.app = pywinauto.application.Application();
        self.win = self.app.window_(handle=self.whndl);
        self.shell = win32com.client.Dispatch("WScript.Shell")
        
    
    def run(self):
        while(1):
            mutex.acquire();
            tr_value = self.trigger;
            if tr_value==-1:
                mutex.release();
                break;
            if tr_value!=0:
                #self.wnd.SendMessage(win32con.WM_CHAR, ord(str(self.trigger)),0); #send keypress here.-> self.trigger value
                if self.whndl!=win32gui.GetForegroundWindow():
                    self.win.Minimize()
                    self.win.Restore();
                    self.win.SetFocus();
                if tr_value==1:
                    self.shell.SendKeys("1")
                if tr_value==2:
                    self.shell.SendKeys("2")
                #windll.inpout32.Out32(self.portAddress, tr_value)
                #core.wait(0.001)
                #windll.inpout32.Out32(self.portAddress, 0)#write to parallel port here. -> self.trigger value.
                self.trigger = 0;
            mutex.release();
            time.sleep(0.001);
        print "trThread closing";

    def close(self):
        self.trigger = -1;

threadNum = 1;

class Form(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Form,self).__init__()
        self.setupUi(self);
        self.getMax.clicked.connect(self.getMaxContrac);
        self.hold.clicked.connect(self.startHoldTask);
        self.learn.clicked.connect(self.startLearnTask);
        self.quit.clicked.connect(self.quit_app);

    def getMaxContrac(self):
        global threadNum
        dThread = dataThread(threadNum,"BIOPAC");
        trThread = triggerThread(threadNum+1,"Trigger");
        threadNum = threadNum+2;
        self.obj = gripperMax();
        self.obj.init();
        mutex.acquire();
        dThread.t0 = time.clock();
        dThread.start();
        trThread.start();
        mutex.release();
        self.obj.gripperInit(dThread);
        print self.obj.init;
        self.text_init.setText(str(self.obj.init));
        self.obj.getGripperMax(dThread);
        self.text_max.setText(str(self.obj.maxVal));
        cv2.destroyAllWindows();
        mutex.acquire();
        dThread.exit = -1;
        trThread.trigger = -1;
        dThread.close();
        trThread.close();
        mutex.release();

    def startHoldTask(self):
        global threadNum
        dThread = dataThread(threadNum,"BIOPAC");
        trThread = triggerThread(threadNum+1,"Trigger");
        threadNum = threadNum+2;
        self.obj = holdTask();
        self.obj.init(str(self.subName));
        mutex.acquire();
        dThread.t0 = time.clock();
        dThread.start();
        trThread.start();
        mutex.release();
        self.obj.gripperInitVal(dThread);
        self.obj.init = float(self.text_init.text());
        self.obj.maxVal = float(self.text_max.text());
        T_start = time.clock();        
        self.obj.gripperTask(50,dThread,trThread);
        T_end = time.clock();
        print (T_end-T_start);
        cv2.destroyAllWindows();
        mutex.acquire();
        dThread.exit = -1;
        trThread.trigger = -1;
        dThread.close();
        trThread.close();
        mutex.release();
        self.obj.plotGripperData(dThread);

    def startLearnTask(self):
        global threadNum
        dThread = dataThread(threadNum,"BIOPAC");
        trThread = triggerThread(threadNum+1,"Trigger");
        threadNum = threadNum+2;
        entered_trials = int(self.totalTrials.text());
        entered_trialTime = int(self.trialTime.text());
        self.obj = motorLearningTask();
        self.obj.init(str(self.subName.text()));
        self.obj.feedback = self.combo_fb.currentIndex();
        mutex.acquire();
        dThread.t0 = time.clock();
        dThread.start();
        trThread.start();
        mutex.release();
        self.obj.gripperInitVal(dThread);
        self.obj.init = float(self.text_init.text());
        self.obj.maxVal = float(self.text_max.text());
        T_start = time.clock();        
        self.obj.gripperTask(entered_trials, entered_trialTime, dThread, trThread);
        T_end = time.clock();
        print (T_end-T_start);
        cv2.destroyAllWindows();
        mutex.acquire();
        dThread.exit = -1;
        trThread.trigger = -1;
        dThread.close();
        trThread.close();
        mutex.release();
        self.obj.plotGripperData(dThread, entered_trialTime);

    def quit_app(self):
        os._exit(0);
        exit()
        
if __name__=='__main__':
    app = QtGui.QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec_())        
        
        
