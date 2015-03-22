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

import numpy
import cv2 as cv
import os
from PyQt4 import QtCore, QtGui
import time
from sys import stdin, exit, argv
import logging
#import qt_image_display
import QImageUtils
from CamGrabber import CamFrame
from violajones_opencv import ViolaJonesRoi


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger( __name__ )

class neoHumanFaceWindow(QtGui.QWidget):
    def __init__(self, neo_head_tracker, parent=None):
        super(neoHumanFaceWindow, self).__init__()
        self.tracker = neo_head_tracker
        self.initUI()
    def initUI(self):
        self.setGeometry(300, 300, 640, 480)
        self.setWindowTitle('neoHumanFace Window')
        self.detect_now = False
        self.cam_index = -1
        desktop = QtGui.QDesktopWidget()
        self.screen_size = QtCore.QRectF(desktop.screenGeometry(desktop.primaryScreen()))
            
        #self.__display =  qt_image_display.ImageDisplayAndRecord()    
        self.display =  QImageUtils.QImageDisplay()    
        self.createCamButton()    
        self.createFileButton()    
        self.createDetectButton()    
        self.createTrackingCheckBox()    
        self.createActivateCheckBox()    
        self.createScrollBar()    
        #self.createScaleSelectDoubleSpinBox()    
        self.createDeviceComboBox()    
        self.createQuitButton()    
        #self.createButton()    
        #self.createLabel()    
        #self.createSlider()    
        self.layout()    
        #self.__frame_grabber_file=  FrameGrabberFile("out.avi")    
        self.__frame_grabber_file=  CamFrame()    
        self.createTimer()
    def createCamButton(self): 
        self.__cam_button = QtGui.QPushButton(self)        
        self.__cam_button.setCheckable(True)
        self.__cam_button.setObjectName("camButton")
        self.__cam_button.setText("Camera")
        self.connect( self.__cam_button, QtCore.SIGNAL("clicked(bool)"),  self.camSlot )
    def createFileButton(self): 
        self.__file_button = QtGui.QPushButton(self)    
        self.__file_button.setCheckable(True)
        self.__file_button.setObjectName("fileButton")
        self.__file_button.setText("Display .avi [Not Done]")
        self.connect( self.__file_button, QtCore.SIGNAL("clicked(bool)"),  self.fileSlot )
    def createDetectButton(self): 
        self.__face_button = QtGui.QPushButton(self)    
        self.__face_button.setCheckable(True)
        self.__face_button.setObjectName("detectButton")
        self.__face_button.setText("Detect faces")
        self.connect( self.__face_button, QtCore.SIGNAL("clicked(bool)"),  self.detectSlot )
    def camSlot(self, checked):    
        if checked:    	
            #filename = QtGui.QFileDialog.getSaveFileName( self, "Select output file",os.getcwd(), "Avi Files(*.avi)")    	
            self.__cam_button.setText("Preview...")  
            self.__frame_grabber_file.open(self.cam_index)
            self.__timer.start()  
        else:    	
            self.__cam_button.setText("Camera")
            self.__timer.stop()
            self.__frame_grabber_file.release()
    def fileSlot(self, checked):
        if checked:
            filename = QtGui.QFileDialog.getOpenFileName( self, "Select output file",os.getcwd(), "Avi Files (*.avi)")
            if len(filename) > 0:
                self.__file_button.setText("Stop display from .avi")
        else:
            self.__file_button.setText("Display .avi")
    def detectSlot(self, checked):    
        if checked:
            self.detect_now = True
        else:     
            self.detect_now = False

    def createTrackingCheckBox(self):
        self.__tracking_box = QtGui.QCheckBox()
        self.__tracking_box.setChecked(True)
        self.__tracking_box.setObjectName("trackingBox")
        self.__tracking_box.setText("Enable tracking")
    def createActivateCheckBox(self):
        self.__active_box = QtGui.QCheckBox()
        self.__active_box.setChecked(False)
        self.__active_box.setObjectName("activeBox")
        self.__active_box.setText("Activate Cursor Control (ESC to exit)")
    def createScrollBar(self):    
        self.__scrollbar_gain_x = QtGui.QScrollBar()
        #self.__scrollbar_gain_x.setGeometry(QtCore.QRect(0, 190, 291, 20))
        self.__scrollbar_gain_x.setMinimum(1)
        self.__scrollbar_gain_y = QtGui.QScrollBar()
        #self.__scrollbar_gain_y.setGeometry(QtCore.QRect(0, 190, 291, 20))
        self.__scrollbar_gain_y.setMinimum(1)
        slider_max = 100
        self.__scrollbar_gain_x.setMaximum(slider_max)
        self.__scrollbar_gain_x.setProperty("value", QtCore.QVariant(slider_max/2))
        self.__scrollbar_gain_x.setSliderPosition(slider_max/2)
        self.__scrollbar_gain_x.setOrientation(QtCore.Qt.Horizontal)
        self.__scrollbar_gain_x.setObjectName("scrollbar_gain")
        self.__scrollbar_gain_y.setMaximum(slider_max)
        self.__scrollbar_gain_y.setProperty("value", QtCore.QVariant(slider_max/2))
        self.__scrollbar_gain_y.setSliderPosition(slider_max/2)
        self.__scrollbar_gain_y.setOrientation(QtCore.Qt.Horizontal)
        self.__scrollbar_gain_y.setObjectName("scrollbar_gain")
        self.__label_gain_x = QtGui.QLabel()
        self.__label_gain_x.setText(QtCore.QString("X gain: "+ str(self.__scrollbar_gain_x.value())))
        self.__label_gain_y = QtGui.QLabel()
        self.__label_gain_y.setText(QtCore.QString("Y gain: "+ str(self.__scrollbar_gain_y.value())))
        QtCore.QObject.connect(self.__scrollbar_gain_x, QtCore.SIGNAL("valueChanged(int)"), self.changeScrollbarGainX )
        QtCore.QObject.connect(self.__scrollbar_gain_y, QtCore.SIGNAL("valueChanged(int)"), self.changeScrollbarGainY )

    def createScaleSelectDoubleSpinBox(self):
        self.__scale_label = QtGui.QLabel()
        self.__scale_label.setText(QtCore.QString("Image scale"))    
        self.__scale_select = QtGui.QDoubleSpinBox()
        self.__scale_select.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.__scale_select.setMaximum(1.0)
        self.__scale_select.setMinimum(0.1)
        self.__scale_select.setSingleStep(0.25)
        self.__scale_select.setProperty("value", QtCore.QVariant(1.0))
    def createDeviceComboBox(self):
        self.__device_label = QtGui.QLabel()
        self.__device_label.setText(QtCore.QString("Device number"))
        self.__device = QtGui.QComboBox(self)
        self.__device.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.__device.setObjectName("device")
        for n in range(-1, 6):
            self.__device.addItem(QtCore.QString(str(n)), QtCore.QVariant(n))
        self.__device.setCurrentIndex(0)
        QtCore.QObject.connect(self.__device, QtCore.SIGNAL("currentIndexChanged(int)"), self.updateDevice )
    def createQuitButton(self):    
        self.__quit_button = QtGui.QPushButton('Quit', self)
        self.__quit_button.clicked.connect(QtCore.QCoreApplication.instance().quit)
        self.__quit_button.resize(self.__quit_button.sizeHint())
    def createSlider(self):    
        slider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        slider.setFocusPolicy(QtCore.Qt.NoFocus)
        #slider.setGeometry(30, 40, 100, 30)
        slider.valueChanged.connect(self.changeValue)
    def createLabel(self):    
        self.label = QtGui.QLabel(self)
        self.label.setText('0')
        #self.label.setGeometry(160, 40, 80, 30)
    def changeScrollbarGainX(self, value):
        self.__label_gain_x.setText(QtCore.QString("X gain: "+ str(value)))
        #self.__label_gain_y.setText(QtCore.QString("Y gain: "+ str(self.__scrollbar_gain_y.value())))
    def changeScrollbarGainY(self, value):
        self.__label_gain_y.setText(QtCore.QString("Y gain: "+ str(value)))

    def changeValue(self, value):
        self.label.setText(str(value))    
        logger.debug("Set val="+str(value))
    def layout(self):    
        g_layout = QtGui.QGridLayout()    
        g_layout.addWidget(self.__face_button, 0, 0)
        g_layout.addWidget(self.__cam_button,1,0)
        g_layout.addWidget(self.__file_button, 2, 0)
        g_layout.addWidget(self.__tracking_box,3,0)
        g_layout.addWidget(self.__active_box,4, 0)
        g_layout.addWidget(self.__label_gain_x,5,0)
        g_layout.addWidget(self.__scrollbar_gain_x),6,0
        g_layout.addWidget(self.__label_gain_y,7,0)
        g_layout.addWidget(self.__scrollbar_gain_y,8,0)
        #g_layout.addWidget(self.__scale_label,9,0)
        #g_layout.addWidget(self.__scale_select,10,0)
        g_layout.addWidget(self.__device_label,11,0)
        g_layout.addWidget(self.__device,12,0)
        g_layout.addWidget(self.__quit_button,13,0)
        v_layout = QtGui.QVBoxLayout()
        v_layout.addWidget(self.display)
        spacer = QtGui.QSpacerItem(10, 100, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        v_layout.addItem(spacer)
        g_layout.addLayout(v_layout, 0, 1,12,1)
        self.setLayout(g_layout)    
        desktop = QtGui.QDesktopWidget()
        screen_size = QtCore.QRectF(desktop.screenGeometry(desktop.primaryScreen()))
        x = screen_size.x() + screen_size.width()
        y = screen_size.y() + screen_size.height()
        self.__current_pos = [x/2., y/2.]

    def createTimer(self):
        self.__timer = QtCore.QTimer()
        QtCore.QObject.connect(self.__timer, QtCore.SIGNAL("timeout()"), self.update )
        #self.__timer.start( 20 )

    def updateDevice(self,i_index):
        #self.__record_button.setDefault(False)
        self.recordSlot(False)
        self.__timer.stop()
        (self.cam_index, is_data) = self.__device.itemData(i_index).toInt()
        self.__frame_grabber_file.release()
        logger.debug(self.cam_index)

    def update(self):
        gain_x = float(self.__scrollbar_gain_x.value())
        gain_y = float(self.__scrollbar_gain_y.value())
        cvimg = self.__frame_grabber_file.nextCamFrame()
        cv.putText(cvimg, "fps: %s" % (str(self.__frame_grabber_file.fps)), (10, 35), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))    
        if(self.detect_now):
            roi = self.tracker.detectROI(cvimg)
            if not (roi == None):
                left_top_x = roi[1]
                left_top_y = roi[0]
                right_bot_x = roi[3]
                right_bot_y = roi[2]     
                cv.rectangle(cvimg, (left_top_x, left_top_y), (right_bot_x, right_bot_y), (0, 255, 0), 2)
        self.display.setImage(QImageUtils.Ipl2QImage(cvimg))

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            QtCore.QCoreApplication.instance().quit()  
        elif event.key() == QtCore.Qt.Key_Return:
            logger.debug("key event="+str(event.key()))            
        elif event.key() == 65:
            logger.debug("key event="+str(event.key()))


