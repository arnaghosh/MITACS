import numpy as np
import cv2, sys, os, time, win32api, wx, threading, win32gui
import win32ui, win32con, re, pywinauto, win32com.client
from libmpdev import *
import matplotlib.pyplot as plt

class cross:
    app = wx.App(False);
    sizes = [wx.Display(i).GetGeometry().GetSize() for i in range(wx.Display.GetCount())]
    width1 = sizes[wx.Display.GetCount()-1].GetWidth();
    height1 = sizes[wx.Display.GetCount()-1].GetHeight();
    width11 = sizes[0].GetWidth();
    height11 = sizes[0].GetHeight();
    width2 = sizes[0].GetWidth()/2;
    height2 = sizes[0].GetHeight()/2;

    def init(self):
        cv2.namedWindow("display");
        cv2.namedWindow("operator");
        self.basImg1 = np.zeros((self.height1,self.width1,3),dtype=np.uint8);
        self.basImg2 = np.zeros((self.height2,self.width2,3),dtype=np.uint8);
        cv2.imshow("display",self.basImg1);
        cv2.imshow("operator",self.basImg2);
        self.crossSize = 50;
        self.crossThickness = 8;

    def drawCross(self):
        task1 = self.basImg1.copy();
        task2 = self.basImg2.copy();
        cv2.putText(task2, "Press Enter when ready",(int(self.width2/5),int(self.height2/3)),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),3);
        cv2.imshow("display",task1);
        cv2.waitKey(2000);
        cv2.imshow("operator",task2);
        while(1):
            if cv2.waitKey(30)==13:
                break;

        task2 = self.basImg2.copy();
        cv2.rectangle(task1,(int((self.width1 - self.crossThickness)/2),int((self.height1 - self.crossSize)/2)),(int((self.width1 + self.crossThickness)/2),int((self.height1 + self.crossSize)/2)),(255,255,255),-1);
        cv2.rectangle(task2,(int((self.width2 - self.crossThickness)/2),int((self.height2 - self.crossSize)/2)),(int((self.width2 + self.crossThickness)/2),int((self.height2 + self.crossSize)/2)),(255,255,255),-1);
        cv2.rectangle(task1,(int((self.width1 - self.crossSize)/2),int((self.height1 - self.crossThickness)/2)),(int((self.width1 + self.crossSize)/2),int((self.height1 + self.crossThickness)/2)),(255,255,255),-1);
        cv2.rectangle(task2,(int((self.width2 - self.crossSize)/2),int((self.height2 - self.crossThickness)/2)),(int((self.width2 + self.crossSize)/2),int((self.height2 + self.crossThickness)/2)),(255,255,255),-1);
        cv2.putText(task2, "Press Escape to quit",(int(self.width2/10),int(4*self.height2/5)),cv2.FONT_HERSHEY_PLAIN,3,(255,255,255),2);
        while(1):
            cv2.imshow("display",task1);
            cv2.imshow("operator",task2);
            if cv2.waitKey(30)==27:
                break;
