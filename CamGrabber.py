# coding=UTF-8
############################################################################
#    Copyright 2015 Neo Hung
#    This file is part of neoHumanFacedetection
#    This library is free software; you can redistribute it and/or
#    modify it under the terms of the GNU Lesser General Public
#    License as published by the Free Software Foundation; either
#    version 2.1 of the License, or (at your option) any later version.
#    This library is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    Lesser General Public License for more details.
#    <http://www.gnu.org/licenses/>
############################################################################
from PyQt4 import QtCore, QtGui
import cv2 as cv
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger( __name__ )
#logger.debug(....)

class CamFrame(object):
    def updateDisplay():
    	logger.debug("update")
    	ret, self.currentFrame = this.camera.read()
    	#gray = cv.cvtColor(currentFrame, cv.COLOR_BGR2GRAY)
    	#display.setImage(QImageUtils.Ipl2QImage(self.currentFrame)) 
    def release(self):
        self.camera.release()
    def open(self,id):
        self.camera.open(id) 
    def __init__(self):
    	#timer = QtCore.QTimer()
    	self.camera = cv.VideoCapture()
    	#QtCore.QObject.connect(timer, QtCore.SIGNAL("timeout()"), self.updateDisplay )
        #timer.start( 50 )

    def getCvCamFrame(self):
    	ret, self.currentFrame = self.camera.read()
    	return self.currentFrame


if __name__ ==  "__main__":
    from PyQt4 import QtCore, QtGui
    from sys import stdin, exit, argv
    import numpy
    import QImageUtils

    timer = QtCore.QTimer()
    app = QtGui.QApplication(argv)
    display =  QImageUtils.ImageDisplay() 
    display.c = CamFrame()
    display.c.open(-1)
    display.i=0
    def updateDisplay():
    	cvimg = display.c.getCvCamFrame()
    	if (cvimg != None):
    		qimg = QImageUtils.Ipl2QImage(cvimg)
    		w = qimg.width()
    		h = qimg.height()
    		for y in range(0,h):
    			for x in range(0,w):
    				gray= QtGui.qGray(qimg.pixel(x, y))
    				qimg.setPixel(x,y,QtGui.qRgb(gray,gray,gray))
     		display.setImage(qimg)	
    		display.i=display.i+1
    	if (display.i>100):
    		timer.stop()
    display.setImage(QImageUtils.Ipl2QImage(cv.imread("lena.png")))	
    display.show()  
    QtCore.QObject.connect(timer, QtCore.SIGNAL("timeout()"), updateDisplay )
    timer.start( 1 )
    retVal = app.exec_()
    exit(retVal)



