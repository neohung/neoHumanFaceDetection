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
import ReadHaarcascade
import QImageUtils
from CamGrabber import CamFrame
from violajones_opencv import ViolaJonesRoi
from decimal import Decimal

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
        self.showDetect = False
        self.cam_index = -1
        desktop = QtGui.QDesktopWidget()
        self.screen_size = QtCore.QRectF(desktop.screenGeometry(desktop.primaryScreen()))
            
        #self.__display =  qt_image_display.ImageDisplayAndRecord()    
        self.display =  QImageUtils.QImageDisplay(1,2)    
        self.createCamButton()    
        self.createFileButton()    
        self.createDetectButton()    
        self.createTrackingCheckBox()    
        self.createActivateCheckBox()    
        self.createScrollBar()    
        self.createScaleSelectDoubleSpinBox()    
        self.createDeviceComboBox()    
        self.createQuitButton()    
        #self.createButton()    
        self.createLabel()    
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
        self.__face_button.setText("Preview detect window")
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
            self.showDetect = True
        else:     
            self.showDetect = False

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
        self.__scrollbar_gain_x.setMinimum(0)
        self.__scrollbar_gain_y = QtGui.QScrollBar()
        #self.__scrollbar_gain_y.setGeometry(QtCore.QRect(0, 190, 291, 20))
        self.__scrollbar_gain_y.setMinimum(0)
        self.__scrollbar_gain_z = QtGui.QScrollBar()
        #self.__scrollbar_gain_z.setGeometry(QtCore.QRect(0, 190, 291, 20))
        self.__scrollbar_gain_z.setMinimum(0)
        
        slider_max = 100
        self.__scrollbar_gain_x.setMaximum(slider_max)
        #self.__scrollbar_gain_x.setProperty("value", QtCore.QVariant(slider_max/2))
        self.__scrollbar_gain_x.setProperty("value", QtCore.QVariant(0))
        self.__scrollbar_gain_x.setSliderPosition(0)
        self.__scrollbar_gain_x.setOrientation(QtCore.Qt.Horizontal)
        self.__scrollbar_gain_x.setObjectName("scrollbar_gain")
        self.__scrollbar_gain_y.setMaximum(slider_max)
        #self.__scrollbar_gain_y.setProperty("value", QtCore.QVariant(slider_max/2))
        self.__scrollbar_gain_y.setProperty("value", QtCore.QVariant(0))
        self.__scrollbar_gain_y.setSliderPosition(0)
        self.__scrollbar_gain_y.setOrientation(QtCore.Qt.Horizontal)
        self.__scrollbar_gain_y.setObjectName("scrollbar_gain")
        
        self.__scrollbar_gain_z.setProperty("value", QtCore.QVariant(0))
        self.__scrollbar_gain_z.setSliderPosition(0)
        self.__scrollbar_gain_z.setOrientation(QtCore.Qt.Horizontal)
        self.__scrollbar_gain_z.setObjectName("scrollbar_gain")
        self.__label_gain_x = QtGui.QLabel()
        self.__label_gain_x.setText(QtCore.QString("stage: "+ str(self.__scrollbar_gain_x.value())))
        self.__label_gain_y = QtGui.QLabel()
        self.__label_gain_y.setText(QtCore.QString("tree: "+ str(self.__scrollbar_gain_y.value())))
        self.__label_gain_z = QtGui.QLabel()
        self.__label_gain_z.setText(QtCore.QString("rect: "+ str(self.__scrollbar_gain_z.value())))
        QtCore.QObject.connect(self.__scrollbar_gain_x, QtCore.SIGNAL("valueChanged(int)"), self.changeScrollbarGainX )
        QtCore.QObject.connect(self.__scrollbar_gain_y, QtCore.SIGNAL("valueChanged(int)"), self.changeScrollbarGainY )
        QtCore.QObject.connect(self.__scrollbar_gain_z, QtCore.SIGNAL("valueChanged(int)"), self.changeScrollbarGainZ )

    def createScaleSelectDoubleSpinBox(self):
        self.__scale_label = QtGui.QLabel()
        self.__scale_label.setText(QtCore.QString("Image scale"))    
        self.__scale_select = QtGui.QDoubleSpinBox()
        self.__scale_select.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.__scale_select.setMaximum(1.0)
        self.__scale_select.setMinimum(0.1)
        self.__scale_select.setSingleStep(0.25)
        self.__scale_select.setProperty("value", QtCore.QVariant(0.5))
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
        self.label1_title = QtGui.QLabel(self)
        self.label1_title.setText("threshold:")
        self.label1 = QtGui.QLabel(self)
        self.label1.setText('0')
        self.label2_title = QtGui.QLabel(self)
        self.label2_title.setText("value:")
        self.label2 = QtGui.QLabel(self)
        self.label2.setText('0')
        #self.label.setGeometry(160, 40, 80, 30)
    def changeScrollbarGainX(self, value):
        self.__label_gain_x.setText(QtCore.QString("stage: "+ str(value)))
    def changeScrollbarGainY(self, value):
        self.__label_gain_y.setText(QtCore.QString("tree: "+ str(value)))
    def changeScrollbarGainZ(self, value):
        self.__label_gain_z.setText(QtCore.QString("rect: "+ str(value)))

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
        g_layout.addWidget(self.__scrollbar_gain_x,6,0)
        g_layout.addWidget(self.__label_gain_y,7,0)
        g_layout.addWidget(self.__scrollbar_gain_y,8,0)
        g_layout.addWidget(self.__label_gain_z,9,0)
        g_layout.addWidget(self.__scrollbar_gain_z,10,0)
        g_layout.addWidget(self.__scale_label,11,0)
        g_layout.addWidget(self.__scale_select,12,0)
        g_layout.addWidget(self.__device_label,13,0)
        g_layout.addWidget(self.__device,14,0)
        g_layout.addWidget(self.__quit_button,15,0)
        g_layout.addWidget(self.label1_title,16,0)
        g_layout.addWidget(self.label1,17,0)
        g_layout.addWidget(self.label2_title,18,0)
        g_layout.addWidget(self.label2,19,0)
        v_layout = QtGui.QVBoxLayout()
        v_layout.addWidget(self.display)
        spacer = QtGui.QSpacerItem(10, 100, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        v_layout.addItem(spacer)
        g_layout.addLayout(v_layout, 0, 1,25,1)
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
        scale = self.__scale_select.value()

        gain_x = int(self.__scrollbar_gain_x.value())
        gain_y = int(self.__scrollbar_gain_y.value())
        gain_z = int(self.__scrollbar_gain_z.value())
        cvimg = self.__frame_grabber_file.nextCamFrame()
        cv.putText(cvimg, "fps: %s" % (str(self.__frame_grabber_file.fps)), (10, 35), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))    
        if(self.__tracking_box.isChecked()):
            roi = self.tracker.detectROI(cvimg,scale)
            if not (roi == None):
                left_top_x = roi[1]
                left_top_y = roi[0]
                right_bot_x = roi[3]
                right_bot_y = roi[2]     
                cv.rectangle(cvimg, (left_top_x, left_top_y), (right_bot_x, right_bot_y), (0, 255, 0), 2)
        self.display.setImage(QImageUtils.Ipl2QImage(cvimg))
        if (self.showDetect):
            if not (roi == None):
                self.__scrollbar_gain_x.setMaximum(self.tracker.cascade.stageSize-1)
                self.__scrollbar_gain_y.setMaximum(self.tracker.cascade.stage[self.__scrollbar_gain_x.value()].treeSize-1)
                self.__scrollbar_gain_z.setMaximum(self.tracker.cascade.stage[self.__scrollbar_gain_x.value()].tree[self.__scrollbar_gain_y.value()].feature.rectSize-1)
                self.label1.setText(QtCore.QString(str(self.tracker.cascade.stage[self.__scrollbar_gain_x.value()].stage_threshold)))
                #self.label1.setText(QtCore.QString(str(self.tracker.cascade.stage[self.__scrollbar_gain_x.value()].tree[self.__scrollbar_gain_y.value()].threshold)))                
                #
                scale_roi_x = int(left_top_x * scale)
                scale_roi_y = int(left_top_y * scale)
                scale_roi_w = int((right_bot_x - left_top_x) * scale)
                scale_roi_h = int((right_bot_y-left_top_y) * scale)
                crop_roi = self.tracker.roiimage[scale_roi_y:(scale_roi_y+scale_roi_h), scale_roi_x:(scale_roi_x+scale_roi_w)].copy()
                crop_roi_resize = cv.resize(crop_roi, (100, 100), interpolation = cv.INTER_AREA).copy()
                #
                scale_w = 100 / self.tracker.cascade.width
                scale_h = 100 / self.tracker.cascade.height
                x1 = int(self.tracker.cascade.stage[gain_x].tree[gain_y].feature.rect[gain_z].x * scale_w)
                y1 = int(self.tracker.cascade.stage[gain_x].tree[gain_y].feature.rect[gain_z].y * scale_h)
                x2 = x1 + int(self.tracker.cascade.stage[gain_x].tree[gain_y].feature.rect[gain_z].w * scale_w)
                y2 = y1 + int(self.tracker.cascade.stage[gain_x].tree[gain_y].feature.rect[gain_z].h * scale_h)
                cv.rectangle(crop_roi_resize, (x1,y1), (x2,y2), (0, 255, 0), 1)
                #p = self.calImageRectThreshold(crop_roi_resize,self.tracker.cascade.stage[gain_x].tree[gain_y].feature.rect)
                #s1 = self.calImageSum(crop_roi_resize,(x1,y1),(x2,y2))

                self.display.setImage(QImageUtils.IplGray2GrayQImage(crop_roi_resize),0,1)   
            #self.display.setImage(QImageUtils.IplGray2GrayQImage(self.tracker.roiimage),0,1)
            s = self.calImageStageVal(crop_roi_resize, self.tracker.cascade.stage[gain_x])
            self.label2.setText(QtCore.QString(str(s)))
            #logger.debug(s)

    def calImageStageVal(self, cvimage, stage):
        sum_p = 0
        for tree in stage.tree:
            threshold = tree.threshold
            left_val = tree.left_val
            right_val = tree.right_val
            p = self.calImageRectThreshold(cvimage,tree.feature.rect)
            if (p > threshold):
                sum_p = sum_p + right_val
            else:
                sum_p = sum_p + left_val
        #logger.debug(str(sum_p))
        return sum_p
    def calImageRectThreshold(self,cvimage,rects):
        sum_p = 0
        for r in rects:
            s = self.calImageSum(cvimage,(r.x,r.y),(r.x+r.w,r.y+r.h))
            s = s * Decimal(r.weight)
            sum_p = sum_p + s
        return sum_p
    def calImageSum(self,cvimage,(x1,y1),(x2,y2)):
        sum_val=0
        count = 0
        if (x1 > x2):
            tmp = x2
            x2 = x1
            x1 = tmp
        if (y1 > y2):
            tmp = y2
            y2 = y1
            y1 = tmp
        for y in range(y1,y2):
            for x in range(x1,x2):
                count = count + 1
                sum_val = sum_val + cvimage[y, x]
        if (count == 0):
            return 0
        sum_val =  Decimal(sum_val) / Decimal((255*count))
        return sum_val

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            QtCore.QCoreApplication.instance().quit()  
        elif event.key() == QtCore.Qt.Key_Return:
            logger.debug("key event="+str(event.key()))            
        elif event.key() == 65:
            logger.debug("key event="+str(event.key()))


