# coding=UTF-8
import sys
from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import QtOpenGL
import OpenGL.GLU as glu
import OpenGL.GL as gl
from numpy import array


class GLWidget(QtOpenGL.QGLWidget):
    def __init__(self, parent=None):
        self.parent = parent
        QtOpenGL.QGLWidget.__init__(self, parent)
        self.yRotDeg = 0.0
    def spin(self):
        self.yRotDeg = (self.yRotDeg  + 1) % 360.0
        self.parent.statusBar().showMessage('rotation %f' % self.yRotDeg)
        self.updateGL()
    def initGeometry(self):
        self.cubeVtxArray = array(
                [[0.0, 0.0, 0.0],
                 [1.0, 0.0, 0.0],
                 [1.0, 1.0, 0.0],
                 [0.0, 1.0, 0.0],
                 [0.0, 0.0, 1.0],
                 [1.0, 0.0, 1.0],
                 [1.0, 1.0, 1.0],
                 [0.0, 1.0, 1.0]])
        self.cubeIdxArray = [
                0, 1, 2, 3,
                3, 2, 6, 7,
                1, 0, 4, 5,
                2, 1, 5, 6,
                0, 3, 7, 4,
                7, 6, 5, 4 ]
        self.cubeClrArray = [
                [0.0, 0.0, 0.0],
                [1.0, 0.0, 0.0],
                [1.0, 1.0, 0.0],
                [0.0, 1.0, 0.0],
                [0.0, 0.0, 1.0],
                [1.0, 0.0, 1.0],
                [1.0, 1.0, 1.0],
                [0.0, 1.0, 1.0 ]]

    def initializeGL(self):
    	print "do initializeGL"
        self.qglClearColor(QtGui.QColor(0, 0,  150))
        self.initGeometry()
        gl.glEnable(gl.GL_DEPTH_TEST)

    def paintGL(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glLoadIdentity()

        gl.glTranslate(0.0, 0.0, -50.0)
        gl.glScale(20.0, 20.0, 20.0)
        gl.glRotate(self.yRotDeg, 0.2, 1.0, 0.3)
        gl.glTranslate(-0.5, -0.5, -0.5)

        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        gl.glEnableClientState(gl.GL_COLOR_ARRAY)
        gl.glVertexPointerf(self.cubeVtxArray)
        gl.glColorPointerf(self.cubeClrArray)
        gl.glDrawElementsui(gl.GL_QUADS, self.cubeIdxArray)

    def resizeGL(self, width, height):
        if height == 0: height = 1

        gl.glViewport(0, 0, width, height)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        aspect = width / float(height)

        glu.gluPerspective(45.0, aspect, 1.0, 100.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.resize(300, 300)
        self.setWindowTitle('GL Cube Test')

        self.initActions()
        self.initMenus()

        glWidget = GLWidget(self)
        self.setCentralWidget(glWidget)

        timer = QtCore.QTimer(self)
        timer.setInterval(20)
        QtCore.QObject.connect(timer, QtCore.SIGNAL('timeout()'), glWidget.spin)
        timer.start()
    def close(self):
        QtGui.qApp.quit()

    def initActions(self):
        self.exitAction = QtGui.QAction('Quit', self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip('Exit application')
        self.connect(self.exitAction, QtCore.SIGNAL('triggered()'), self.close)

    def initMenus(self):
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        fileMenu.addAction(self.exitAction)


if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)

	win = MainWindow()
	win.show()

	sys.exit(app.exec_())
