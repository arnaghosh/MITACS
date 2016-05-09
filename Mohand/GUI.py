import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from subprocess import Popen, PIPE

class Form:
    def window(self):
        app = QApplication(sys.argv)
        w = QWidget()
        record = QPushButton(w)
        record.setText("Record Tracking Data")
        record.clicked.connect(self.runCPP)
        w.setGeometry(50,50,700,500)
        record.move(20,20)

        quit = QPushButton(w)
        quit.setText("Quit")
        quit.clicked.connect(self.quit)
        quit.move(300,20)

        self.patient_label = QLabel(w)
        self.patient_label.setText("Enter Subject Number")
        self.patient_label.move(20,70)
        self.patient_text = QLineEdit(w)
        self.patient_text.move(250,70)

        self.day_label = QLabel(w)
        self.day_label.setText("Enter Day (0 for early practice)")
        self.day_label.move(20,120)
        self.day_text = QLineEdit(w)
        self.day_text.move(250,120)

        self.Screen_label = QLabel(w)
        self.Screen_label.setText("Enter Screen Resolution")
        self.Screen_label.move(20,170)

        self.Horiz_label = QLabel(w)
        self.Horiz_label.setText("Horizontal")
        self.Horiz_label.move(20,200)
        self.Horiz_text = QLineEdit(w)
        self.Horiz_text.move(150,200)

        self.Vert_label = QLabel(w)
        self.Vert_label.setText("Vertical")
        self.Vert_label.move(300,200)
        self.Vert_text = QLineEdit(w)
        self.Vert_text.move(450,200)

        w.setWindowTitle("Mohand's Task")
        w.show()
        sys.exit(app.exec_())

    def runCPP(self):
        subNo = self.patient_text.text()
        dayNo = self.day_text.text()
        horiz = self.Horiz_text.text()
        vert = self.Vert_text.text()
        s = './tracker ' + subNo + ' ' + dayNo + ' ' + horiz + ' ' + vert;
        p = Popen([s], shell=True, stdout=PIPE, stdin=PIPE)
        result = p.stdout.readline().strip()
        print result

    def quit(self):
        exit()

if __name__ == '__main__':
    form = Form()
    form.window()
