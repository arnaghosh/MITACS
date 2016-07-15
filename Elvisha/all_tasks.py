from gripperMax import gripperMax
from holdTask import holdTask
from isometricTask import isometricTask
from motorLearningTask import motorLearningTask
from cross import cross
from task_GUI_prog import Ui_MainWindow
from PyQt4 import QtGui
import numpy as np
import cv2, sys, os, time, win32api, wx, threading, win32gui
import win32ui, win32con, re, pywinauto, win32com.client
from libmpdev import *
import matplotlib.pyplot as plt
from win32api import GetSystemMetrics

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

threadNum = 1;

class Form(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Form,self).__init__()
        self.setupUi(self);
        self.getMax.clicked.connect(self.getMaxContrac);
        self.loadMax.clicked.connect(self.loadMaxContrac);
        self.hold.clicked.connect(self.startHoldTask);
        self.learn.clicked.connect(self.startLearnTask);
        self.isometric.clicked.connect(self.startIsometricTask);
        self.presentCross.clicked.connect(self.presentationCross);
        self.quit.clicked.connect(self.quit_app);

    def timeAfterExercise_str(self,x):
        return {
            0 : 'Familiarization' ,
            1 : 'preExercise' ,
            2 : '30min',
            3 : '60min',
            4 : '90min',
        }.get(x,'120min')

    def msgbtn(self,i):
       self.optionChosen = i.text();

    def overwriteMessage(self,filename):
        msg = QtGui.QMessageBox()
        msg.setIcon(QtGui.QMessageBox.Question)
        msg.setFixedSize(250, 100); 
        msg.move((GetSystemMetrics(0))/2,(GetSystemMetrics(1))/2);
        msg.setText("Do you want to overwrite an existing file?")
        msg.setInformativeText("Do you want to overwrite the file "+filename)
        msg.setWindowTitle("MessageBox demo")
        msg.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        msg.buttonClicked.connect(self.msgbtn)
        retval = msg.exec_()

    def presentationCross(self):
        self.obj = cross();
        self.obj.init();
        self.obj.drawCross();
        cv2.destroyAllWindows();
    
    def getMaxContrac(self):
        subname = self.subName.text();
        checkFile = "data\\"+subname+"\\"+subname+"_maxContrac.txt";
        if os.path.isfile(checkFile):
            self.overwriteMessage(checkFile);
            if self.optionChosen == "&No":
                return;
        global threadNum
        dThread = dataThread(threadNum,"BIOPAC");
        threadNum = threadNum+1;
        self.obj = gripperMax();
        self.obj.init();
        mutex.acquire();
        dThread.t0 = time.clock();
        dThread.start();
        mutex.release();
        self.obj.gripperInit(dThread);
        print self.obj.init;
        self.text_init.setText(str(self.obj.init));
        self.obj.getGripperMax(dThread, str(self.subName.text()));
        self.text_max.setText(str(self.obj.maxVal));
        cv2.destroyAllWindows();
        mutex.acquire();
        dThread.exit = -1;
        dThread.close();
        mutex.release();
        
    def loadMaxContrac(self):
        global threadNum
        dThread = dataThread(threadNum,"BIOPAC");
        threadNum = threadNum+1;
        self.obj = gripperMax();
        self.obj.init();
        mutex.acquire();
        dThread.t0 = time.clock();
        dThread.start();
        mutex.release();
        self.obj.gripperInit(dThread);
        print self.obj.init;
        self.text_init.setText(str(self.obj.init));
        fname = self.subName.text();
        f = open("data\\"+fname+"\\"+fname+"_maxContrac.txt",'r');
        self.obj.maxVal = float(f.read())+self.obj.init;
        self.text_max.setText(str(self.obj.maxVal));
        cv2.destroyAllWindows();
        mutex.acquire();
        dThread.exit = -1;
        dThread.close();
        mutex.release();
        
    def startHoldTask(self):
        subname = self.subName.text();
        tAE = self.combo_holdTime.currentIndex();
        tAfterExer = self.timeAfterExercise_str(self.combo_holdTime.currentIndex());
        familTrials = int(self.text_trialFamil.text());
        checkFile = "data\\"+subname+"\\"+subname+"_"+tAfterExer+".txt";
        if tAE!=0 and os.path.isfile(checkFile):
            self.overwriteMessage(checkFile);
            if self.optionChosen == "&No":
                return;
        global threadNum
        dThread = dataThread(threadNum,"BIOPAC");
        threadNum = threadNum+1;
        self.obj = holdTask();
        self.obj.init(str(self.subName.text()), self.timeAfterExercise_str(self.combo_holdTime.currentIndex()));
        mutex.acquire();
        dThread.t0 = time.clock();
        dThread.start();
        mutex.release();
        self.obj.gripperInitVal(dThread);
        self.obj.init = float(self.text_init.text());
        self.obj.maxVal = float(self.text_max.text());
        T_start = time.clock();        
        if tAE!=0:
            self.obj.gripperTask(50,dThread);
        else:
            self.obj.familiarization(familTrials,dThread);
        T_end = time.clock();
        print (T_end-T_start);
        cv2.destroyAllWindows();
        mutex.acquire();
        dThread.exit = -1;
        dThread.close();
        mutex.release();
        if (tAE!=0):
            self.obj.plotGripperData(dThread);

    def startIsometricTask(self):
        subname = self.subName.text();
        tAfterExer = self.timeAfterExercise_str(self.combo_holdTime.currentIndex());
        checkFile = "data\\"+subname+"\\"+subname+"_"+tAfterExer+"_isometricData.txt";
        if os.path.isfile(checkFile):
            self.overwriteMessage(checkFile);
            if self.optionChosen == "&No":
                return;
        global threadNum
        dThread = dataThread(threadNum,"BIOPAC");
        threadNum = threadNum+1;
        self.obj = isometricTask();
        self.obj.init(str(self.subName.text()), self.timeAfterExercise_str(self.combo_holdTime.currentIndex()));
        mutex.acquire();
        dThread.t0 = time.clock();
        dThread.start();
        mutex.release();
        self.obj.gripperInitVal(dThread);
        self.obj.init = float(self.text_init.text());
        self.obj.maxVal = float(self.text_max.text());
        T_start = time.clock();        
        self.obj.gripperTask(float(self.text_isoTrialTime.text()),dThread);
        T_end = time.clock();
        print (T_end-T_start);
        cv2.destroyAllWindows();
        mutex.acquire();
        dThread.exit = -1;
        dThread.close();
        mutex.release();
        self.obj.plotGripperData(dThread);

    def startLearnTask(self):
        subname = self.subName.text();
        block = self.combo_block.currentIndex();
        checkFile = "data\\"+subname+"_learning\\"+subname+"_learning_Block"+str(block)+".txt";
        if block!=0 and os.path.isfile(checkFile):
            self.overwriteMessage(checkFile);
            if self.optionChosen == "&No":
                return;
        global threadNum
        dThread = dataThread(threadNum,"BIOPAC");
        threadNum = threadNum+1;
        entered_trials = int(self.totalTrials.text());
        entered_trialTime = int(self.trialTime.text());
        entered_scoreThresh = int(self.text_scoreThresh.text());
        self.obj = motorLearningTask();
        self.obj.init(str(self.subName.text()));
        if block==6:
            self.combo_fb.setCurrentIndex(0);
        if block==7:
            self.combo_fb.setCurrentIndex(1);
        self.obj.feedback = self.combo_fb.currentIndex();
        mutex.acquire();
        dThread.t0 = time.clock();
        dThread.start();
        mutex.release();
        self.obj.gripperInitVal(dThread);
        self.obj.init = float(self.text_init.text());
        self.obj.maxVal = float(self.text_max.text());
        T_start = time.clock();
        if block==0:
            self.obj.familiarization(entered_scoreThresh, entered_trialTime, block, dThread);
        else:
            self.obj.gripperTask(entered_trials, entered_trialTime, block, dThread);
        T_end = time.clock();
        print (T_end-T_start);
        cv2.destroyAllWindows();
        mutex.acquire();
        dThread.exit = -1;
        dThread.close();
        mutex.release();
        if block!=0:
            self.obj.plotGripperData(dThread, entered_trialTime);
        self.combo_block.setCurrentIndex((1+block)%8);

    def quit_app(self):
        os._exit(0);
        exit()
        
if __name__=='__main__':
    app = QtGui.QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec_())        
        
        
