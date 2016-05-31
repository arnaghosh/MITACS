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

class Ui_DataCollection(object):
    def setupUi(self, DataCollection):
        DataCollection.setObjectName(_fromUtf8("DataCollection"))
        DataCollection.resize(668, 566)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Leelawadee"))
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        DataCollection.setFont(font)
        self.centralwidget = QtGui.QWidget(DataCollection)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.logo1 = QtGui.QLabel(self.centralwidget)
        self.logo1.setGeometry(QtCore.QRect(20, 10, 141, 101))
        self.logo1.setText(_fromUtf8(""))
        self.logo1.setPixmap(QtGui.QPixmap(_fromUtf8("13552-REPAR-COUL.png")))
        self.logo1.setObjectName(_fromUtf8("logo1"))
        self.logo2 = QtGui.QLabel(self.centralwidget)
        self.logo2.setGeometry(QtCore.QRect(420, 31, 271, 61))
        self.logo2.setText(_fromUtf8(""))
        self.logo2.setPixmap(QtGui.QPixmap(_fromUtf8("medicine_logo_horiz_eng_outlined_750.png")))
        self.logo2.setObjectName(_fromUtf8("logo2"))
        self.subjectNo = QtGui.QLabel(self.centralwidget)
        self.subjectNo.setGeometry(QtCore.QRect(20, 161, 113, 18))
        self.subjectNo.setObjectName(_fromUtf8("subjectNo"))
        self.Day = QtGui.QLabel(self.centralwidget)
        self.Day.setGeometry(QtCore.QRect(20, 226, 73, 18))
        self.Day.setObjectName(_fromUtf8("Day"))
        self.record = QtGui.QPushButton(self.centralwidget)
        self.record.setGeometry(QtCore.QRect(20, 501, 181, 41))
        self.record.setObjectName(_fromUtf8("record"))
        self.quit = QtGui.QPushButton(self.centralwidget)
        self.quit.setGeometry(QtCore.QRect(540, 500, 101, 41))
        self.quit.setObjectName(_fromUtf8("quit"))
        self.clear = QtGui.QPushButton(self.centralwidget)
        self.clear.setGeometry(QtCore.QRect(260, 501, 131, 41))
        self.clear.setObjectName(_fromUtf8("clear"))
        self.block = QtGui.QLabel(self.centralwidget)
        self.block.setGeometry(QtCore.QRect(20, 291, 85, 18))
        self.block.setObjectName(_fromUtf8("block"))
        self.horizontal = QtGui.QLabel(self.centralwidget)
        self.horizontal.setGeometry(QtCore.QRect(20, 421, 91, 21))
        self.horizontal.setObjectName(_fromUtf8("horizontal"))
        self.resolution = QtGui.QLabel(self.centralwidget)
        self.resolution.setGeometry(QtCore.QRect(20, 371, 181, 21))
        self.resolution.setObjectName(_fromUtf8("resolution"))
        self.vertical = QtGui.QLabel(self.centralwidget)
        self.vertical.setGeometry(QtCore.QRect(390, 421, 101, 21))
        self.vertical.setObjectName(_fromUtf8("vertical"))
        self.patient_text = QtGui.QLineEdit(self.centralwidget)
        self.patient_text.setGeometry(QtCore.QRect(250, 151, 171, 31))
        self.patient_text.setObjectName(_fromUtf8("patient_text"))
        self.combo_day = QtGui.QComboBox(self.centralwidget)
        self.combo_day.setGeometry(QtCore.QRect(250, 212, 141, 31))
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
        self.combo_block.setGeometry(QtCore.QRect(250, 281, 51, 31))
        self.combo_block.setObjectName(_fromUtf8("combo_block"))
        self.combo_block.addItem(_fromUtf8(""))
        self.combo_block.addItem(_fromUtf8(""))
        self.combo_block.addItem(_fromUtf8(""))
        self.combo_block.addItem(_fromUtf8(""))
        self.combo_block.addItem(_fromUtf8(""))
        self.Horiz_text = QtGui.QLineEdit(self.centralwidget)
        self.Horiz_text.setGeometry(QtCore.QRect(140, 411, 151, 31))
        self.Horiz_text.setObjectName(_fromUtf8("Horiz_text"))
        self.Vert_text = QtGui.QLineEdit(self.centralwidget)
        self.Vert_text.setGeometry(QtCore.QRect(490, 410, 141, 31))
        self.Vert_text.setObjectName(_fromUtf8("Vert_text"))
        DataCollection.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(DataCollection)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 668, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        DataCollection.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(DataCollection)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        DataCollection.setStatusBar(self.statusbar)

        self.retranslateUi(DataCollection)
        QtCore.QMetaObject.connectSlotsByName(DataCollection)

    def retranslateUi(self, DataCollection):
        DataCollection.setWindowTitle(_translate("DataCollection", "Data Collection", None))
        self.subjectNo.setText(_translate("DataCollection", "Subject Number", None))
        self.Day.setText(_translate("DataCollection", "Select Day", None))
        self.record.setText(_translate("DataCollection", "Record Tracking Data", None))
        self.quit.setText(_translate("DataCollection", "Quit", None))
        self.clear.setText(_translate("DataCollection", "Clear", None))
        self.block.setText(_translate("DataCollection", "Select Block", None))
        self.horizontal.setText(_translate("DataCollection", "Horizontal", None))
        self.resolution.setText(_translate("DataCollection", "Enter Screen Resolution", None))
        self.vertical.setText(_translate("DataCollection", "Vertical", None))
        self.combo_day.setItemText(0, _translate("DataCollection", "Familiarisation", None))
        self.combo_day.setItemText(1, _translate("DataCollection", "Baseline", None))
        self.combo_day.setItemText(2, _translate("DataCollection", "Day 1", None))
        self.combo_day.setItemText(3, _translate("DataCollection", "Day 2", None))
        self.combo_day.setItemText(4, _translate("DataCollection", "Day 3", None))
        self.combo_day.setItemText(5, _translate("DataCollection", "Day 4", None))
        self.combo_day.setItemText(6, _translate("DataCollection", "Day 5", None))
        self.combo_day.setItemText(7, _translate("DataCollection", "Performance", None))
        self.combo_block.setItemText(0, _translate("DataCollection", "1", None))
        self.combo_block.setItemText(1, _translate("DataCollection", "2", None))
        self.combo_block.setItemText(2, _translate("DataCollection", "3", None))
        self.combo_block.setItemText(3, _translate("DataCollection", "4", None))
        self.combo_block.setItemText(4, _translate("DataCollection", "5", None))

