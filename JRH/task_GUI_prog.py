# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'task_GUI.ui'
#
# Created: Fri Jun 10 08:23:18 2016
#      by: PyQt4 UI code generator 4.11
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
        MainWindow.resize(944, 507)
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
        self.subjectName.setGeometry(QtCore.QRect(250, 60, 121, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.subjectName.setFont(font)
        self.subjectName.setObjectName(_fromUtf8("subjectName"))
        self.trials = QtGui.QLabel(self.centralwidget)
        self.trials.setGeometry(QtCore.QRect(140, 250, 71, 21))
        self.trials.setObjectName(_fromUtf8("trials"))
        self.subName = QtGui.QLineEdit(self.centralwidget)
        self.subName.setGeometry(QtCore.QRect(410, 60, 171, 31))
        self.subName.setObjectName(_fromUtf8("subName"))
        self.totalTrials = QtGui.QLineEdit(self.centralwidget)
        self.totalTrials.setGeometry(QtCore.QRect(230, 240, 161, 31))
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
        self.label_trialTime.setGeometry(QtCore.QRect(460, 240, 171, 31))
        self.label_trialTime.setObjectName(_fromUtf8("label_trialTime"))
        self.trialTime = QtGui.QLineEdit(self.centralwidget)
        self.trialTime.setGeometry(QtCore.QRect(660, 240, 121, 31))
        self.trialTime.setObjectName(_fromUtf8("trialTime"))
        self.LearningParam = QtGui.QLabel(self.centralwidget)
        self.LearningParam.setGeometry(QtCore.QRect(60, 180, 301, 41))
        self.LearningParam.setObjectName(_fromUtf8("LearningParam"))
        self.label_fb = QtGui.QLabel(self.centralwidget)
        self.label_fb.setGeometry(QtCore.QRect(300, 290, 81, 21))
        self.label_fb.setObjectName(_fromUtf8("label_fb"))
        self.combo_fb = QtGui.QComboBox(self.centralwidget)
        self.combo_fb.setGeometry(QtCore.QRect(410, 290, 69, 22))
        self.combo_fb.setObjectName(_fromUtf8("combo_fb"))
        self.combo_fb.addItem(_fromUtf8(""))
        self.combo_fb.addItem(_fromUtf8(""))
        self.label_init = QtGui.QLabel(self.centralwidget)
        self.label_init.setGeometry(QtCore.QRect(10, 120, 161, 31))
        self.label_init.setObjectName(_fromUtf8("label_init"))
        self.label_max = QtGui.QLabel(self.centralwidget)
        self.label_max.setGeometry(QtCore.QRect(450, 110, 261, 41))
        self.label_max.setObjectName(_fromUtf8("label_max"))
        self.text_init = QtGui.QLineEdit(self.centralwidget)
        self.text_init.setGeometry(QtCore.QRect(180, 120, 231, 21))
        self.text_init.setObjectName(_fromUtf8("text_init"))
        self.text_max = QtGui.QLineEdit(self.centralwidget)
        self.text_max.setGeometry(QtCore.QRect(720, 120, 211, 21))
        self.text_max.setObjectName(_fromUtf8("text_max"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 944, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.combo_fb.setCurrentIndex(1)
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
        self.label_fb.setText(_translate("MainWindow", "Feedback", None))
        self.combo_fb.setItemText(0, _translate("MainWindow", "No", None))
        self.combo_fb.setItemText(1, _translate("MainWindow", "Yes", None))
        self.label_init.setText(_translate("MainWindow", "Gripper Initial Value", None))
        self.label_max.setText(_translate("MainWindow", "Max Voluntary Contraction Value", None))

