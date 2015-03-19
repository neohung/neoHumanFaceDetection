import cv2 as cv
import image_utils
import time

class FrameStore(object):
    def __init__(self, i_id, i_converter ):
        self.__frames = {}
        self.__id = i_id
        self.__converter = i_converter
    def getFrame(self, i_format):
        if not self.__frames.has_key(self.__id):
            msg = "Frame store not initialised with an image associated with " + self.__id
            raise ValueError, msg
        else:
            if self.__frames.has_key(i_format):
                return self.__frames[i_format]
            else:
                image = self.__converter( self.__frames[self.__id],  [i_format])
                return image[i_format] 
  
class IplFrameStore(FrameStore):
    def __init__(self):
        FrameStore.__init__(self, 'Ipl', image_utils.Ipl2Formats)

class FrameGrabber(object):
    def __init__(self, i_capture_device, i_scale=1. , i_color=False):
        self.__current_frame = IplFrameStore()
        self.__capture_device = i_capture_device
        self.__scale = i_scale
        #self.__time_start = time.time()
        self.__frame_cnt = 0
        self.__fps = 0
        self.__is_color = i_color
    def nextFrame(self):
	#current_frame = cv.highgui.cvQueryFrame(self.__capture_device )
	current_frame = cv.QueryFrame(self.__capture_device)
	if not( current_frame == None ):
		cv.cvFlip(current_frame, None, 1);
	return self.currentFrame()
    def currentFrame(self, i_format='Ipl'):
	return self.__current_frame.getFrame(i_format)
		
class FrameGrabberFile(FrameGrabber):
    def __init__(self, i_file, i_loop_back = True, i_scale=1.,  i_color=False):
        #FrameGrabber.__init__(self, cv.highgui.cvCreateFileCapture(i_file ), i_scale, i_color )
        FrameGrabber.__init__(self, cv.VideoCapture(i_file), i_scale, i_color )



if __name__ ==  "__main__":
    from PyQt4 import QtCore, QtGui
    from sys import stdin, exit, argv
    import qt_image_display

    timer = QtCore.QTimer()
    app = QtGui.QApplication(argv)
    display =  qt_image_display.ImageDisplay()
    frame_grabber = FrameGrabberFile("out.avi", i_loop_back = True, i_scale=1.0)
    #frame_grabber = FrameGrabberWebCam( i_scale=1.0, i_camera=0, i_color=False)
    def updateDisplay():
        current_frame = frame_grabber.nextFrame()
        #if current_frame == None:
        #    print "No image available"
        #    timer.stop()
        #else:
        print "image available"
        timer.stop()
            #display.drawImage(self, i_image, 0, 0)
	display.show()
            #qt_image =  frame_grabber.currentFrame('QImage')
            #frame_rate = str(frame_grabber.frameRate())
            #w = str(qt_image.width())
            #h = str(qt_image.height())
            #disp_str =  frame_rate + " fps, width = " +  w  + ", height = " + h
            #display.setImage(qt_image, i_text=QtCore.QString(disp_str))
            #display.show()
    #frame_grabber = FrameGrabberWebCam( i_scale=1.0, i_camera=0, i_color=False)
#    display =  qt_image_display.ImageDisplay()
    QtCore.QObject.connect(timer, QtCore.SIGNAL("timeout()"), updateDisplay )
    timer.start( 50 )
    retVal = app.exec_()
    exit(retVal)
 
