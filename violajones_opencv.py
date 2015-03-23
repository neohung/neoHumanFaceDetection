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
work_folder_path = __file__
pos = __file__.rfind('/')
if pos != -1:
    work_folder_path = work_folder_path[:pos+1]
else:
    work_folder_path = ''

import numpy
import cv2 as cv
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger( __name__ )
#logger.debug(....)

class ViolaJonesRoi(object):
    def __init__(self, i_method, i_xml):
        #haarcascade_frontalface_default.xml, haarcascade_frontalface_alt.xml
        self.g_cascade_name = work_folder_path + i_xml
        self.g_parameters = {
            'robust': { 
            'min_size': (30,30), 
            'window_scale': 1.1,
            'min_neighbors': 3,
            'haar_flags': 0,
            },
            'webcam': { 
            'min_size': (30,30),
            'window_scale':1.2,
            'min_neighbors': 2,
            'haar_flags': cv.cv.CV_HAAR_DO_CANNY_PRUNING,
            },
            #CV_HAAR_DO_CANNY_PRUNING
            #CV_HAAR_SCALE_IMAGE
            #CV_HAAR_FIND_BIGGEST_OBJECT
        }
        self.faceCascade = cv.CascadeClassifier(self.g_cascade_name)
        self.i_param = self.g_parameters[i_method]
    def detectROI(self, cvgrayimage):
        faceRects = self.faceCascade.detectMultiScale(cvgrayimage,scaleFactor=self.i_param['window_scale'],minNeighbors=self.i_param['min_neighbors'], minSize=self.i_param['min_size'],flags=self.i_param['haar_flags'])
        if not (faceRects == None):
            max_size = 0
            best_face = None
            for (fx, fy, fw, fh) in faceRects:
                #logger.debug("Found ("+ str(fx) + "," + str(fy) + "," + str(fx) + "," + str(fx+fw) + "," + str(fy+fh)+ ")" )
                s = numpy.sqrt( (float(fh))**2 + (float(fw))**2)
                if s >= max_size:
                    max_size = s
                    best_face = (fy, fx , fy + fh , fx + fw)
            return best_face
        return None

if __name__ == "__main__":
    from PyQt4 import QtCore, QtGui
    from sys import stdin, exit, argv
    import numpy
    import QImageUtils
    import struct

    app = QtGui.QApplication(argv)
    display =  QImageUtils.ImageDisplay()
    display.setWindowTitle(u"Tracking展示") 
    vj = ViolaJonesRoi("webcam","haarcascade_frontalface_default.xml")
    qimg = QtGui.QImage()
    qimg.load("lena.png")
    cvimage = QImageUtils.QImage2Ipl(qimg)
    gray = cv.cvtColor(cvimage, cv.COLOR_BGR2GRAY)
    roi = vj.detectROI(gray)
    display.setImage(qimg) 
    display.drawRectangleRaw(0,roi)
    display.show()    
    retVal = app.exec_()    
    exit(retVal)
