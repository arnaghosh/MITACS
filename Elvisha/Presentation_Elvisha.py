import numpy as np
import cv2, sys, os, time
from win32api import GetSystemMetrics
from calib import *

class Present_Elvisha:
    width = 640; #GetSystemMetrics(0);
    height = 640; #GetSystemMetrics(1);
        
    def init(self):
        cv2.namedWindow("screen");
        cv2.namedWindow("mine");
        
        size = self.height, self.width,3;
        baseImg = np.zeros(size,dtype=np.uint8);
        #max Height of target, ie , 100% => 80% of height. Setting initial target at 30%
        cv2.rectangle(baseImg, (int(self.width/3), int(self.height - 0.8*self.height)), (int(2*self.width/3), self.height), (255,255,255), -1);
        gripper = calibrate_BIOPAC();
        gripper.init();
        gripper.getGripperMax();
        print "Release the gripper" ;
        cv2.waitKey(1000);
        valX = gripper.gripperVal();
        cv2.imshow("screen", baseImg);
        cv2.waitKey(1000);
        cv2.putText(baseImg, "Squeeze to reach the target and", (int(self.width/60),int(0.1*self.height)),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),3);
        cv2.putText(baseImg, "Hold for 1 second", (int(self.width/5),int(0.15*self.height)),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),3);
        print gripper.maxVal, gripper.init_x
        cv2.imshow("screen", baseImg);
        cv2.waitKey(1000);
        targets = 1;  #number of targets
        for i in range(targets):
            img = baseImg.copy();
            t1 = 0;
            t2 = 0;
            target_reached = 0;
            #setting first target to 30%
            target_ = 30;
            tar_per = target_/100.0;
            cv2.rectangle(img, (int(self.width/3), int(self.height - tar_per*0.8*self.height)), (int(2*self.width/3), self.height), (0,0,255), -1);
            while(1):
                img2 = img.copy();
                valX = gripper.gripperVal();
                frac = (valX - gripper.init_x)/(gripper.maxVal - gripper.init_x);
                #print valX, frac
                cv2.rectangle(img2, (int(4*self.width/9), int(self.height - frac*0.8*self.height)), (int(5*self.width/9), self.height), (255,0,0), -1);
                cv2.imshow("screen",img2);
                cv2.imshow("mine",img2);
                if cv2.waitKey(15)==27 :
                    break;
                if abs(frac-tar_per)<0.05 :
                    if target_reached==0:
                        t1 = time.time();
                        target_reached = 1;
                    if target_reached == 1:
                        t2 = time.time();
                    if (t2-t1)>3.0 :    # change hold time here -> presently it's 1 sec
                        break;
                if abs(frac-tar_per)>=0.05:
                    target_reached = 0;
                
        
        cv2.destroyAllWindows();
        gripper.destroy();


if __name__ == '__main__':
    ppt = Present_Elvisha()
    ppt.init()
