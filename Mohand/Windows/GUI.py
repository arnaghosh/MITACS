import sys
import os
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from subprocess import Popen, PIPE
import winsound
from win32api import GetSystemMetrics

def dayTitle(x):
    return {
        1 : '_Day1_' ,
        2 : '_Day2_',
        3 : '_Day3_',
        4 : '_Day4_',
        5 : '_Day5_',
        6 : '_Baseline_',
    }.get(x,'_Performance_')

class Form:
    def window(self):
        app = QApplication(sys.argv)
        w = QWidget()
        record = QPushButton(w)
        record.setText("Record Tracking Data")
        record.clicked.connect(self.runCPP)
        w.setGeometry(50,50,530,480)
        record.move(20,440)

        quit = QPushButton(w)
        quit.setText("Quit")
        quit.clicked.connect(self.quit)
        quit.move(420,440)

        self.McGillMed = QLabel(w);
        self.McGillMed.move(275,35);
        self.McGillMed.setGeometry(275,35,250,60);
        pixMap1 = QPixmap(os.getcwd() + "/medicine_logo_horiz_eng_outlined_750.png")
        pixMapScaled1 = pixMap1.scaled(self.McGillMed.size(), Qt.KeepAspectRatio)
        self.McGillMed.setPixmap(pixMapScaled1)

        self.REPAR = QLabel(w);
        self.REPAR.move(20,25);
        self.REPAR.setGeometry(20,25,250,60);
        pixMap2 = QPixmap(os.getcwd() + "/13552-REPAR-COUL.png")
        pixMapScaled2 = pixMap2.scaled(self.REPAR.size(), Qt.KeepAspectRatio)
        self.REPAR.setPixmap(pixMapScaled2)


        self.patient_label = QLabel(w)
        self.patient_label.setText("Enter Subject Number")
        self.patient_label.move(20,120)
        self.patient_text = QLineEdit(w)
        self.patient_text.move(250,120)

        self.day_label = QLabel(w)
        self.day_label.setText("Enter Day (6 for baseline and 7 for retention)")
        self.day_label.move(20,170)
        self.day_text = QLineEdit(w)
        self.day_text.move(250,170)

        self.block_label = QLabel(w)
        self.block_label.setText("Enter Block")
        self.block_label.move(20,220)
        self.block_text = QLineEdit(w)
        self.block_text.move(250,220)

        self.Screen_label = QLabel(w)
        self.Screen_label.setText("Enter Screen Resolution")
        self.Screen_label.move(20,290)

        self.Horiz_label = QLabel(w)
        self.Horiz_label.setText("Horizontal")
        self.Horiz_label.move(20,340)
        self.Horiz_text = QLineEdit(w)
        self.Horiz_text.move(90,340)
        self.Horiz_text.setText(str(GetSystemMetrics(0)))

        self.Vert_label = QLabel(w)
        self.Vert_label.setText("Vertical")
        self.Vert_label.move(300,340)
        self.Vert_text = QLineEdit(w)
        self.Vert_text.move(360,340)
        self.Vert_text.setText(str(GetSystemMetrics(1)))

        w.setWindowTitle("Mohand's Task")
        w.show()
        sys.exit(app.exec_())

    def ensure_dir(self,f):
        d = os.path.dirname(f)
        print os.path.exists(d)
        if not os.path.exists(d):
            os.makedirs(d)
        
    def runCPP(self):
        subNo = self.patient_text.text()
        dayNo = self.day_text.text()
        block = self.block_text.text()
        horiz = self.Horiz_text.text()
        vert = self.Vert_text.text()
        s1 = 'C:\\Users\\Arna\\Documents\\Arna\\Tracker\\Data\\Subject ' + str(subNo)+'\\';
        self.ensure_dir(s1);
        s = '"C:\\Users\\Arna\\Documents\\Visual Studio 2015\\Projects\\Mohand\'sTracker1\\Debug\\Mohand\'sTracker1.exe" ' + subNo + ' ' + dayNo + ' ' + block +' ' + horiz + ' ' + vert;
        p = Popen(str(s), shell=True, stdout=PIPE, stdin=PIPE)
        result = p.stdout.readline().strip()
        print result
        if(result == 'Started'):
            winsound.Beep(2500,400); #Beep(frequency,duration_in_ms)

    def quit(self):
        exit()

if __name__ == '__main__':
    print "Width = ", GetSystemMetrics(0)
    print "Height = ", GetSystemMetrics(1)
    form = Form()
    form.window()
