from PyQt4 import  QtCore, QtGui
#import frame_recorder
import numpy

class ImageDisplay(QtGui.QWidget):
  def __init__(self,i_cols_number = 1 , i_rows_number=1,  parent = None ):
        QtGui.QWidget.__init__(self, parent)
	h_layout = QtGui.QHBoxLayout()
        self.__labels = []
        self.__text_labels = []
        self.__cols = i_cols_number
        self.__rows = i_rows_number
        for i in range(0, i_cols_number):
            vbox_layout = QtGui.QVBoxLayout()
            label_text = QtGui.QLabel()
            vbox_layout.addWidget(label_text)
            for  j in range(0, i_rows_number):
                label_img = QtGui.QLabel()#f=QtCore.Qt.WNoAutoErase)
                vbox_layout.addWidget(label_img)
                self.__labels.append(label_img)

        self.__text_labels.append(label_text)
        h_layout.addLayout(vbox_layout)
        self.setLayout(h_layout)
        self.resize( 320, 240 )

	self.thumb = QtGui.QImage()
	#self.thumb.load(QtCore.QString("group.jpg"))
	#painter.begin(self)
	#self.repaint()
	#painter.end()
##        paint.begin(self)

#  def paintEvent(self, event):
#	painter = QtGui.QPainter()
#	point = QtCore.QPoint(0, 0)
#	painter.begin(self)
#	painter.drawImage( point, self.thumb)
#	painter.end()
  
  def setImage(self, i_image, i_index_col=0, i_index_row = 0,  i_text=None, i_scale=1.):
        """Update the display with a new image"""
        if not i_text is None:
        	self.__text_labels[i_index_col].setText(i_text)
        idx = i_index_col*self.__rows + i_index_row
        w = i_image.width()*i_scale
        h = i_image.height()*i_scale
        self.setSize(w, h)
        self.__labels[idx].setPixmap(QtGui.QPixmap.fromImage(i_image).scaled(w,h))
  
  def drawImage(self, io_image, i_image, i_x=0., i_y=0.):
        #Draw i_image on io_image at position x,y of io_image
        painter = QtGui.QPainter( io_image )
        point = QtCore.QPoint(i_x, i_y)
        painter.drawImage( point, i_image)
        painter.end()
  def autoSize(self):
	w = self.thumb.width()
        h = self.thumb.height()
	self.resize(w,h)
        
class ImageDisplayAndRecord( ImageDisplay ):
  def __init__(self, i_file_name="out.avi",i_cols_number = 1 , i_rows_number=1,  parent = None):
  	ImageDisplay.__init__(self, i_cols_number, i_rows_number,  parent )
   

if __name__ ==  "__main__":
    import cv2 as cv
    from PyQt4 import QtCore, QtGui
    from sys import stdin, exit, argv
    app = QtGui.QApplication(argv)
    test = ImageDisplay()
    test.thumb.load(QtCore.QString("group.jpg"))

    cam = cv.VideoCapture()
    cam.open(-1)
    img=cam.read()
    test.image = QtGui.QImage()

    cv.imwrite("test3.jpg",img[1])
    test.thumb.load(QtCore.QString("test3.jpg"))
    test.piclabel = QtGui.QLabel('pic')
    if test.image.load("group.jpg"):  
            test.piclabel.setPixmap(QtGui.QPixmap.fromImage(test.image))  
        
    test.autoSize();
    im = highgui.cvQueryFrame(self.playcapture)
    im = opencv.adaptors.Ipl2PIL(im) 
    im = im.convert('RGB').tostring('jpeg', 'RGB')
    self.image.loadFromData(QByteArray(im))
    self.piclabel.setPixmap(QPixmap.fromImage(self.image))  
  

    test.show()
    retVal = app.exec_()
    exit(retVal)
