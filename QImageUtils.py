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
from PyQt4 import  QtCore, QtGui
import numpy
import cv2 as cv
from sys import stdin, exit, argv
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger( __name__ )
#logger.debug(....)

class QImageDisplay(QtGui.QWidget):
    """Display and update a QImage in a QLabel"""
    def __init__(self,i_cols_number = 1 , i_rows_number=1,  parent = None ):
        super(QImageDisplay, self).__init__()
        self.__labels = []
        self.__images = []
        for i in range(0, i_cols_number*i_rows_number):
            self.__images.append(0)
        self.__text_labels = []
        hbox = QtGui.QHBoxLayout()
        self.__cols = i_cols_number
        self.__rows = i_rows_number
        for i in range(0, i_cols_number):
            vbox = QtGui.QVBoxLayout() 
            label_text = QtGui.QLabel()
            vbox.addWidget(label_text)
            for  j in range(0, i_rows_number):
                label_img = QtGui.QLabel()#f=QtCore.Qt.WNoAutoErase)
                vbox.addWidget(label_img)
                self.__labels.append(label_img)
            self.__text_labels.append(label_text)
            hbox.addLayout(vbox)
        self.setLayout(hbox)
        self.resize( 320, 240 )

#        self.__images[0] = QtGui.QImage()
#        if self.__images[0].load("group.jpg"):  
#            self.__labels[0].setPixmap(QtGui.QPixmap.fromImage(self.__images[0]))  

    def setSize(self, i_width, i_height, i_index_col=0, i_index_row = 0):
        idx = i_index_col*self.__rows + i_index_row
        self.__labels[idx].resize(i_width, i_height)

    def setImage(self, i_image, i_index_col=0, i_index_row = 0, i_scale=1.):
        """Update the display with a new image"""
        idx = i_index_col*self.__rows + i_index_row
        w = i_image.width()*i_scale
        h = i_image.height()*i_scale
        new_image = i_image.scaled(w,h,QtCore.Qt.KeepAspectRatio)
        self.setSize(w,h,i_index_col,i_index_row)
        self.__images[idx] = new_image
        self.__labels[idx].setPixmap(QtGui.QPixmap.fromImage(new_image).scaled(w,h))
    def getLabels(self):
        return self.__labels
    def getImages(self):
        return self.__images
    def setText(self, col_index=0, i_text=None):
        if not( i_text == None):
            self.__text_labels[col_index].setText(i_text)
    def drawRectangleRaw( self, idx, i_min_row, i_min_col, i_max_row, i_max_col, i_pen_width=2,i_color=QtGui.QColor("red")):
        """Overlay a red rectangle on the input image"""
        rect = QtCore.QRect(i_min_col, i_min_row, i_max_col-i_min_col, i_max_row-i_min_row)
        painter = QtGui.QPainter( self.__images[idx] )
        pen = QtGui.QPen(i_color)
        pen.setWidth(i_pen_width)
        painter.setPen(pen)
        painter.drawRect(rect)  
        w = self.__images[idx].width()
        h = self.__images[idx].height()
        self.__labels[idx].setPixmap(QtGui.QPixmap.fromImage(self.__images[idx]).scaled(w,h))       
    def drawRectangle( self, idx, i_rect, i_pen_width=6, i_color=QtGui.QColor("red")):
        """Overlay a red rectangle on the input image"""
        painter = QtGui.QPainter( self.__images[idx] )
        pen = QtGui.QPen(i_color)
        pen.setWidth(i_pen_width)
        painter.setPen(pen)
        painter.drawRect(i_rect)  
        w = self.__images[idx].width()
        h = self.__images[idx].height()
        self.__labels[idx].setPixmap(QtGui.QPixmap.fromImage(self.__images[idx]).scaled(w,h))
    def drawImage(self, idx, i_image, i_x=0., i_y=0.):
        painter = QtGui.QPainter( self.__images[idx] )
        point = QtCore.QPoint(i_x, i_y)
        painter.drawImage( point, i_image)
        w = self.__images[idx].width()
        h = self.__images[idx].height()
        self.__labels[idx].setPixmap(QtGui.QPixmap.fromImage(self.__images[idx]).scaled(w,h))
    def drawLines(self, idx,   start_xy_line, end_xy_line, i_pen_width=0.25,color=QtGui.QColor("red") ):
        painter = QtGui.QPainter( self.__images[idx] )
        pen = QtGui.QPen(color)
        pen.setWidth(i_pen_width)
        painter.setPen(pen)
        lines = [QtCore.QLine ( start_xy_line[n,0], start_xy_line[n,1], end_xy_line[n,0],  end_xy_line[n,1] ) for n in range(0, len(start_xy_line)) ]
        painter.drawLines(lines)  
        w = self.__images[idx].width()
        h = self.__images[idx].height()
        self.__labels[idx].setPixmap(QtGui.QPixmap.fromImage(self.__images[idx]).scaled(w,h))
    def drawPoints(self, idx,   i_points, i_pen_width=5,color=QtGui.QColor("red") ):
        if len(i_points) > 0:
            painter = QtGui.QPainter( self.__images[idx] )
            pen = QtGui.QPen(color)
            pen.setWidth(i_pen_width)
            painter.setPen(pen)
            [painter.drawPoint(i_points[n,0],i_points[n,1]) for n in range(0, i_points.shape[0]) ]
            w = self.__images[idx].width()
            h = self.__images[idx].height()
            self.__labels[idx].setPixmap(QtGui.QPixmap.fromImage(self.__images[idx]).scaled(w,h))
    def drawEllipse(self, idx,  i_x, i_y, i_size, i_color=QtGui.QColor("red")):
        painter = QtGui.QPainter( self.__images[idx] )
        brush = QtGui.QBrush( i_color )
        painter.setBrush(brush)
        ellipse = QtCore.QRectF( i_x, i_y,  i_size, i_size )
        painter.drawEllipse(ellipse)
        w = self.__images[idx].width()
        h = self.__images[idx].height()
        self.__labels[idx].setPixmap(QtGui.QPixmap.fromImage(self.__images[idx]).scaled(w,h))
    def drawArrows( self, idx,  start_xy_line, end_xy_line, i_pen_width=2, arrow_size=10, color=QtGui.QColor("red") ):
        painter = QtGui.QPainter( self.__images[idx] )
        pen = QtGui.QPen(color)
        pen.setWidth(i_pen_width)
        painter.setPen(pen)
        #
        delta = start_xy_line - end_xy_line  
        sum = numpy.absolute(delta[:,0]) + numpy.absolute(delta[:,1]).flatten()
        (idx, ) = numpy.nonzero( sum > 1E-4 )
        
        if len(idx) < 1: 
            return 
        
        delta = delta[ idx, :]  
        s_line = start_xy_line[idx]
        e_line = end_xy_line[idx]
        tangent = numpy.arctan2( delta[:,1], delta[:,0])
        arrow_angle1 = tangent + numpy.pi / 6.
        arrow_angle2 = tangent - numpy.pi / 6.
        arrow_x1 = arrow_size * numpy.cos (arrow_angle1) + e_line[:,0]
        arrow_y1 = arrow_size * numpy.sin (arrow_angle1) + e_line[:,1]
        arrow_x2 = arrow_size * numpy.cos (arrow_angle2) + e_line[:,0]
        arrow_y2 = arrow_size * numpy.sin (arrow_angle2) + e_line[:,1]
        
        for n in range(0, len(idx)):
            #Draw the line (input)
            line_start_point = QtCore.QPointF(s_line[n,0], s_line[n,1])
            line_end_point   = QtCore.QPointF(e_line[n,0], e_line[n,1])
            painter.drawLine(line_start_point , line_end_point )  
            #Draw the first arrow side
            arrow_start_point = line_end_point
            arrow_end_point = QtCore.QPointF( arrow_x1[n], arrow_y1[n])
            painter.drawLine(arrow_start_point , arrow_end_point )  
            #Draw the second arrow side
            arrow_end_point = QtCore.QPointF( arrow_x2[n], arrow_y2[n])
            painter.drawLine(arrow_start_point , arrow_end_point )  
        # 
        w = self.__images[idx].width()
        h = self.__images[idx].height()
        self.__labels[idx].setPixmap(QtGui.QPixmap.fromImage(self.__images[idx]).scaled(w,h))