class  HeadTracker(object):
    def __init__(self, method,xmlfile,i_viola_scale=0.5, i_img_resize_scale=1.0):
        #self.__roi_detector = ViolaJonesRoi( i_scale= self.__params['viola_scale'])
        self.__roi_detector = ViolaJonesRoi(method,xmlfile)
        self.pre_roi = self.roi = (0,0,0,0)
    def detectROI(self, cvimage, i_roi_scale_factor=1.2, i_track=True):
        roi = self.__roi_detector.detectROI(cvimage)
        if not (roi == None):
            self.pre_roi = self.roi
            self.roi = roi
            return self.roi
            #left_top_x = roi[1]
            #left_top_y = roi[0]
            #right_bot_x = roi[3]
            #right_bot_y = roi[2] 
        else:    
            return self.pre_roi
 
        return self.__roi_detector.detectROI(cvimage)

if __name__ == "__main__":    
        app = QtGui.QApplication(argv)
        #haarcascade_frontalface_alt.xml, haarcascade_frontalface_default.xml
        h = HeadTracker("webcam","haarcascade_frontalface_alt.xml")
        pWin = neoHumanFaceWindow(neo_head_tracker=h)
        qimg = QtGui.QImage()
        qimg.load("group.jpg")
        pWin.display.setImage(qimg)
        pWin.show()    
        retVal = app.exec_()    
        exit(retVal)
