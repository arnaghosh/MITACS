# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'task_GUI.ui'
#
# Created: Fri Jul 15 14:38:05 2016
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
        MainWindow.resize(1025, 626)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("MS Reference Sans Serif"))
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        MainWindow.setFont(font)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.subjectName = QtGui.QLabel(self.centralwidget)
        self.subjectName.setGeometry(QtCore.QRect(300, 50, 121, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.subjectName.setFont(font)
        self.subjectName.setObjectName(_fromUtf8("subjectName"))
        self.trials = QtGui.QLabel(self.centralwidget)
        self.trials.setGeometry(QtCore.QRect(31, 270, 39, 16))
        self.trials.setObjectName(_fromUtf8("trials"))
        self.subName = QtGui.QLineEdit(self.centralwidget)
        self.subName.setGeometry(QtCore.QRect(460, 50, 171, 31))
        self.subName.setObjectName(_fromUtf8("subName"))
        self.totalTrials = QtGui.QLineEdit(self.centralwidget)
        self.totalTrials.setGeometry(QtCore.QRect(80, 270, 81, 22))
        self.totalTrials.setObjectName(_fromUtf8("totalTrials"))
        self.getMax = QtGui.QPushButton(self.centralwidget)
        self.getMax.setGeometry(QtCore.QRect(160, 480, 251, 41))
        self.getMax.setObjectName(_fromUtf8("getMax"))
        self.hold = QtGui.QPushButton(self.centralwidget)
        self.hold.setGeometry(QtCore.QRect(630, 480, 131, 41))
        self.hold.setObjectName(_fromUtf8("hold"))
        self.learn = QtGui.QPushButton(self.centralwidget)
        self.learn.setGeometry(QtCore.QRect(450, 530, 161, 41))
        self.learn.setObjectName(_fromUtf8("learn"))
        self.quit = QtGui.QPushButton(self.centralwidget)
        self.quit.setGeometry(QtCore.QRect(820, 500, 81, 41))
        self.quit.setObjectName(_fromUtf8("quit"))
        self.label_trialTime = QtGui.QLabel(self.centralwidget)
        self.label_trialTime.setGeometry(QtCore.QRect(249, 270, 172, 16))
        self.label_trialTime.setObjectName(_fromUtf8("label_trialTime"))
        self.trialTime = QtGui.QLineEdit(self.centralwidget)
        self.trialTime.setGeometry(QtCore.QRect(430, 270, 91, 22))
        self.trialTime.setObjectName(_fromUtf8("trialTime"))
        self.LearningParam = QtGui.QLabel(self.centralwidget)
        self.LearningParam.setGeometry(QtCore.QRect(60, 210, 301, 41))
        self.LearningParam.setObjectName(_fromUtf8("LearningParam"))
        self.label_fb = QtGui.QLabel(self.centralwidget)
        self.label_fb.setGeometry(QtCore.QRect(173, 331, 71, 21))
        self.label_fb.setObjectName(_fromUtf8("label_fb"))
        self.combo_fb = QtGui.QComboBox(self.centralwidget)
        self.combo_fb.setGeometry(QtCore.QRect(270, 331, 52, 22))
        self.combo_fb.setObjectName(_fromUtf8("combo_fb"))
        self.combo_fb.addItem(_fromUtf8(""))
        self.combo_fb.addItem(_fromUtf8(""))
        self.label_init = QtGui.QLabel(self.centralwidget)
        self.label_init.setGeometry(QtCore.QRect(60, 110, 161, 31))
        self.label_init.setObjectName(_fromUtf8("label_init"))
        self.label_max = QtGui.QLabel(self.centralwidget)
        self.label_max.setGeometry(QtCore.QRect(500, 100, 261, 41))
        self.label_max.setObjectName(_fromUtf8("label_max"))
        self.text_init = QtGui.QLineEdit(self.centralwidget)
        self.text_init.setGeometry(QtCore.QRect(230, 110, 231, 21))
        self.text_init.setObjectName(_fromUtf8("text_init"))
        self.text_max = QtGui.QLineEdit(self.centralwidget)
        self.text_max.setGeometry(QtCore.QRect(770, 110, 211, 21))
        self.text_max.setObjectName(_fromUtf8("text_max"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(590, 270, 39, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.combo_block = QtGui.QComboBox(self.centralwidget)
        self.combo_block.setGeometry(QtCore.QRect(645, 270, 238, 22))
        self.combo_block.setObjectName(_fromUtf8("combo_block"))
        self.combo_block.addItem(_fromUtf8(""))
        self.combo_block.addItem(_fromUtf8(""))
        self.combo_block.addItem(_fromUtf8(""))
        self.combo_block.addItem(_fromUtf8(""))
        self.combo_block.addItem(_fromUtf8(""))
        self.combo_block.addItem(_fromUtf8(""))
        self.combo_block.addItem(_fromUtf8(""))
        self.combo_block.addItem(_fromUtf8(""))
        self.label_scoreThresh = QtGui.QLabel(self.centralwidget)
        self.label_scoreThresh.setGeometry(QtCore.QRect(420, 331, 223, 21))
        self.label_scoreThresh.setObjectName(_fromUtf8("label_scoreThresh"))
        self.text_scoreThresh = QtGui.QLineEdit(self.centralwidget)
        self.text_scoreThresh.setGeometry(QtCore.QRect(660, 331, 71, 22))
        self.text_scoreThresh.setObjectName(_fromUtf8("text_scoreThresh"))
        self.loadMax = QtGui.QPushButton(self.centralwidget)
        self.loadMax.setGeometry(QtCore.QRect(160, 530, 261, 41))
        self.loadMax.setObjectName(_fromUtf8("loadMax"))
        self.isometric = QtGui.QPushButton(self.centralwidget)
        self.isometric.setGeometry(QtCore.QRect(630, 530, 161, 41))
        self.isometric.setObjectName(_fromUtf8("isometric"))
        self.logo1 = QtGui.QLabel(self.centralwidget)
        self.logo1.setGeometry(QtCore.QRect(740, 10, 251, 51))
        self.logo1.setText(_fromUtf8(""))
        self.logo1.setPixmap(QtGui.QPixmap(_fromUtf8("medicine_logo_horiz_eng_outlined_750.png")))
        self.logo1.setObjectName(_fromUtf8("logo1"))
        self.isometricParam = QtGui.QLabel(self.centralwidget)
        self.isometricParam.setGeometry(QtCore.QRect(60, 389, 241, 31))
        self.isometricParam.setObjectName(_fromUtf8("isometricParam"))
        self.trialTime_2 = QtGui.QLabel(self.centralwidget)
        self.trialTime_2.setGeometry(QtCore.QRect(270, 440, 172, 16))
        self.trialTime_2.setObjectName(_fromUtf8("trialTime_2"))
        self.text_isoTrialTime = QtGui.QLineEdit(self.centralwidget)
        self.text_isoTrialTime.setGeometry(QtCore.QRect(490, 440, 101, 22))
        self.text_isoTrialTime.setObjectName(_fromUtf8("text_isoTrialTime"))
        self.time_forHold = QtGui.QLabel(self.centralwidget)
        self.time_forHold.setGeometry(QtCore.QRect(110, 160, 251, 41))
        self.time_forHold.setObjectName(_fromUtf8("time_forHold"))
        self.combo_holdTime = QtGui.QComboBox(self.centralwidget)
        self.combo_holdTime.setGeometry(QtCore.QRect(380, 170, 141, 21))
        self.combo_holdTime.setObjectName(_fromUtf8("combo_holdTime"))
        self.combo_holdTime.addItem(_fromUtf8(""))
        self.combo_holdTime.addItem(_fromUtf8(""))
        self.combo_holdTime.addItem(_fromUtf8(""))
        self.combo_holdTime.addItem(_fromUtf8(""))
        self.combo_holdTime.addItem(_fromUtf8(""))
        self.combo_holdTime.addItem(_fromUtf8(""))
        self.trials_famil_label = QtGui.QLabel(self.centralwidget)
        self.trials_famil_label.setGeometry(QtCore.QRect(580, 170, 201, 21))
        self.trials_famil_label.setObjectName(_fromUtf8("trials_famil_label"))
        self.text_trialFamil = QtGui.QLineEdit(self.centralwidget)
        self.text_trialFamil.setGeometry(QtCore.QRect(780, 170, 71, 20))
        self.text_trialFamil.setObjectName(_fromUtf8("text_trialFamil"))
        self.presentCross = QtGui.QPushButton(self.centralwidget)
        self.presentCross.setGeometry(QtCore.QRect(460, 480, 141, 41))
        self.presentCross.setObjectName(_fromUtf8("presentCross"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1025, 21))
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
        self.totalTrials.setText(_translate("MainWindow", "20", None))
        self.getMax.setText(_translate("MainWindow", "Get Max Voluntary Contraction", None))
        self.hold.setText(_translate("MainWindow", "Matching Task", None))
        self.learn.setText(_translate("MainWindow", "Motor Learning Task", None))
        self.quit.setText(_translate("MainWindow", "Quit", None))
        self.label_trialTime.setText(_translate("MainWindow", "Trial Time (in seconds)", None))
        self.trialTime.setText(_translate("MainWindow", "9", None))
        self.LearningParam.setText(_translate("MainWindow", "Learning Task Parameters :", None))
        self.label_fb.setText(_translate("MainWindow", "Feedback", None))
        self.combo_fb.setItemText(0, _translate("MainWindow", "No", None))
        self.combo_fb.setItemText(1, _translate("MainWindow", "Yes", None))
        self.label_init.setText(_translate("MainWindow", "Gripper Initial Value", None))
        self.label_max.setText(_translate("MainWindow", "Max Voluntary Contraction Value", None))
        self.label.setText(_translate("MainWindow", "Block", None))
        self.combo_block.setItemText(0, _translate("MainWindow", "Familiarization", None))
        self.combo_block.setItemText(1, _translate("MainWindow", "1", None))
        self.combo_block.setItemText(2, _translate("MainWindow", "2", None))
        self.combo_block.setItemText(3, _translate("MainWindow", "3", None))
        self.combo_block.setItemText(4, _translate("MainWindow", "4", None))
        self.combo_block.setItemText(5, _translate("MainWindow", "5", None))
        self.combo_block.setItemText(6, _translate("MainWindow", "Retention with no Feedback", None))
        self.combo_block.setItemText(7, _translate("MainWindow", "Retention with Feedback", None))
        self.label_scoreThresh.setText(_translate("MainWindow", "Score Threshold for feedback", None))
        self.text_scoreThresh.setText(_translate("MainWindow", "30", None))
        self.loadMax.setText(_translate("MainWindow", "Load Max Voluntary Contraction", None))
        self.isometric.setText(_translate("MainWindow", "Isometric Task", None))
        self.isometricParam.setText(_translate("MainWindow", "Isometric Task Parameters :", None))
        self.trialTime_2.setText(_translate("MainWindow", "Trial Time (in seconds)", None))
        self.text_isoTrialTime.setText(_translate("MainWindow", "120", None))
        self.time_forHold.setText(_translate("MainWindow", "Time after exercise (in minutes)", None))
        self.combo_holdTime.setItemText(0, _translate("MainWindow", "Familiarization", None))
        self.combo_holdTime.setItemText(1, _translate("MainWindow", "pre-exercise", None))
        self.combo_holdTime.setItemText(2, _translate("MainWindow", "30", None))
        self.combo_holdTime.setItemText(3, _translate("MainWindow", "60", None))
        self.combo_holdTime.setItemText(4, _translate("MainWindow", "90", None))
        self.combo_holdTime.setItemText(5, _translate("MainWindow", "120", None))
        self.trials_famil_label.setText(_translate("MainWindow", "Trials For Familiarization", None))
        self.text_trialFamil.setText(_translate("MainWindow", "10", None))
        self.presentCross.setText(_translate("MainWindow", "Present Cross", None))

