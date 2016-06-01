from perform_presentation_BIOPAC_hold import *
from perform_presentation_BIOPAC_learning import Present_PERFORM_learn
from hold_task_GUI_prog import Ui_MainWindow
from PyQt4 import QtGui
import numpy as np
import cv2, sys, os, time, win32api, wx, threading
from libmpdev import *
import matplotlib.pyplot as plt

class Form(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Form,self).__init__()
        self.setupUi(self);
        self.getMax.clicked.connect(self.getMaxContrac);
        self.hold.clicked.connect(self.holdTask);
        self.learn.clicked.connect(self.learnTask);
        self.quit.clicked.connect(self.quit_app);

    def getMaxContrac(self):
        self.dThread = dataThread(1,"BIOPAC");
        self.obj = Present_PERFORM_hold();
        self.obj.init(str(self.subName.text()));
        self.dThread.t0 = time.clock();
        self.dThread.start();
        self.obj.gripperInit(self.dThread);
        print self.obj.init;
        self.obj.getGripperMax(self.dThread);
        cv2.destroyAllWindows();
        self.dThread.no_action = 1;

    def holdTask(self):
        self.dThread.no_action = 0;
        T_start = time.clock();        
        self.obj.gripperTask(50,self.dThread);
        T_end = time.clock();
        print (T_end-T_start);
        cv2.destroyAllWindows();
        self.dThread.no_action = 1;
        self.obj.plotGripperData(self.dThread);

    def learnTask(self):               
        entered_trials = int(self.totalTrials.text());
        entered_trialTime = int(self.trialTime.text());
        self.learning = Present_PERFORM_learn();
        self.learning.init(str(self.subName.text()));
        self.learning.maxVal = self.obj.maxVal;
        self.learning.init = self.obj.init;
        print self.learning.init, self.learning.maxVal;
        self.dThread.t0 = time.clock();
        self.dThread.no_action = 0;
        T_start = time.clock();        
        self.learning.gripperTask(entered_trials, entered_trialTime, self.dThread);
        T_end = time.clock();
        print (T_end-T_start);
        cv2.destroyAllWindows();
        self.dThread.no_action = 1;
        self.learning.plotGripperData(self.dThread, entered_trialTime);

    def quit_app(self):
        self.dThread.exit = 1;
        self.dThread.close();
        exit()

if __name__=='__main__':
    app = QtGui.QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec_())
    
    
    