#    def keyPressEvent(self, event):
#        if event.key() == QtCore.Qt.Key_Escape:
#            QtCore.QCoreApplication.instance().quit()  
#        elif event.key() == QtCore.Qt.Key_Return:
#            logger.debug("key event="+str(event.key()))            
#        elif event.key() == 65:
#            logger.debug("key event="+str(event.key()))
#    def closeEvent(self, event):
#        """ Ignore Alt+F4 and [X] Botton Event""" 
#        logger.debug("can't close by [X] botton, plz use ESC")
#        event.ignore()  

class ImageDisplay( QImageDisplay ):
    """Same as image display, but with the ability to record while displaying"""
    def __init__(self, i_file_name="out.avi",i_cols_number = 1 , i_rows_number=1,  parent = None):
        QImageDisplay.__init__(self, i_cols_number, i_rows_number,  parent )

class Ipl2QImage(QtGui.QImage): 
    '''
    Converting BGR iplimage to BGR QImage
    '''     
    def __init__(self, iplimage): 
        width = iplimage.shape[1]
        height = iplimage.shape[0]
        #depth = iplimage.shape[2]
        #tmpImage = np.zeros((iplimage.shape[0],iplimage.shape[1],iplimage.shape[2]), np.uint8)
        cv2ImageRGB = cv.cvtColor(iplimage, cv.COLOR_BGR2RGB)
        imageArray = numpy.asarray(cv2ImageRGB[:, :])
        super(Ipl2QImage,self).__init__(imageArray.data, width, height, QtGui.QImage.Format_RGB888)
 
