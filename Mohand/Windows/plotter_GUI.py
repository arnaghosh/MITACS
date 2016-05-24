# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'plotter.ui'
#
# Created: Thu May 19 17:51:51 2016
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
        MainWindow.resize(843, 639)
        font = QtGui.QFont()
        font.setPointSize(10)
        MainWindow.setFont(font)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.label_subNo = QtGui.QLabel(self.centralwidget)
        self.label_subNo.setGeometry(QtCore.QRect(160, 20, 101, 16))
        self.label_subNo.setObjectName(_fromUtf8("label_subNo"))
        self.text_subNo = QtGui.QLineEdit(self.centralwidget)
        self.text_subNo.setGeometry(QtCore.QRect(260, 20, 113, 20))
        self.text_subNo.setObjectName(_fromUtf8("text_subNo"))
        self.label_filter = QtGui.QLabel(self.centralwidget)
        self.label_filter.setGeometry(QtCore.QRect(390, 20, 81, 16))
        self.label_filter.setObjectName(_fromUtf8("label_filter"))
        self.combo_filter = QtGui.QComboBox(self.centralwidget)
        self.combo_filter.setGeometry(QtCore.QRect(490, 20, 69, 22))
        self.combo_filter.setObjectName(_fromUtf8("combo_filter"))
        self.combo_filter.addItem(_fromUtf8(""))
        self.combo_filter.addItem(_fromUtf8(""))
        self.label_param = QtGui.QLabel(self.centralwidget)
        self.label_param.setGeometry(QtCore.QRect(210, 50, 81, 21))
        self.label_param.setObjectName(_fromUtf8("label_param"))
        self.combo_param = QtGui.QComboBox(self.centralwidget)
        self.combo_param.setGeometry(QtCore.QRect(310, 50, 221, 22))
        self.combo_param.setObjectName(_fromUtf8("combo_param"))
        self.combo_param.addItem(_fromUtf8(""))
        self.combo_param.addItem(_fromUtf8(""))
        self.combo_param.addItem(_fromUtf8(""))
        self.combo_param.addItem(_fromUtf8(""))
        self.combo_param.addItem(_fromUtf8(""))
        self.combo_param.addItem(_fromUtf8(""))
        self.combo_param.addItem(_fromUtf8(""))
        self.combo_param.addItem(_fromUtf8(""))
        self.combo_param.addItem(_fromUtf8(""))
        self.combo_param.addItem(_fromUtf8(""))
        self.combo_param.addItem(_fromUtf8(""))
        self.combo_param.addItem(_fromUtf8(""))
        self.combo_param.addItem(_fromUtf8(""))
        self.combo_param.addItem(_fromUtf8(""))
        self.combo_param.addItem(_fromUtf8(""))
        self.widget = QtGui.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(10, 80, 831, 471))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.mplvl = QtGui.QVBoxLayout(self.widget)
        self.mplvl.setMargin(0)
        self.mplvl.setObjectName(_fromUtf8("mplvl"))
        self.PlotButton = QtGui.QPushButton(self.centralwidget)
        self.PlotButton.setGeometry(QtCore.QRect(170, 560, 75, 23))
        self.PlotButton.setObjectName(_fromUtf8("PlotButton"))
        self.ClearButton = QtGui.QPushButton(self.centralwidget)
        self.ClearButton.setGeometry(QtCore.QRect(320, 560, 75, 23))
        self.ClearButton.setObjectName(_fromUtf8("ClearButton"))
        self.QuitButton = QtGui.QPushButton(self.centralwidget)
        self.QuitButton.setGeometry(QtCore.QRect(650, 560, 75, 23))
        self.QuitButton.setObjectName(_fromUtf8("QuitButton"))
        self.logo1 = QtGui.QLabel(self.centralwidget)
        self.logo1.setGeometry(QtCore.QRect(20, 0, 141, 71))
        self.logo1.setText(_fromUtf8(""))
        self.logo1.setPixmap(QtGui.QPixmap(_fromUtf8("13552-REPAR-COUL.png")))
        self.logo1.setObjectName(_fromUtf8("logo1"))
        self.logo2 = QtGui.QLabel(self.centralwidget)
        self.logo2.setGeometry(QtCore.QRect(590, 10, 231, 51))
        self.logo2.setText(_fromUtf8(""))
        self.logo2.setPixmap(QtGui.QPixmap(_fromUtf8("medicine_logo_horiz_eng_outlined_750.png")))
        self.logo2.setObjectName(_fromUtf8("logo2"))
        self.SaveButton = QtGui.QPushButton(self.centralwidget)
        self.SaveButton.setGeometry(QtCore.QRect(480, 560, 75, 23))
        self.SaveButton.setObjectName(_fromUtf8("SaveButton"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 843, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Plot Generator", None))
        self.label_subNo.setText(_translate("MainWindow", "Subject Number", None))
        self.text_subNo.setText(_translate("MainWindow", "3", None))
        self.label_filter.setText(_translate("MainWindow", "Filtered Data", None))
        self.combo_filter.setItemText(0, _translate("MainWindow", "Yes", None))
        self.combo_filter.setItemText(1, _translate("MainWindow", "No", None))
        self.label_param.setText(_translate("MainWindow", "Parameter", None))
        self.combo_param.setItemText(0, _translate("MainWindow", "Index Value", None))
        self.combo_param.setItemText(1, _translate("MainWindow", "mean Reaction Time", None))
        self.combo_param.setItemText(2, _translate("MainWindow", "mean Movement Time", None))
        self.combo_param.setItemText(3, _translate("MainWindow", "mean Response Time", None))
        self.combo_param.setItemText(4, _translate("MainWindow", "mean Max Velocity", None))
        self.combo_param.setItemText(5, _translate("MainWindow", "mean Max Acceleration", None))
        self.combo_param.setItemText(6, _translate("MainWindow", "mean End Point Deviation", None))
        self.combo_param.setItemText(7, _translate("MainWindow", "mean Real Distance", None))
        self.combo_param.setItemText(8, _translate("MainWindow", "mean Distance Travelled", None))
        self.combo_param.setItemText(9, _translate("MainWindow", "mean Percentage Deviation", None))
        self.combo_param.setItemText(10, _translate("MainWindow", "overall Max Reaction Time", None))
        self.combo_param.setItemText(11, _translate("MainWindow", "overall Max Movement Time", None))
        self.combo_param.setItemText(12, _translate("MainWindow", "overall Max End Point Deviation", None))
        self.combo_param.setItemText(13, _translate("MainWindow", "overall Max Speed", None))
        self.combo_param.setItemText(14, _translate("MainWindow", "overall Max Acceleration", None))
        self.PlotButton.setText(_translate("MainWindow", "Plot", None))
        self.ClearButton.setText(_translate("MainWindow", "Clear", None))
        self.QuitButton.setText(_translate("MainWindow", "Quit", None))
        self.SaveButton.setText(_translate("MainWindow", "Save Plot", None))

