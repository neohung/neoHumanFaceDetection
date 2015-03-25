import numpy as np
#import Image
import cv2 as cv
import os
from PyQt4 import QtCore, QtGui
import time
from sys import stdin, exit , argv
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger( __name__ )
#logger.debug(....)


class Ipl2QImage(QtGui.QImage): 
    '''
    Converting iplimage to QImage
    '''     
    def __init__(self, iplimage): 
	width = iplimage.shape[1]
	height = iplimage.shape[0]
	#depth = iplimage.shape[2]
	#tmpImage = np.zeros((iplimage.shape[0],iplimage.shape[1],iplimage.shape[2]), np.uint8)
        cv2ImageRGB = cv.cvtColor(iplimage, cv.COLOR_BGR2RGB)
        imageArray = np.asarray(cv2ImageRGB[:, :])
        super(Ipl2QImage,self).__init__(imageArray.data, width, height, QtGui.QImage.Format_RGB888)

class Ipl2GrayQImage(QtGui.QImage):
    '''
    Converting iplimage to QImage
    '''
    def __init__(self, iplimage):
        width = iplimage.shape[1]
        height = iplimage.shape[0]
        #depth = iplimage.shape[2]
        print "["+str(width)+","+str(height)+"]"
        #tmpImage = np.zeros((iplimage.shape[0],iplimage.shape[1],iplimage.shape[2]), np.uint8)
        cv2ImageRGB = cv.cvtColor(iplimage, cv.COLOR_BGR2RGB)
        cv2ImageGRAY = cv.cvtColor(iplimage, cv.COLOR_RGB2GRAY)
        imageArray = np.asarray(cv2ImageGRAY[:, :])
        super(Ipl2QImage,self).__init__(imageArray.data, width, height, QtGui.QImage.Format_RGB888)


class neoHumanFaceWindow(QtGui .QWidget):
    def __init__(self ):
        super (neoHumanFaceWindow, self).__init__ ()
        self.initUI()
	self.showFirstImage()
    def initUI(self ):
        self .setGeometry(300, 300, 550, 550)
        self .setWindowTitle('neoHumanFace Window' )
	self.image = QtGui.QImage()
        
	self.capturebtn = QtGui.QPushButton('capture')
        self.playbtn = QtGui.QPushButton('SwitchPic')
        exitbtn = QtGui.QPushButton('exit')
	
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.capturebtn)
        vbox.addWidget(self.playbtn)
        vbox.addWidget(exitbtn)
        
        self.piclabel = QtGui.QLabel('pic')
        hbox = QtGui.QHBoxLayout()
        hbox.addLayout(vbox)
        hbox.addStretch(1)
        hbox.addWidget(self.piclabel)
        self.setLayout(hbox)

	self.connect( self.playbtn, QtCore.SIGNAL("clicked(bool)"),  self.SwitchPic )
	self.connect( self.capturebtn, QtCore.SIGNAL("clicked(bool)"),  self.capturePic )
        exitbtn.clicked.connect(QtCore.QCoreApplication.instance().quit)
    def showFirstImage(self ):
	if self.image.load("group.jpg"):  
        	self.piclabel.setPixmap(QtGui.QPixmap.fromImage(self.image))  
      
    def update(self):
	ret, self.currentFrame = self.camera.read()
	gray = cv.cvtColor(self.currentFrame, cv.COLOR_BGR2GRAY)

        faces = self.faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv.cv.CV_HAAR_SCALE_IMAGE
        )
	for (x, y, w, h) in faces:
       		 cv.rectangle(self.currentFrame, (x, y), (x+w, y+h), (0, 255, 0), 2)


        self.image = Ipl2QImage(self.currentFrame)
	self.piclabel.setPixmap(QtGui.QPixmap.fromImage(self.image))

    def capturePic(self):
	print "capture now"
	#self.faceCascade = cv.CascadeClassifier("haarcascade_frontalface_alt.xml")
	self.faceCascade = cv.CascadeClassifier("haarcascade_frontalface_alt.xml")
        self.camera = cv.VideoCapture()
        self.camera.open(-1)
	#ret, frame = self.camera.read()
 	#self.image = Ipl2QImage(frame)
 	#self.image = Ipl2GrayQImage(frame)
	#self.piclabel.setPixmap(QtGui.QPixmap.fromImage(self.image))
	self.__timer = QtCore.QTimer()
        QtCore.QObject.connect(self.__timer, QtCore.SIGNAL("timeout()"), self.update )
        self.__timer.start( 1 )
    def SwitchPic(self):
 	self.image = Ipl2QImage(cv.imread('lena.png'))
	self.piclabel.setPixmap(QtGui.QPixmap.fromImage(self.image))

if __name__ == "__main__":
    import ReadHaarcascade
    a = ReadHaarcascade.readXml("haarcascade_frontalface_alt.xml")
    print "x: "+ str(a.stage[1].tree[12].feature.rect[2].x)
    print "y: "+ str(a.stage[1].tree[12].feature.rect[2].y)
    print "w: "+ str(a.stage[1].tree[12].feature.rect[2].w)
    print "h: "+ str(a.stage[1].tree[12].feature.rect[2].h)
    print "weight: "+ str(a.stage[1].tree[12].feature.rect[2].weight) 
    app = QtGui.QApplication(argv )
    pWin = neoHumanFaceWindow()
    pWin.show()
    retVal = app. exec_()
    exit (retVal)
 

