import numpy
import cv2 as cv
import os
from PyQt4 import QtCore, QtGui
import time
from sys import stdin, exit, argv

class neoHumanFaceWindow(QtGui.QWidget):
    def __init__(self):
        super(neoHumanFaceWindow, self).__init__()
        self.initUI()
    def initUI(self):
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('neoHumanFace Window')
	self.createButton()
	self.createLabel()
	self.createSlider()
        self.show()
    def createButton(self):
	qbtn = QtGui.QPushButton('Quit', self)
        qbtn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(150, 100)
    def createSlider(self):
	slider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        slider.setFocusPolicy(QtCore.Qt.NoFocus)
        slider.setGeometry(30, 40, 100, 30)
        slider.valueChanged.connect(self.changeValue)
    def createLabel(self):
	self.label = QtGui.QLabel(self)
        self.label.setText('0')
        self.label.setGeometry(160, 40, 80, 30)
    def changeValue(self, value):
        self.label.setText(str(value))
	
if __name__ == "__main__":
	app = QtGui.QApplication(argv)
        pWin = neoHumanFaceWindow()
	retVal = app.exec_()
	exit(retVal)
