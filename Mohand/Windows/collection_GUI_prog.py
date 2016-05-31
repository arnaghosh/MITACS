# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'collection_GUI.ui'
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
        MainWindow.resize(1033, 699)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Leelawadee"))
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        MainWindow.setFont(font)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.logo1 = QtGui.QLabel(self.centralwidget)
        self.logo1.setGeometry(QtCore.QRect(50, 10, 141, 101))
        self.logo1.setText(_fromUtf8(""))
        self.logo1.setPixmap(QtGui.QPixmap(_fromUtf8("13552-REPAR-COUL.png")))
        self.logo1.setObjectName(_fromUtf8("logo1"))
        self.logo2 = QtGui.QLabel(self.centralwidget)
        self.logo2.setGeometry(QtCore.QRect(780, 40, 271, 61))
        self.logo2.setText(_fromUtf8(""))
        self.logo2.setPixmap(QtGui.QPixmap(_fromUtf8("medicine_logo_horiz_eng_outlined_750.png")))
        self.logo2.setObjectName(_fromUtf8("logo2"))
        self.subjectNo = QtGui.QLabel(self.centralwidget)
        self.subjectNo.setGeometry(QtCore.QRect(220, 170, 113, 18))
        self.subjectNo.setObjectName(_fromUtf8("subjectNo"))
        self.Day = QtGui.QLabel(self.centralwidget)
        self.Day.setGeometry(QtCore.QRect(220, 235, 73, 18))
        self.Day.setObjectName(_fromUtf8("Day"))
        self.record = QtGui.QPushButton(self.centralwidget)
        self.record.setGeometry(QtCore.QRect(220, 510, 181, 41))
        self.record.setObjectName(_fromUtf8("record"))
        self.quit = QtGui.QPushButton(self.centralwidget)
        self.quit.setGeometry(QtCore.QRect(700, 510, 101, 41))
        self.quit.setObjectName(_fromUtf8("quit"))
        self.clear = QtGui.QPushButton(self.centralwidget)
        self.clear.setGeometry(QtCore.QRect(460, 510, 131, 41))
        self.clear.setObjectName(_fromUtf8("clear"))
        self.block = QtGui.QLabel(self.centralwidget)
        self.block.setGeometry(QtCore.QRect(220, 300, 85, 18))
        self.block.setObjectName(_fromUtf8("block"))
        self.horizontal = QtGui.QLabel(self.centralwidget)
        self.horizontal.setGeometry(QtCore.QRect(220, 430, 91, 21))
        self.horizontal.setObjectName(_fromUtf8("horizontal"))
        self.resolution = QtGui.QLabel(self.centralwidget)
        self.resolution.setGeometry(QtCore.QRect(220, 380, 181, 21))
        self.resolution.setObjectName(_fromUtf8("resolution"))
        self.vertical = QtGui.QLabel(self.centralwidget)
        self.vertical.setGeometry(QtCore.QRect(590, 430, 101, 21))
        self.vertical.setObjectName(_fromUtf8("vertical"))
        self.patient_text = QtGui.QLineEdit(self.centralwidget)
        self.patient_text.setGeometry(QtCore.QRect(450, 160, 171, 31))
        self.patient_text.setObjectName(_fromUtf8("patient_text"))
        self.combo_day = QtGui.QComboBox(self.centralwidget)
        self.combo_day.setGeometry(QtCore.QRect(450, 221, 141, 31))
        self.combo_day.setObjectName(_fromUtf8("combo_day"))
        self.combo_day.addItem(_fromUtf8(""))
        self.combo_day.addItem(_fromUtf8(""))
        self.combo_day.addItem(_fromUtf8(""))
        self.combo_day.addItem(_fromUtf8(""))
        self.combo_day.addItem(_fromUtf8(""))
        self.combo_day.addItem(_fromUtf8(""))
        self.combo_day.addItem(_fromUtf8(""))
        self.combo_day.addItem(_fromUtf8(""))
        self.combo_block = QtGui.QComboBox(self.centralwidget)
        self.combo_block.setGeometry(QtCore.QRect(450, 290, 51, 31))
        self.combo_block.setObjectName(_fromUtf8("combo_block"))
        self.combo_block.addItem(_fromUtf8(""))
        self.combo_block.addItem(_fromUtf8(""))
        self.combo_block.addItem(_fromUtf8(""))
        self.combo_block.addItem(_fromUtf8(""))
        self.combo_block.addItem(_fromUtf8(""))
        self.Horiz_text = QtGui.QLineEdit(self.centralwidget)
        self.Horiz_text.setGeometry(QtCore.QRect(340, 420, 151, 31))
        self.Horiz_text.setObjectName(_fromUtf8("Horiz_text"))
        self.Vert_text = QtGui.QLineEdit(self.centralwidget)
        self.Vert_text.setGeometry(QtCore.QRect(690, 419, 141, 31))
        self.Vert_text.setObjectName(_fromUtf8("Vert_text"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1033, 24))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.subjectNo.setText(_translate("MainWindow", "Subject Number", None))
        self.Day.setText(_translate("MainWindow", "Select Day", None))
        self.record.setText(_translate("MainWindow", "Record Tracking Data", None))
        self.quit.setText(_translate("MainWindow", "Quit", None))
        self.clear.setText(_translate("MainWindow", "Clear", None))
        self.block.setText(_translate("MainWindow", "Select Block", None))
        self.horizontal.setText(_translate("MainWindow", "Horizontal", None))
        self.resolution.setText(_translate("MainWindow", "Enter Screen Resolution", None))
        self.vertical.setText(_translate("MainWindow", "Vertical", None))
        self.combo_day.setItemText(0, _translate("MainWindow", "Day 1", None))
        self.combo_day.setItemText(1, _translate("MainWindow", "Day 2", None))
        self.combo_day.setItemText(2, _translate("MainWindow", "Day 3", None))
        self.combo_day.setItemText(3, _translate("MainWindow", "Day 4", None))
        self.combo_day.setItemText(4, _translate("MainWindow", "Day5", None))
        self.combo_day.setItemText(5, _translate("MainWindow", "Baseline", None))
        self.combo_day.setItemText(6, _translate("MainWindow", "Performance", None))
        self.combo_day.setItemText(7, _translate("MainWindow", "Familiarisation", None))
        self.combo_block.setItemText(0, _translate("MainWindow", "1", None))
        self.combo_block.setItemText(1, _translate("MainWindow", "2", None))
        self.combo_block.setItemText(2, _translate("MainWindow", "3", None))
        self.combo_block.setItemText(3, _translate("MainWindow", "4", None))
        self.combo_block.setItemText(4, _translate("MainWindow", "5", None))

