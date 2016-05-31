import sys
import os
from PyQt4 import QtGui
from subprocess import Popen, PIPE
import winsound
from win32api import GetSystemMetrics
from collection_GUI_prog import Ui_MainWindow

def dayTitle(x):
    return {
        1 : '_Day1_' ,
        2 : '_Day2_',
        3 : '_Day3_',
        4 : '_Day4_',
        5 : '_Day5_',
        6 : '_Baseline_',
        7 : '_Performance_'
    }.get(x,'_Familiarisation_')

class Form(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Form,self).__init__()
        self.setupUi(self);
        self.record.clicked.connect(self.runCPP);
        self.clear.clicked.connect(self.clear_data);
        self.quit.clicked.connect(self.quit_app);
        self.Horiz_text.setText(str(GetSystemMetrics(0)))
        self.Vert_text.setText(str(GetSystemMetrics(1)))

    def clear_data(self):
        self.patient_text.setText("");
        self.combo_day.setCurrentIndex(0);
        self.combo_block.setCurrentIndex(0);
        
    def ensure_dir(self,f):
        d = os.path.dirname(f)
        print os.path.exists(d)
        if not os.path.exists(d):
            os.makedirs(d)
        
    def runCPP(self):
        subNo = str(self.patient_text.text())
        dayNo = self.combo_day.currentIndex()+1;
        block = self.combo_block.currentIndex()
        horiz = self.Horiz_text.text()
        vert = self.Vert_text.text()
        s1 = 'C:\\Users\\neuro\\Documents\\Arna\\Tracker\\Data\\Subject ' + str(subNo)+'\\';
        self.ensure_dir(s1);
        s = '"C:\\Users\\neuro\\Documents\\Visual Studio 2015\\Projects\\MohandTracker\\Debug\\MohandTracker.exe" ' + subNo + ' ' + str(dayNo) + ' ' + str(block) +' ' + horiz + ' ' + vert;
        p = Popen(str(s), shell=True, stdout=PIPE, stdin=PIPE)
        result = p.stdout.readline().strip()
        print result
        if(result == 'Started'):
            winsound.Beep(2500,400); #Beep(frequency,duration_in_ms)
        new_block = (1+block)%5;
        self.combo_block.setCurrentIndex(new_block);

    def quit_app(self):
        exit()

if __name__ == '__main__':
    print "Width = ", GetSystemMetrics(0)
    print "Height = ", GetSystemMetrics(1)
    app = QtGui.QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec_())
