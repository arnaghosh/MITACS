import os,sys,math,random
import numpy as np
from database_GUI import Ui_MainWindow
import mysql.connector
from PyQt4 import QtGui

def gender(x):
        return {
            0: 'Male',
            1: 'Female'
        }.get(x)

def hand(x):
        return {
            0: 'Right',
            1: 'Left'
        }.get(x)

def leisureFreq(x):
        return {
            0: 'Almost Every Day',
            1: '5 times per week',
            2: '2-3 times per week',
            3: 'Once per week',
            4: '<1 per week'
        }.get(x)

def dayTime(x):
        return {
            0: '9 to 11',
            1: '11 to 13',
            2: '13 to 15'
        }.get(x)
    

class Main(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Main,self).__init__()
        self.setupUi(self);
        self.button_submit.clicked.connect(self.enter);
        self.button_clear.clicked.connect(self.clear);
        self.button_quit.clicked.connect(self.quit);
        self.tdcsArray = np.loadtxt("tdcs_original.txt");
        self.cnx = mysql.connector.connect(user='root',password='neuro',database='mohand');
        self.cursor = self.cnx.cursor();
        self.add_str = ("insert into subjectInfo (subNo,subName,age,gender,nativeTongue,hand,occupation,tdcsNo,leisureFreq,week,dayTime,sham_tdcs) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)");


    def clear(self):
        self.text_subNum.setText("");
        self.text_subjectName.setText("");
        self.text_age.setText("");
        self.combo_gender.setCurrentIndex(0);
        self.text_lang.setText("");
        self.combo_hand.setCurrentIndex(0);
        self.text_occupation.setText("");
        self.text_TDCS.setText("");
        self.combo_leisure.setCurrentIndex(0);
        self.text_week.setText("");
        self.combo_time.setCurrentIndex(0);

    
    def enter(self):
        subNum = int(self.text_subNum.text());
        subName = str(self.text_subjectName.text());
        subAge = int(self.text_age.text());
        subGender = str(gender(self.combo_gender.currentIndex()));
        subLang = str(self.text_lang.text());
        subHand = str(hand(self.combo_hand.currentIndex()));
        subOcc = str(self.text_occupation.text());
        subTDCS = int(self.text_TDCS.text());
        subLeisure = str(leisureFreq(self.combo_leisure.currentIndex()));
        subWeek = int(self.text_week.text());
        subTime = str(dayTime(self.combo_time.currentIndex()));
        shamStr = "Yes";
        if subTDCS in self.tdcsArray:
              shamStr = "No";  
        val_str = (subNum,subName,subAge,subGender,subLang,subHand,subOcc,subTDCS,subLeisure,subWeek,subTime,shamStr);
        comb_str = (self.add_str,val_str);
        #print comb_str;
        self.cursor.execute(self.add_str,val_str);
        print "entered in database"                     

    def quit(self):
        self.cnx.commit();
        self.cnx.close();
        exit()
        

if __name__== '__main__':

    app = QtGui.QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())