class IplBGR2GrayQImage(QtGui.QImage): 
    '''
    Converting BGR iplimage to Gray QImage
    '''     
    def __init__(self, iplimage): 
        width = iplimage.shape[1]
        height = iplimage.shape[0]
        cv2ImageGray = cv.cvtColor(iplimage, cv.COLOR_BGR2GRAY)
        imageArray = numpy.asarray(cv2ImageGray[:, :])
        super(IplBGR2GrayQImage,self).__init__(imageArray.data, width, height, QtGui.QImage.Format_Indexed8)

class IplGray2GrayQImage(QtGui.QImage): 
    '''
    Converting Gray iplimage to Gray QImage
    '''     
    def __init__(self, iplimage): 
        width = iplimage.shape[1]
        height = iplimage.shape[0]
        imageArray = numpy.asarray(iplimage[:, :])
        super(IplGray2GrayQImage,self).__init__(imageArray.data, width, height, QtGui.QImage.Format_Indexed8)
 

if __name__ == "__main__":
    import cv2 as cv
    app = QtGui.QApplication(argv)
    pWin = QImageDisplay(2,1)
    pWin.setWindowTitle(u"繪圖展示")
    #pWin.setWindowIcon(QtGui.QIcon('icon.png'))
    qimg = QtGui.QImage()
    qimg.load("group.jpg")
    qimg2 = Ipl2QImage(cv.imread("lena.png"))
    pWin.setImage(qimg,0,0)
    pWin.setText(0,"group.jpg")
    pWin.setImage(qimg2,1,0,0.5)
    pWin.setText(1,"lena.png")
    pics = pWin.getLabels()
    r = QtCore.QRect(200, 120, 50, 50)
    pWin.show()
    pWin.drawRectangle(0,r,1)
    pWin.drawRectangleRaw(1,100,100,200,200,1)
    pWin.drawImage(0,pWin.getImages()[1],250,200);
    start_point  = numpy.atleast_2d(numpy.array([10, 10]))
    end_point  = numpy.atleast_2d(numpy.array([200, 150]))  
    pWin.drawLines(1,start_point,end_point)
    points = numpy.atleast_2d(numpy.array([[10, 10],[20,20],[30,30]]))
    pWin.drawPoints(0,points)
    pWin.drawEllipse(1,50,200,15)
    start_point2  = numpy.atleast_2d(numpy.array([10, 200]))
    end_point2  = numpy.atleast_2d(numpy.array([200, 150]))  
    pWin.drawArrows(0,start_point2,end_point2)

    retVal = app.exec_()
    exit(retVal)
