from PyQt4.uic import loadUiType
import sys, math, random
from PyQt4 import QtGui
import numpy as np
from win32api import GetSystemMetrics
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from analyseWin import Ui_MainWindow
import mysql.connector

horiz = GetSystemMetrics(0)
vert = GetSystemMetrics(1)
screen_conv_ratio_h = (1.0*horiz) / 1366;
screen_conv_ratio_v = (1.0*vert) / 768;

def dayTitle(x):
    return {
        1 : '_Day1_' ,
        2 : '_Day2_',
        3 : '_Day3_',
        4 : '_Day4_',
        5 : '_Day5_',
        6 : '_Baseline_',
    }.get(x,'_Performance_')

def center_x(x):
    return {
        0: 683 * screen_conv_ratio_h,
        1: 994 * screen_conv_ratio_h,
        2: 1052 * screen_conv_ratio_h,
        3: 994 * screen_conv_ratio_h,
        4: 683 * screen_conv_ratio_h,
        5: 466 * screen_conv_ratio_h,
        6: 243 * screen_conv_ratio_h,
        7: 466 * screen_conv_ratio_h,
        }.get(x, 683 * screen_conv_ratio_h)

def center_y(x):
    return {
        0: 71 * screen_conv_ratio_h,
        1: 157 * screen_conv_ratio_h,
        2: 384 * screen_conv_ratio_h,
        3: 602 * screen_conv_ratio_h,
        4: 693 * screen_conv_ratio_h,
        5: 602 * screen_conv_ratio_h,
        6: 384 * screen_conv_ratio_h,
        7: 157 * screen_conv_ratio_h,
        }.get(x, 384 * screen_conv_ratio_h)


