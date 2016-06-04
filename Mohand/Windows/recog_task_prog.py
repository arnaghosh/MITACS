# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'recog_task.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(651, 409)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("MS Sans Serif"))
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        MainWindow.setFont(font)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.logo1 = QtGui.QLabel(self.centralwidget)
        self.logo1.setGeometry(QtCore.QRect(10, 10, 161, 91))
        self.logo1.setText(_fromUtf8(""))
        self.logo1.setPixmap(QtGui.QPixmap(_fromUtf8("13552-REPAR-COUL.png")))
        self.logo1.setObjectName(_fromUtf8("logo1"))
        self.logo2 = QtGui.QLabel(self.centralwidget)
        self.logo2.setGeometry(QtCore.QRect(390, 20, 261, 71))
        self.logo2.setText(_fromUtf8(""))
        self.logo2.setPixmap(QtGui.QPixmap(_fromUtf8("medicine_logo_horiz_eng_outlined_750.png")))
        self.logo2.setObjectName(_fromUtf8("logo2"))
        self.subNo = QtGui.QLabel(self.centralwidget)
        self.subNo.setGeometry(QtCore.QRect(100, 130, 121, 31))
        self.subNo.setObjectName(_fromUtf8("subNo"))
        self.subjectNo = QtGui.QLineEdit(self.centralwidget)
        self.subjectNo.setGeometry(QtCore.QRect(290, 130, 151, 21))
        self.subjectNo.setObjectName(_fromUtf8("subjectNo"))
        self.screenResol = QtGui.QLabel(self.centralwidget)
        self.screenResol.setGeometry(QtCore.QRect(40, 190, 211, 21))
        self.screenResol.setObjectName(_fromUtf8("screenResol"))
        self.horiz = QtGui.QLabel(self.centralwidget)
        self.horiz.setGeometry(QtCore.QRect(100, 240, 91, 16))
        self.horiz.setObjectName(_fromUtf8("horiz"))
        self.vert = QtGui.QLabel(self.centralwidget)
        self.vert.setGeometry(QtCore.QRect(390, 240, 71, 21))
        self.vert.setObjectName(_fromUtf8("vert"))
        self.horiz_text = QtGui.QLineEdit(self.centralwidget)
        self.horiz_text.setGeometry(QtCore.QRect(220, 240, 113, 20))
        self.horiz_text.setObjectName(_fromUtf8("horiz_text"))
        self.vert_text = QtGui.QLineEdit(self.centralwidget)
        self.vert_text.setGeometry(QtCore.QRect(500, 240, 113, 20))
        self.vert_text.setObjectName(_fromUtf8("vert_text"))
        self.button_start = QtGui.QPushButton(self.centralwidget)
        self.button_start.setGeometry(QtCore.QRect(40, 310, 171, 31))
        self.button_start.setObjectName(_fromUtf8("button_start"))
        self.button_clear = QtGui.QPushButton(self.centralwidget)
        self.button_clear.setGeometry(QtCore.QRect(290, 310, 101, 31))
        self.button_clear.setObjectName(_fromUtf8("button_clear"))
        self.button_quit = QtGui.QPushButton(self.centralwidget)
        self.button_quit.setGeometry(QtCore.QRect(470, 310, 101, 31))
        self.button_quit.setObjectName(_fromUtf8("button_quit"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 651, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Recognition Task GUI", None))
        self.subNo.setText(_translate("MainWindow", "Subject Number", None))
        self.screenResol.setText(_translate("MainWindow", "Enter Screen Resolution", None))
        self.horiz.setText(_translate("MainWindow", "Horizontal", None))
        self.vert.setText(_translate("MainWindow", "Vertical", None))
        self.button_start.setText(_translate("MainWindow", "Start Recognition Task", None))
        self.button_clear.setText(_translate("MainWindow", "Clear", None))
        self.button_quit.setText(_translate("MainWindow", "Quit", None))

