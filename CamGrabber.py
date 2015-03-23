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
import cv2 as cv
import logging
import time

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger( __name__ )
#logger.debug(....)

class CamFrame(object):
    def release(self):
        self.camera.release()
    def open(self,id):
        self.camera.open(id) 
    def __init__(self):
        self.startTime = self.lastTime = time.time() 
        self.camera = cv.VideoCapture()
        self.fps = 0
        self.frame_cnt = 0
        self.nextCamFrame()
    def nextCamFrame(self):
        ret, self.currentFrame = self.camera.read()
        self.currentFrame = cv.flip(self.currentFrame, 1)
        self.frame_cnt += 1
        currectTime = time.time() 
        diffTime = currectTime - self.lastTime
        if diffTime > 1:
            self.fps = self.frame_cnt
            self.frame_cnt = 0
            self.lastTime = currectTime
        else:
            self.frame_cnt += 1
        return self.currentFrame
    def frameRate(self):
        return self.fps

    def getCvCamFrame(self):
        return self.currentFrame
    def getCvCamGrayFrame(self):
        width = self.currentFrame.shape[1]
        height = self.currentFrame.shape[0]
        cv2ImageGray = cv.cvtColor(self.currentFrame, cv.COLOR_BGR2GRAY)
        return cv2ImageGray


if __name__ ==  "__main__":
    from PyQt4 import QtCore, QtGui
    from sys import stdin, exit, argv
    import numpy
    import QImageUtils
    import struct
    import ctypes

    timer = QtCore.QTimer()
    app = QtGui.QApplication(argv)
    display =  QImageUtils.ImageDisplay()
    display.setWindowTitle(u"Camera展示") 
    display.c = CamFrame()
    display.c.open(-1)
    firstcvimg = display.c.nextCamFrame()
    firstqimg_gray = QImageUtils.Ipl2QImage(firstcvimg)
    height, width = firstcvimg.shape[:2]
    def updateDisplay():
        cvimg = display.c.nextCamFrame()
        cv2ImageGray = cv.cvtColor(cvimg, cv.COLOR_BGR2GRAY)
        cvimg = cv.equalizeHist(cv2ImageGray)
        cv.putText(cvimg, "fps: %s" % (str(display.c.fps)), (10, 35), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
        if not (cvimg == None):
            qimg = QImageUtils.IplGray2GrayQImage(cvimg)
            #qimg_gray = QImageUtils.IplBGR2GrayQImage(cvimg)
            display.setImage(qimg)    
    display.setImage(QImageUtils.Ipl2QImage(cv.imread("lena.png")))    
    display.show()  
    QtCore.QObject.connect(timer, QtCore.SIGNAL("timeout()"), updateDisplay )
    timer.start(0)
    retVal = app.exec_()
    exit(retVal)