class Main(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, ):
        super(Main, self).__init__()
        self.setupUi(self)
        self.StartButton.clicked.connect(self.loadFile)
        self.NextButton.clicked.connect(self.nextRecord)
        self.DeleteButton.clicked.connect(self.deleteRecord)
        self.GenerateButton.clicked.connect(self.generateRecord)
        self.QuitButton.clicked.connect(self.quit)
        self.horiz = GetSystemMetrics(0)
        self.verti = GetSystemMetrics(1)
        self.X=[];
        self.Y=[];
        self.D=[];
        self.V=[];
        self.A=[];
        self.T=[];
        self.subjectNo = 0;
        self.dayNo = 0;
        self.blockNo = 0;
        self.center_no = 0;
        self.tr_no = 0;
        self.old_x = 0
        self.old_y = 0
        self.old_t = 0
        self.start=0;
        self.vel_thresh = 500; #in pix/s
        self.deleteThisRecord = 0;
        self.generateAll = 0;
        self.fileReadDone = 0;
        self.AllStrings = [];  #raw file.
        self.AllGoodStrings = []; #filtered file
        self.RandomStrings = [];
        self.SequenceStrings = [];
        self.RandomGoodStrings = [];
        self.SequenceGoodStrings = [];
        topics="tr_no Reaction_Time Movement_Time Response_Time Max_Vel Max_Acc End_Point_Dev Real_Distance Actual_Distance_Traversed Distance_Percent\n";
        self.AllStrings.append(topics);
        self.AllGoodStrings.append(topics);
        self.RandomStrings.append(topics);
        self.SequenceStrings.append(topics);
        self.RandomGoodStrings.append(topics);
        self.SequenceGoodStrings.append(topics);
        self.cnx = mysql.connector.connect(user='root',password='neuro',database='mohand');
        self.cursor = self.cnx.cursor();

    def addplot(self, fig):
        #plt.savefig('common_labels_text.png', dpi=300)
        self.canvas = FigureCanvas(fig)
        self.mplvl.addWidget(self.canvas)
        self.canvas.draw()
        self.toolbar = NavigationToolbar(self.canvas, self, coordinates=True)
        self.addToolBar(self.toolbar)

    def rmplot(self):
        self.mplvl.removeWidget(self.canvas)
        self.canvas.close()
        self.mplvl.removeWidget(self.toolbar)
        self.toolbar.close()

    def loadFile(self):
        print "load file"
        self.generateAll = 0;
        self.fileReadDone = 0;
        subNo = self.SubjectText.text()
        d = self.DayCombo.currentIndex()
        self.subjectNo = int(subNo);
        self.dayNo = d+1;
        self.blockNo = self.BlockCombo.currentIndex()+1 
        block = str(self.blockNo);
        day = dayTitle(self.dayNo)
        if self.dayNo<=5:
            s = "C:\\Users\\neuro\\Documents\\Arna\\Tracker\\Data\\Subject "+subNo+"\\Subject" + subNo + day + "Block" + block + "_Data.txt";
        else:
            s = "C:\\Users\\neuro\\Documents\\Arna\\Tracker\\Data\\Subject "+subNo+"\\Subject" + subNo + day + "Data.txt";
        center_file_s = "C:\\Users\\neuro\\Documents\\Visual Studio 2015\\Projects\\MohandTracker\\Mohands(4,6,5).txt";
        print s
        self.file = open(s, 'r');
        self.center_file = open(center_file_s, 'r');
        self.center_array = [[int(x) for x in line.split()] for line in self.center_file];
        #print self.center_array
        self.center_array_size = len(self.center_array[0]);
        self.tr_no = 1;
        self.start = 0;
        self.getFig();
        
        
        
    def getFig(self):
        s1 = str(self.tr_no);
        s2 = str(self.tr_no+1);
        self.FromLabel.setText(s1);
        self.ToLabel.setText(s2);
        reac_time = 0;
        react_time_set = 0;
        response_time = 0;
        
        if self.dayNo<=5 :
            self.center_no = (5 * (self.dayNo-1) + self.blockNo-1) % self.center_array_size; 
        else :
            self.center_no = (25 + self.dayNo % 2) % self.center_array_size;
        if int(self.tr_no)<len(self.center_array):
            present_target = (self.center_array[int(self.tr_no)][int(self.center_no)])%9;
        #print self.tr_no, present_target;
        for line in self.file:
            tr_no, x , y , t = [float(i) for i in line.split()];
            
            
            if self.start==0:
                self.old_x = x;
                self.old_y = y;
                self.old_t = t;
                self.X=[x];
                self.Y=[y];
                self.T=[t];
                self.start=1;
                continue
                
            if tr_no == self.tr_no:
                
                self.X.append(x);
                self.Y.append(y);
                self.T.append(t);
                dist = math.sqrt((x-self.old_x)*(x-self.old_x) + (y-self.old_y)*(y-self.old_y));
                if len(self.D)!=0:
                    self.D.append(dist+self.D[len(self.D)-1]);
                else:
                    self.D.append(dist);
                    print t,self.old_t
                vel = dist/(t-self.old_t);
                if len(self.V)!=0 :
                    self.old_v = self.V[len(self.V)-1];
                    acc = (vel-self.old_v)/(t-self.old_t);
                    self.A.append(acc);
                self.V.append(vel);
                self.old_x = x
                self.old_y = y
                self.old_t = t
                if (vel>self.vel_thresh) and (react_time_set==0):
                    reac_time = t;
                    react_time_set = 1;
                if (vel>self.vel_thresh):
                    response_time = t;
                movement_time = response_time - reac_time;

            else:
                print "len",len(self.T), len(self.D)
                if self.T[len(self.T)-1]<=0.007 or self.T[len(self.T)-1]>=12:
                    self.deleteThisRecord = 1;
                if self.generateAll==0:
                    fig = plt.figure()
                    a1 = fig.add_subplot(221)
                    a1.plot(self.X,self.Y);
                    a1.set_ylabel('Y');
                    a1.set_xlabel('X');
                    a1.plot(self.X[0],self.Y[0],'g+', mew=1.5, ms=15)
                    a1.plot(center_x(present_target),center_y(present_target),'ro', markerfacecolor='None', mew= 1, ms = 15)
                    a1.plot(center_x(present_target),center_y(present_target),'r.')
                    a1.axis([0,self.horiz,0,self.verti])
                
                    a2 = fig.add_subplot(222)
                    a2.plot(self.T[1:len(self.T)],self.D);
                    a2.set_ylabel('Distance from starting point');
                    a2.set_xlabel('Time');
                
                    a3 = fig.add_subplot(223)
                    a3.plot(self.T[1:len(self.T)],self.V);
                    a3.set_ylabel('Speed of cursor');
                    a3.set_xlabel('Time');
                
                    a4 = fig.add_subplot(224)
                    a4.plot(self.T[2:len(self.T)],self.A);
                    a4.set_ylabel('Acceleration of cursor');
                    a4.set_xlabel('Time');
                
                    self.rmplot()
                    self.addplot(fig)

                max_vel = max(self.V);
                max_acc = max(self.A);
                end_point_dev = math.sqrt((self.X[len(self.X)-1]-center_x(present_target))*(self.X[len(self.X)-1]-center_x(present_target)) + (self.Y[len(self.Y)-1]-center_y(present_target))*(self.Y[len(self.Y)-1]-center_y(present_target)));
                real_dist = math.sqrt((self.X[0]-self.X[len(self.X)-1])*(self.X[0]-self.X[len(self.X)-1]) + (self.Y[0]-self.Y[len(self.Y)-1])*(self.Y[0]-self.Y[len(self.Y)-1]));
                actual_dist_traversed = self.D[len(self.D)-1];
                dist_per = (actual_dist_traversed - real_dist)*100.0/real_dist ;
                
                old_tr_no = self.tr_no;
                self.old_x = x
                self.old_y = y
                self.old_t = t
                self.tr_no = tr_no
                self.D=[];
                self.V=[];
                self.A=[];
                self.T=[t];
                self.X=[x];
                self.Y=[y];
                break

        else:
            self.fileReadDone = 1;

        if self.generateAll ==0:
            s3 = "Reaction Time = " + str(reac_time);
            s4 = "Movement Time = " + str(movement_time);
            s5 = "Response Time = " + str(response_time);
            s6 = "Max Velocity = " + str(max_vel);
            s7 = "Max Acc = " + str(max_acc);
            s8 = "End Point Deviation = " + str(end_point_dev);
            s9 = "Real Distance = " + str(real_dist);
            s10 = "Actual Distance Traversed = " + str(actual_dist_traversed);
            s11 = "Distance Percent Deviation = " + str(dist_per);
            self.Reaction_Time.setText(s3)
            self.Movement_Time.setText(s4)
            self.Response_Time.setText(s5)
            self.Max_Velocity.setText(s6)
            self.Max_Acc.setText(s7)
            self.Deviation.setText(s8)
            self.Real_Dist.setText(s9)
            self.Actual_Dist.setText(s10)
            self.Dist_Per.setText(s11)
        if self.fileReadDone==0:
            final_str = str(int(old_tr_no))+" "+str(reac_time)+" "+str(movement_time)+" "+str(response_time)+" "+str(max_vel)+" "+str(max_acc)+" "+str(end_point_dev)+" "+str(real_dist)+" "+str(actual_dist_traversed)+" "+str(dist_per)+"\n";
            self.AllStrings.append(final_str);
            if (old_tr_no%13)>=7 or (old_tr_no%13)==0:
                self.SequenceStrings.append(final_str);
            else:
                self.RandomStrings.append(final_str);

    def nextRecord(self):
        self.writeToFilteredFile();
        print "fetching next record"
        #self.tr_no = self.tr_no+1;
        self.getFig();

    def writeToFilteredFile(self):
        already_written_tr_no = -1;
        if len(self.AllGoodStrings)>1:
            filtered_data_list = [j for j in self.AllGoodStrings[len(self.AllGoodStrings)-1].split()]
            already_written_tr_no = int(filtered_data_list[0]);
        old_tr_no = int(self.AllStrings[len(self.AllStrings)-1].split()[0])
        if (self.deleteThisRecord==0) and (int(old_tr_no)!=already_written_tr_no):
            self.AllGoodStrings.append(self.AllStrings[len(self.AllStrings)-1]);
            if (old_tr_no%13)>=7 or (old_tr_no%13)==0:
                self.SequenceGoodStrings.append(self.AllStrings[len(self.AllStrings)-1]);
            else:
                self.RandomGoodStrings.append(self.AllStrings[len(self.AllStrings)-1]);
        self.deleteThisRecord = 0;

    def typeOfEntry(self,x):
        return{
            1: '_fil_rep',
            2: '_fil_ran',
            3: '_raw_rep',
            4: '_raw_ran'
            }.get(x)

    def dayDatabase(self,x):
        return{
            1: 'day1',
            2: 'day2',
            3: 'day3',
            4: 'day4'
            }.get(x,'day5')

    def deleteFromDatabase(self):
        if self.dayNo==6:
            day_str = "baseline";
        elif self.dayNo<=5:
            day_str = self.dayDatabase(self.dayNo);
        else:
            day_str = "performance";
        s = "delete from "+day_str+" where subNo="+str(self.subjectNo);
        self.cursor.execute(s);

    def createDatabaseRecord(self):
        if self.dayNo==6:
            day_str = "baseline";
        elif self.dayNo<=5:
            day_str = self.dayDatabase(self.dayNo);
        else:
            day_str = "performance";
        init_record = np.zeros(60);
        s="insert into "+day_str+"(subNo) values("+str(self.subjectNo)+")";
        self.cursor.execute(s);
            
    def writeToDatabase(self,entryType,meanReactionTime,meanMovementTime,meanResponseTime,meanMaxVel,meanMaxAcc,meanEPD,meanRealDist,meanTraversedDist,meanPerDev,ovMaxReactionTime,ovMaxMovementTime,ovMaxEPD,ovMaxSpeed,ovMaxAcc,indexVal):
        entry_str = self.typeOfEntry(entryType);
        print entryType,entry_str
        if self.dayNo>5:
            if self.dayNo==6:
                day_str = "baseline";
            else :
                day_str = "performance";
            s ="update "+day_str+" set meanReactionTime"+entry_str+"="+str(meanReactionTime)+",meanMovementTime"+entry_str+"="+str(meanMovementTime)+",meanResponseTime"+entry_str+"="+str(meanResponseTime)+",meanMaxVel"+entry_str+"="+str(meanMaxVel)+",meanMaxAcc"+entry_str+"="+str(meanMaxAcc)+",meanEPD"+entry_str+"="+str(meanEPD)+",meanRealDist"+entry_str+"="+str(meanRealDist)+",meanTraversedDist"+entry_str+"="+str(meanTraversedDist)+",meanPerDev"+entry_str+"="+str(meanPerDev)+",ovMaxReactionTime"+entry_str+"="+str(ovMaxReactionTime)+",ovMaxMovementTime"+entry_str+"="+str(ovMaxMovementTime)+",ovMaxEPD"+entry_str+"="+str(ovMaxEPD)+",ovMaxSpeed"+entry_str+"="+str(ovMaxSpeed)+",ovMaxAcc"+entry_str+"="+str(ovMaxAcc)+",indexVal"+entry_str+"="+str(indexVal)+" where subNo="+str(self.subjectNo);
            self.cursor.execute(s);
        else:
            day_str = self.dayDatabase(self.dayNo);
            if self.blockNo==1:             #query will return empty set or an old junk value. Generating block 1 data clears any old data already stored.
                s ="update "+day_str+" set meanReactionTime"+entry_str+"="+str(meanReactionTime)+",meanMovementTime"+entry_str+"="+str(meanMovementTime)+",meanResponseTime"+entry_str+"="+str(meanResponseTime)+",meanMaxVel"+entry_str+"="+str(meanMaxVel)+",meanMaxAcc"+entry_str+"="+str(meanMaxAcc)+",meanEPD"+entry_str+"="+str(meanEPD)+",meanRealDist"+entry_str+"="+str(meanRealDist)+",meanTraversedDist"+entry_str+"="+str(meanTraversedDist)+",meanPerDev"+entry_str+"="+str(meanPerDev)+",ovMaxReactionTime"+entry_str+"="+str(ovMaxReactionTime)+",ovMaxMovementTime"+entry_str+"="+str(ovMaxMovementTime)+",ovMaxEPD"+entry_str+"="+str(ovMaxEPD)+",ovMaxSpeed"+entry_str+"="+str(ovMaxSpeed)+",ovMaxAcc"+entry_str+"="+str(ovMaxAcc)+",indexVal"+entry_str+"="+str(indexVal)+" where subNo="+str(self.subjectNo);
                self.cursor.execute(s);
            else:
                s = "select meanReactionTime"+entry_str+",meanMovementTime"+entry_str+",meanResponseTime"+entry_str+",meanMaxVel"+entry_str+",meanMaxAcc"+entry_str+",meanEPD"+entry_str+",meanRealDist"+entry_str+",meanTraversedDist"+entry_str+",meanPerDev"+entry_str+",ovMaxReactionTime"+entry_str+",ovMaxMovementTime"+entry_str+",ovMaxEPD"+entry_str+",ovMaxSpeed"+entry_str+",ovMaxAcc"+entry_str+",indexVal"+entry_str+" from "+day_str+" where subNo="+str(self.subjectNo);
                self.cursor.execute(s);
                for (old_meanReactionTime,old_meanMovementTime,old_meanResponseTime,old_meanMaxVel,old_meanMaxAcc,old_meanEPD,old_meanRealDist,old_meanTraversedDist,old_meanPerDev,old_ovMaxReactionTime,old_ovMaxMovementTime,old_ovMaxEPD,old_ovMaxSpeed,old_ovMaxAcc,old_indexVal) in self.cursor:
                    meanReactionTime = (float(old_meanReactionTime)*(self.blockNo-1)+meanReactionTime)/self.blockNo;
                    meanMovementTime = (float(old_meanMovementTime)*(self.blockNo-1)+meanMovementTime)/self.blockNo;
                    meanResponseTime = (float(old_meanResponseTime)*(self.blockNo-1)+meanResponseTime)/self.blockNo;
                    meanMaxVel = (float(old_meanMaxVel)*(self.blockNo-1)+meanMaxVel)/self.blockNo;
                    meanMaxAcc = (float(old_meanMaxAcc)*(self.blockNo-1)+meanMaxAcc)/self.blockNo;
                    meanEPD = (float(old_meanEPD)*(self.blockNo-1)+meanEPD)/self.blockNo;
                    meanRealDist = (float(old_meanRealDist)*(self.blockNo-1)+meanRealDist)/self.blockNo;
                    meanTraversedDist = (float(old_meanTraversedDist)*(self.blockNo-1)+meanTraversedDist)/self.blockNo;
                    meanPerDev = (float(old_meanPerDev)*(self.blockNo-1)+meanPerDev)/self.blockNo;
                    ovMaxReactionTime = (float(old_ovMaxReactionTime)*(self.blockNo-1)+ovMaxReactionTime)/self.blockNo;
                    ovMaxMovementTime = (float(old_ovMaxMovementTime)*(self.blockNo-1)+ovMaxMovementTime)/self.blockNo;
                    ovMaxEPD = (float(old_ovMaxEPD*(self.blockNo-1))+ovMaxEPD)/self.blockNo;
                    ovMaxSpeed = (float(old_ovMaxSpeed*(self.blockNo-1))+ovMaxSpeed)/self.blockNo;
                    ovMaxAcc = (float(old_ovMaxAcc*(self.blockNo-1))+ovMaxAcc)/self.blockNo;
                    indexVal = (float(old_indexVal*(self.blockNo-1))+indexVal)/self.blockNo;
            s ="update "+day_str+" set meanReactionTime"+entry_str+"="+str(meanReactionTime)+",meanMovementTime"+entry_str+"="+str(meanMovementTime)+",meanResponseTime"+entry_str+"="+str(meanResponseTime)+",meanMaxVel"+entry_str+"="+str(meanMaxVel)+",meanMaxAcc"+entry_str+"="+str(meanMaxAcc)+",meanEPD"+entry_str+"="+str(meanEPD)+",meanRealDist"+entry_str+"="+str(meanRealDist)+",meanTraversedDist"+entry_str+"="+str(meanTraversedDist)+",meanPerDev"+entry_str+"="+str(meanPerDev)+",ovMaxReactionTime"+entry_str+"="+str(ovMaxReactionTime)+",ovMaxMovementTime"+entry_str+"="+str(ovMaxMovementTime)+",ovMaxEPD"+entry_str+"="+str(ovMaxEPD)+",ovMaxSpeed"+entry_str+"="+str(ovMaxSpeed)+",ovMaxAcc"+entry_str+"="+str(ovMaxAcc)+",indexVal"+entry_str+"="+str(indexVal)+" where subNo="+str(self.subjectNo);
            self.cursor.execute(s);

    def generateRecord(self):
        self.writeToFilteredFile();
        self.generateAll = 1;
        while self.fileReadDone==0:
            self.getFig();
            self.writeToFilteredFile();
            
        raw_s = "C:\\Users\\neuro\\Documents\\Arna\\Tracker\\Data\\Subject "+str(self.subjectNo)+"\\Subject" + str(self.subjectNo) + dayTitle(self.dayNo) + "Block" + str(self.blockNo) + "_RawFileAll.txt";
        filter_s = "C:\\Users\\neuro\\Documents\\Arna\\Tracker\\Data\\Subject "+str(self.subjectNo)+"\\Subject" + str(self.subjectNo) + dayTitle(self.dayNo) + "Block" + str(self.blockNo) + "_FilteredFileAll.txt";
        rand_raw_s = "C:\\Users\\neuro\\Documents\\Arna\\Tracker\\Data\\Subject "+str(self.subjectNo)+"\\Subject" + str(self.subjectNo) + dayTitle(self.dayNo) + "Block" + str(self.blockNo) + "_RawFileRandom.txt";
        seq_raw_s = "C:\\Users\\neuro\\Documents\\Arna\\Tracker\\Data\\Subject "+str(self.subjectNo)+"\\Subject" + str(self.subjectNo) + dayTitle(self.dayNo) + "Block" + str(self.blockNo) + "_RawFileRepeated.txt";
        rand_filter_s = "C:\\Users\\neuro\\Documents\\Arna\\Tracker\\Data\\Subject "+str(self.subjectNo)+"\\Subject" + str(self.subjectNo) + dayTitle(self.dayNo) + "Block" + str(self.blockNo) + "_FilteredFileRandom.txt";
        seq_filter_s = "C:\\Users\\neuro\\Documents\\Arna\\Tracker\\Data\\Subject "+str(self.subjectNo)+"\\Subject" + str(self.subjectNo) + dayTitle(self.dayNo) + "Block" + str(self.blockNo) + "_FilteredFileRepeated.txt";
        rawFile = open(raw_s,'w');
        rand_rawFile = open(rand_raw_s, 'w');
        seq_rawFile = open(seq_raw_s, 'w');
        filterFile = open(filter_s,'w');
        rand_filterFile = open(rand_filter_s,'w');
        seq_filterFile = open(seq_filter_s,'w');
        s_meanReact = "\nMean Reaction Time = ";
        s_meanMove = "\nMean Movement Time = ";
        s_meanResponse = "\nMean Response Time = ";
        s_meanMaxVel = "\nMean maximum Speed = ";
        s_meanMaxAcc = "\nMean maximum acceleration = ";
        s_meanEPD = "\nMean End Point Deviation = ";
        s_meanRealDist = "\nMean Real Distance = ";
        s_meanDistTraversed = "\nMean Traversed Distance = ";
        s_meanDistPer = "\nMean Percentage deviation = ";
        s_maxReact = "%\nOverall Maximum Reaction Time = ";
        s_maxMove = "\nOverall Maximum Movement Time = ";
        s_maxEPD = "\nOverall Maximum End Point Deviation = ";
        s_maxMaxVel = "\nOverall Maximum Speed = ";
        s_maxMaxAcc= "\nOverall Maximum Acceleration = ";
        s_score = "\nIndex Value = ";

        A = np.zeros(9);
        max_react,max_move,max_epd,max_vel,max_acc = 0,0,0,0,0;
        for i in range(len(self.AllStrings)):
            rawFile.write(self.AllStrings[i])
            if i==0:
                continue;
            temp_data = [float(j) for j in self.AllStrings[i].split()];
            tdnp = np.array(temp_data[1:]);
            if tdnp[0]>max_react:
                max_react = tdnp[0];
            if tdnp[1]>max_move:
                max_move = tdnp[1];
            if tdnp[5]>max_epd:
                max_epd = tdnp[5];
            if tdnp[3]>max_vel:
                max_vel = tdnp[3];
            if tdnp[4]>max_acc:
                max_acc = tdnp[4];
            A = A+tdnp;
        A = A/(len(self.AllStrings));
        ##index_val = (A[3]/2330)+(A[4]/119289)+((2.389-A[1])/2.389)+((1.165-A[0])/1.165)+((100-A[8])/100)+((49.7-A[5])/49.7);
        ##index_val = index_val*10/6;
        index_val = ((100-A[8])/100)+((49.7-A[5])/49.7)+((1.165-A[0])/1.165);
        index_val = index_val*10/3;
        res_str=s_meanReact+str(A[0])+s_meanMove+str(A[1])+s_meanResponse+str(A[2])+s_meanMaxVel+str(A[3])+s_meanMaxAcc+str(A[4])+s_meanEPD+str(A[5])+s_meanRealDist+str(A[6])+s_meanDistTraversed+str(A[7])+s_meanDistPer+str(A[8])+s_maxReact+str(max_react)+s_maxMove+str(max_move)+s_maxEPD+str(max_epd)+s_maxMaxVel+str(max_vel)+s_maxMaxAcc+str(max_acc)+s_score+str(index_val)+"\n";
        rawFile.write(res_str);

        A = np.zeros(9);
        max_react,max_move,max_epd,max_vel,max_acc = 0,0,0,0,0;
        for i in range(len(self.AllGoodStrings)):
            filterFile.write(self.AllGoodStrings[i])
            if i==0:
                continue;
            temp_data = [float(j) for j in self.AllGoodStrings[i].split()];
            tdnp = np.array(temp_data[1:]);
            if tdnp[0]>max_react:
                max_react = tdnp[0];
            if tdnp[1]>max_move:
                max_move = tdnp[1];
            if tdnp[5]>max_epd:
                max_epd = tdnp[5];
            if tdnp[3]>max_vel:
                max_vel = tdnp[3];
            if tdnp[4]>max_acc:
                max_acc = tdnp[4];
            A = A+tdnp;
        A = A/(len(self.AllGoodStrings));
        index_val = ((100-A[8])/100)+((49.7-A[5])/49.7)+((1.165-A[0])/1.165);
        index_val = index_val*10/3;
        res_str=s_meanReact+str(A[0])+s_meanMove+str(A[1])+s_meanResponse+str(A[2])+s_meanMaxVel+str(A[3])+s_meanMaxAcc+str(A[4])+s_meanEPD+str(A[5])+s_meanRealDist+str(A[6])+s_meanDistTraversed+str(A[7])+s_meanDistPer+str(A[8])+s_maxReact+str(max_react)+s_maxMove+str(max_move)+s_maxEPD+str(max_epd)+s_maxMaxVel+str(max_vel)+s_maxMaxAcc+str(max_acc)+s_score+str(index_val)+"\n";
        filterFile.write(res_str);

        if self.blockNo==1:
            self.deleteFromDatabase();
            self.createDatabaseRecord();
        if self.dayNo>5:
            self.deleteFromDatabase();
            self.createDatabaseRecord();
        
        A = np.zeros(9);
        max_react,max_move,max_epd,max_vel,max_acc = 0,0,0,0,0;
        for i in range(len(self.RandomStrings)):
            rand_rawFile.write(self.RandomStrings[i])
            if i==0:
                continue;
            temp_data = [float(j) for j in self.RandomStrings[i].split()];
            tdnp = np.array(temp_data[1:]);
            if tdnp[0]>max_react:
                max_react = tdnp[0];
            if tdnp[1]>max_move:
                max_move = tdnp[1];
            if tdnp[5]>max_epd:
                max_epd = tdnp[5];
            if tdnp[3]>max_vel:
                max_vel = tdnp[3];
            if tdnp[4]>max_acc:
                max_acc = tdnp[4];
            A = A+tdnp;
        A = A/(len(self.RandomStrings));
        index_val = ((100-A[8])/100)+((49.7-A[5])/49.7)+((1.165-A[0])/1.165);
        index_val = index_val*10/3;
        res_str=s_meanReact+str(A[0])+s_meanMove+str(A[1])+s_meanResponse+str(A[2])+s_meanMaxVel+str(A[3])+s_meanMaxAcc+str(A[4])+s_meanEPD+str(A[5])+s_meanRealDist+str(A[6])+s_meanDistTraversed+str(A[7])+s_meanDistPer+str(A[8])+s_maxReact+str(max_react)+s_maxMove+str(max_move)+s_maxEPD+str(max_epd)+s_maxMaxVel+str(max_vel)+s_maxMaxAcc+str(max_acc)+s_score+str(index_val)+"\n";
        rand_rawFile.write(res_str);
        self.writeToDatabase(4,A[0],A[1],A[2],A[3],A[4],A[5],A[6],A[7],A[8],max_react,max_move,max_epd,max_vel,max_acc,index_val);

        A = np.zeros(9);
        max_react,max_move,max_epd,max_vel,max_acc = 0,0,0,0,0;
        for i in range(len(self.SequenceStrings)):
            seq_rawFile.write(self.SequenceStrings[i])
            if i==0:
                continue;
            temp_data = [float(j) for j in self.SequenceStrings[i].split()];
            tdnp = np.array(temp_data[1:]);
            if tdnp[0]>max_react:
                max_react = tdnp[0];
            if tdnp[1]>max_move:
                max_move = tdnp[1];
            if tdnp[5]>max_epd:
                max_epd = tdnp[5];
            if tdnp[3]>max_vel:
                max_vel = tdnp[3];
            if tdnp[4]>max_acc:
                max_acc = tdnp[4];
            A = A+tdnp;
        A = A/(len(self.SequenceStrings));
        index_val = ((100-A[8])/100)+((49.7-A[5])/49.7)+((1.165-A[0])/1.165);
        index_val = index_val*10/3;
        res_str=s_meanReact+str(A[0])+s_meanMove+str(A[1])+s_meanResponse+str(A[2])+s_meanMaxVel+str(A[3])+s_meanMaxAcc+str(A[4])+s_meanEPD+str(A[5])+s_meanRealDist+str(A[6])+s_meanDistTraversed+str(A[7])+s_meanDistPer+str(A[8])+s_maxReact+str(max_react)+s_maxMove+str(max_move)+s_maxEPD+str(max_epd)+s_maxMaxVel+str(max_vel)+s_maxMaxAcc+str(max_acc)+s_score+str(index_val)+"\n";
        seq_rawFile.write(res_str);
        self.writeToDatabase(3,A[0],A[1],A[2],A[3],A[4],A[5],A[6],A[7],A[8],max_react,max_move,max_epd,max_vel,max_acc,index_val);

        A = np.zeros(9);
        max_react,max_move,max_epd,max_vel,max_acc = 0,0,0,0,0;
        for i in range(len(self.RandomGoodStrings)):
            rand_filterFile.write(self.RandomGoodStrings[i])
            if i==0:
                continue;
            temp_data = [float(j) for j in self.RandomGoodStrings[i].split()];
            tdnp = np.array(temp_data[1:]);
            if tdnp[0]>max_react:
                max_react = tdnp[0];
            if tdnp[1]>max_move:
                max_move = tdnp[1];
            if tdnp[5]>max_epd:
                max_epd = tdnp[5];
            if tdnp[3]>max_vel:
                max_vel = tdnp[3];
            if tdnp[4]>max_acc:
                max_acc = tdnp[4];
            A = A+tdnp;
        A = A/(len(self.RandomGoodStrings));
       index_val = ((100-A[8])/100)+((49.7-A[5])/49.7)+((1.165-A[0])/1.165);
        index_val = index_val*10/3;
        res_str=s_meanReact+str(A[0])+s_meanMove+str(A[1])+s_meanResponse+str(A[2])+s_meanMaxVel+str(A[3])+s_meanMaxAcc+str(A[4])+s_meanEPD+str(A[5])+s_meanRealDist+str(A[6])+s_meanDistTraversed+str(A[7])+s_meanDistPer+str(A[8])+s_maxReact+str(max_react)+s_maxMove+str(max_move)+s_maxEPD+str(max_epd)+s_maxMaxVel+str(max_vel)+s_maxMaxAcc+str(max_acc)+s_score+str(index_val)+"\n";
        rand_filterFile.write(res_str);
        self.writeToDatabase(2,A[0],A[1],A[2],A[3],A[4],A[5],A[6],A[7],A[8],max_react,max_move,max_epd,max_vel,max_acc,index_val);

        A = np.zeros(9);
        max_react,max_move,max_epd,max_vel,max_acc = 0,0,0,0,0;
        for i in range(len(self.SequenceGoodStrings)):
            seq_filterFile.write(self.SequenceGoodStrings[i])
            if i==0:
                continue;
            temp_data = [float(j) for j in self.SequenceGoodStrings[i].split()];
            tdnp = np.array(temp_data[1:]);
            if tdnp[0]>max_react:
                max_react = tdnp[0];
            if tdnp[1]>max_move:
                max_move = tdnp[1];
            if tdnp[5]>max_epd:
                max_epd = tdnp[5];
            if tdnp[3]>max_vel:
                max_vel = tdnp[3];
            if tdnp[4]>max_acc:
                max_acc = tdnp[4];
            A = A+tdnp;
        A = A/(len(self.SequenceGoodStrings));
        index_val = ((100-A[8])/100)+((49.7-A[5])/49.7)+((1.165-A[0])/1.165);
        index_val = index_val*10/3;
        res_str=s_meanReact+str(A[0])+s_meanMove+str(A[1])+s_meanResponse+str(A[2])+s_meanMaxVel+str(A[3])+s_meanMaxAcc+str(A[4])+s_meanEPD+str(A[5])+s_meanRealDist+str(A[6])+s_meanDistTraversed+str(A[7])+s_meanDistPer+str(A[8])+s_maxReact+str(max_react)+s_maxMove+str(max_move)+s_maxEPD+str(max_epd)+s_maxMaxVel+str(max_vel)+s_maxMaxAcc+str(max_acc)+s_score+str(index_val)+"\n";
        seq_filterFile.write(res_str);
        self.writeToDatabase(1,A[0],A[1],A[2],A[3],A[4],A[5],A[6],A[7],A[8],max_react,max_move,max_epd,max_vel,max_acc,index_val);
        
        print "written analysis files"

    def deleteRecord(self):
        print "delete this record"
        self.deleteThisRecord = 1;

    def quit(self):
        self.cnx.commit();
        self.cnx.close();
        exit()
 
if __name__ == '__main__':
    
    fig1 = plt.figure()
    ax1f1 = fig1.add_subplot(111)
    ax1f1.plot(np.random.rand(5))
 
    fig2 = plt.figure()
    ax1f2 = fig2.add_subplot(121)
    ax1f2.plot(np.random.rand(5))
    ax2f2 = fig2.add_subplot(122)
    ax2f2.plot(np.random.rand(10))
 
    app = QtGui.QApplication(sys.argv)
    #print QtGui.QDesktopWidget().width(), QtGui.QDesktopWidget().height()
    #print QtGui.QX11Info.appDpiX(), QtGui.QX11Info.appDpiX() 
    main = Main()
    main.addplot(fig1)
    main.show()
    main.rmplot()
    main.addplot(fig2)
    sys.exit(app.exec_())
