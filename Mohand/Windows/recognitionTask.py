import sys
import os
from PyQt4 import QtGui
from subprocess import Popen, PIPE
import pywinauto, win32gui
from win32api import GetSystemMetrics
from recog_task_prog import Ui_MainWindow
import mysql.connector

class Main(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Main,self).__init__()
        self.setupUi(self);
        self.button_start.clicked.connect(self.task);
        self.button_clear.clicked.connect(self.clear);
        self.button_quit.clicked.connect(self.quit);
        self.horiz_text.setText(str(GetSystemMetrics(0)))
        self.vert_text.setText(str(GetSystemMetrics(1)))
        self.optionChosen = 0;
        self.cnx = mysql.connector.connect(user='root',password='neuro',database='mohand');
        self.cursor = self.cnx.cursor();

    def option(self,s):
        #print str(s);
        if str(s)=="&Yes":
            return 1;
        else: return 0;            

    def clear(self):
        self.subjectNo.setText("");

    def quit(self):
        self.cnx.close();
        exit();

    def ensure_dir(self,f):
        d = os.path.dirname(f)
        print os.path.exists(d)
        if not os.path.exists(d):
            os.makedirs(d)
    
    def msgbtn(self,i):
       #print "Button pressed is:",i.text()
       self.optionChosen = self.option(i.text());
   
    def showdialog(self, handle):
        if handle!=win32gui.GetForegroundWindow():            
            app = pywinauto.application.Application();
            window = app.window_(handle=handle)
            window.Minimize()
            window.Restore()
            window.SetFocus()
        msg = QtGui.QMessageBox()
        msg.setIcon(QtGui.QMessageBox.Question)
        msg.setFixedSize(250, 100); 
        msg.move((GetSystemMetrics(0))/2,(GetSystemMetrics(1))/2);
        msg.setText("Do you recognise this sequence?")
        msg.setInformativeText("If you recognise the sequence you just saw, Click Yes or else click No.")
        msg.setWindowTitle("MessageBox demo")
        msg.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        msg.buttonClicked.connect(self.msgbtn)
        retval = msg.exec_()
   
    def task(self):
        subNo = str(self.subjectNo.text())
        horiz = self.horiz_text.text()
        vert = self.vert_text.text()
        s1 = 'C:\\Users\\neuro\\Documents\\Arna\\Tracker\\Data\\Subject ' + str(subNo)+'\\';
        self.ensure_dir(s1);
        file_s = 'C:\\Users\\neuro\\Documents\\Arna\\Tracker\\Data\\Subject ' + str(subNo)+'\\Subject'+str(subNo)+'_Recognition.txt';
        recog_file = open(file_s,'w');
        s = '"C:\\Users\\neuro\\Documents\\Visual Studio 2015\\Projects\\RecognitionTask\\Debug\\RecognitionTask.exe" ' + subNo +' ' + horiz + ' ' + vert;
        p = Popen(str(s), shell=True, stdout=PIPE, stdin=PIPE)
        count_trial = 1;
        score = 0;
        handle = pywinauto.findwindows.find_windows(title = "Recognition Task GUI")[0];
        repeatedTargetArray = [2,5,9,11,14];
        while(count_trial<=15):
            result = p.stdout.readline().strip()
            print result
            if(result == 'DONE'):
                self.showdialog(handle);
                #print self.optionChosen
                if (count_trial in repeatedTargetArray):
                    score = score + self.optionChosen; #Yes is correct answer.
                else :
                    score = score +(1-self.optionChosen); #No is correct answer
                #print score
                response_str = str(self.optionChosen)+'\n';
                recog_file.write(response_str);
                p.stdin.write('1\n');
                p.stdin.flush();
                count_trial= count_trial+1;
            if (result =='Escaped'):
                break;
        score = score*100.0/(count_trial-1);
        response_str = "Score = "+str(int(score))+'\n';
        recog_file.write(response_str);
        recog_file.close();
        database_s = "update subjectinfo set recognition_score=" + str(int(score)) + " where subNo="+str(subNo);
        self.cursor.execute(database_s);
        self.cnx.commit();
        #print score


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    form = Main()
    form.show()
    sys.exit(app.exec_())
