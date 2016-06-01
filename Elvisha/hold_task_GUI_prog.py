# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'hold_task.ui'
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
        MainWindow.resize(841, 507)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("MS Reference Sans Serif"))
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        MainWindow.setFont(font)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.logo1 = QtGui.QLabel(self.centralwidget)
        self.logo1.setGeometry(QtCore.QRect(540, 20, 281, 51))
        self.logo1.setText(_fromUtf8(""))
        self.logo1.setPixmap(QtGui.QPixmap(_fromUtf8("medicine_logo_horiz_eng_outlined_750.png")))
        self.logo1.setObjectName(_fromUtf8("logo1"))
        self.subjectName = QtGui.QLabel(self.centralwidget)
        self.subjectName.setGeometry(QtCore.QRect(250, 130, 121, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.subjectName.setFont(font)
        self.subjectName.setObjectName(_fromUtf8("subjectName"))
        self.trials = QtGui.QLabel(self.centralwidget)
        self.trials.setGeometry(QtCore.QRect(120, 260, 71, 21))
        self.trials.setObjectName(_fromUtf8("trials"))
        self.subName = QtGui.QLineEdit(self.centralwidget)
        self.subName.setGeometry(QtCore.QRect(410, 130, 171, 31))
        self.subName.setObjectName(_fromUtf8("subName"))
        self.totalTrials = QtGui.QLineEdit(self.centralwidget)
        self.totalTrials.setGeometry(QtCore.QRect(210, 250, 161, 31))
        self.totalTrials.setObjectName(_fromUtf8("totalTrials"))
        self.getMax = QtGui.QPushButton(self.centralwidget)
        self.getMax.setGeometry(QtCore.QRect(50, 350, 251, 41))
        self.getMax.setObjectName(_fromUtf8("getMax"))
        self.hold = QtGui.QPushButton(self.centralwidget)
        self.hold.setGeometry(QtCore.QRect(350, 350, 121, 41))
        self.hold.setObjectName(_fromUtf8("hold"))
        self.learn = QtGui.QPushButton(self.centralwidget)
        self.learn.setGeometry(QtCore.QRect(520, 350, 161, 41))
        self.learn.setObjectName(_fromUtf8("learn"))
        self.quit = QtGui.QPushButton(self.centralwidget)
        self.quit.setGeometry(QtCore.QRect(750, 350, 81, 41))
        self.quit.setObjectName(_fromUtf8("quit"))
        self.label_trialTime = QtGui.QLabel(self.centralwidget)
        self.label_trialTime.setGeometry(QtCore.QRect(440, 250, 171, 31))
        self.label_trialTime.setObjectName(_fromUtf8("label_trialTime"))
        self.trialTime = QtGui.QLineEdit(self.centralwidget)
        self.trialTime.setGeometry(QtCore.QRect(640, 250, 121, 31))
        self.trialTime.setObjectName(_fromUtf8("trialTime"))
        self.LearningParam = QtGui.QLabel(self.centralwidget)
        self.LearningParam.setGeometry(QtCore.QRect(40, 190, 301, 41))
        self.LearningParam.setObjectName(_fromUtf8("LearningParam"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 841, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.subjectName.setText(_translate("MainWindow", "Subject Name", None))
        self.trials.setText(_translate("MainWindow", "Trials", None))
        self.getMax.setText(_translate("MainWindow", "Get Max Voluntary Contraction", None))
        self.hold.setText(_translate("MainWindow", "Hold Task", None))
        self.learn.setText(_translate("MainWindow", "Motor Learning Task", None))
        self.quit.setText(_translate("MainWindow", "Quit", None))
        self.label_trialTime.setText(_translate("MainWindow", "Trial Time (in seconds)", None))
        self.LearningParam.setText(_translate("MainWindow", "Learning Task Parameters :", None))

