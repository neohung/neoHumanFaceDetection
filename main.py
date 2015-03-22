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

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger( __name__ )

class neoHumanFaceWindow(QtGui.QWidget):
    def __init__(self, neo_head_tracker, parent=None):
        super(neoHumanFaceWindow, self).__init__()
        self.initUI()
    def initUI(self):
        self.setGeometry(300, 300, 640, 480)
        self.setWindowTitle('neoHumanFace Window')
        #self.__display =  qt_image_display.ImageDisplayAndRecord()    
        self.display =  QImageUtils.QImageDisplay()    
        self.createRecordButton()    
        self.createFileButton()    
        self.createDetectButton()    
        self.createTrackingCheckBox()    
        self.createActivateCheckBox()    
        self.createScrollBar()    
        self.createScaleSelectDoubleSpinBox()    
        self.createDeviceComboBox()    
        self.createQuitButton()    
        #self.createButton()    
        #self.createLabel()    
        #self.createSlider()    
        self.layout()    
        #self.__frame_grabber_file=  FrameGrabberFile("out.avi")    
        self.__frame_grabber_file=  CamFrame()    
        self.createTimer()
    def createRecordButton(self): 
        self.__record_button = QtGui.QPushButton(self)        
        self.__record_button.setCheckable(True)
        self.__record_button.setObjectName("recordButton")
        self.__record_button.setText("Record")
        self.connect( self.__record_button, QtCore.SIGNAL("clicked(bool)"),  self.recordSlot )
    def createFileButton(self): 
        self.__file_button = QtGui.QPushButton(self)    
        self.__file_button.setCheckable(True)
        self.__file_button.setObjectName("fileButton")
        self.__file_button.setText("Display .avi")
        self.connect( self.__file_button, QtCore.SIGNAL("clicked(bool)"),  self.fileSlot )
    def createDetectButton(self): 
        self.__face_button = QtGui.QPushButton(self)    
        self.__face_button.setCheckable(True)
        self.__face_button.setObjectName("detectButton")
        self.__face_button.setText("Detect faces")
    def recordSlot(self, checked):    
        if checked:    	
            #filename = QtGui.QFileDialog.getSaveFileName( self, "Select output file",os.getcwd(), "Avi Files(*.avi)")    	
            self.__record_button.setText("Recording...")  
            self.__frame_grabber_file.open(-1)
            self.__timer.start( 0 )  
        else:    	
            self.__record_button.setText("Record")
            self.__timer.stop()
            self.__frame_grabber_file.release()
    def fileSlot(self, checked):
        if checked:
            filename = QtGui.QFileDialog.getOpenFileName( self, "Select output file",os.getcwd(), "Avi Files (*.avi)")
            if len(filename) > 0:
                self.__file_button.setText("Stop display from .avi")
        else:
            self.__file_button.setText("Display .avi")

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
        self.__label_gain_x.setText(QtCore.QString("X gain"))
        self.__label_gain_y = QtGui.QLabel()
        self.__label_gain_y.setText(QtCore.QString("Y gain"))
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
        for n in range(0, 6):
            self.__device.addItem(QtCore.QString(str(n)), QtCore.QVariant(n))
        self.__device.setCurrentIndex(0)
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
    def changeValue(self, value):
        self.label.setText(str(value))    
        logger.debug("Set val="+str(value))
    def layout(self):    
        g_layout = QtGui.QGridLayout()    
        g_layout.addWidget(self.__face_button, 0, 0)
        g_layout.addWidget(self.__record_button,1,0)
        g_layout.addWidget(self.__file_button, 2, 0)
        g_layout.addWidget(self.__tracking_box,3,0)
        g_layout.addWidget(self.__active_box,4, 0)
        g_layout.addWidget(self.__label_gain_x,5,0)
        g_layout.addWidget(self.__scrollbar_gain_x),6,0
        g_layout.addWidget(self.__label_gain_y,7,0)
        g_layout.addWidget(self.__scrollbar_gain_y,8,0)
        g_layout.addWidget(self.__scale_label,9,0)
        g_layout.addWidget(self.__scale_select,10,0)
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
 	
    def update(self):    
        #logger.debug("time out")
        #pWin.display.setImage(QImageUtils.Ipl2QImage(self.__frame_grabber_file.getCvCamFrame()))
        cvimg = self.__frame_grabber_file.nextCamFrame()
        cv.putText(cvimg, "fps: %s" % (str(self.__frame_grabber_file.fps)), (10, 35), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))    
        pWin.display.setImage(QImageUtils.Ipl2QImage(cvimg))
        

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            QtCore.QCoreApplication.instance().quit()  
        elif event.key() == QtCore.Qt.Key_Return:
            logger.debug("key event="+str(event.key()))            
        elif event.key() == 65:
            logger.debug("key event="+str(event.key()))

if __name__ == "__main__":    
        app = QtGui.QApplication(argv)
        pWin = neoHumanFaceWindow("")
        qimg = QtGui.QImage()
        qimg.load("group.jpg")
        pWin.display.setImage(qimg)    
        pWin.show()    
        retVal = app.exec_()    
        exit(retVal)