class  HeadTracker(object):
    def __init__(self, method,xmlfile):
        self.cascade = ReadHaarcascade.readXml(xmlfile)
        #self.__roi_detector = ViolaJonesRoi( i_scale= self.__params['viola_scale'])
        self.__roi_detector = ViolaJonesRoi(method,xmlfile)
        self.pre_roi = self.roi = (0,0,0,0)
    def detectROI(self, cvimage, i_img_resize_scale=1.0):
        gray = cv.cvtColor(cvimage, cv.COLOR_BGR2GRAY)
        new_width, new_height = int(round(gray.shape[1]*i_img_resize_scale)), int(round(gray.shape[0]*i_img_resize_scale))
        smallgray = cv.resize(gray, (new_width, new_height), interpolation = cv.INTER_AREA)
        equalize_smallgray = cv.equalizeHist(smallgray)
        self.roiimage = equalize_smallgray
        roi = self.__roi_detector.detectROI(equalize_smallgray)
        if not (roi == None):
            roi = (int(round(roi[0]/i_img_resize_scale)),int(round(roi[1]/i_img_resize_scale)),int(round(roi[2]/i_img_resize_scale)),int(round(roi[3]/i_img_resize_scale)))
            self.pre_roi = self.roi
            self.roi = roi
            return self.roi
            #left_top_x = roi[1]
            #left_top_y = roi[0]
            #right_bot_x = roi[3]
            #right_bot_y = roi[2] 
        else:    
            return self.pre_roi
 
        return self.__roi_detector.detectROI(equalize_smallgray)

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
