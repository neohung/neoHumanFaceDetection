# coding=UTF-8
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
 
def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    gluOrtho2D(-1.0, 1.0, -1.0, 1.0)
def drawReferenceAxis():
    glBegin(GL_LINES);
    glColor3f(1.0,0.0,0.0);
    glVertex3f( 0.0,0.0,0.0);
    glVertex3f( 1000.0,0.0,0.0);
    glEnd();
    glBegin(GL_LINES);
    glColor3f(0.9,0.3,0.0);
    glVertex3f( 0.0,0.0,0.0);
    glVertex3f( -1000.0,0.0,0.0);
    glEnd();

    glBegin(GL_LINES);
    glColor3f(0.0,1.0,0.0);
    glVertex3f(0.0, 0.0,0.0);
    glVertex3f(0.0, 1000.0,0.0);
    glEnd();

    glBegin(GL_LINES);
    glColor3f(0.3,0.8,0.0);
    glVertex3f(0.0, 0.0,0.0);
    glVertex3f(0.0, -1000.0,0.0);
    glEnd();

    glBegin(GL_LINES);
    glColor3f(0.0,0.0,1.0);
    glVertex3f( 0.0,0.0,0.0);
    glVertex3f( 0.0,0.0,1000.0);
    glEnd();

    glBegin(GL_LINES);
    glColor3f(0.0,0.0,0.5);
    glVertex3f( 0.0,0.0,0.0);
    glVertex3f( 0.0,0.0,-1000.0);
    glEnd();
def drawCentralAxis():
    #設定坐標軸中心點
    cx = .5 - 0;
    cy = -.25 - 0;
    cz = 1.0 - 0;
    #畫正負X軸
    glLineWidth(4.0);
    glBegin(GL_LINES);
    glColor3f(1.0,0.0,0.0);
    glVertex3f( cx,cy,cz);
    glVertex3f( cx+1000,cy,cz);
    glEnd();

    glBegin(GL_LINES);
    glColor3f(0.9,0.3,0.0);
    glVertex3f( cx,cy,cz);
    glVertex3f( cx -1000,cy,cz);
    glEnd();
    #畫正負Y軸
    glBegin(GL_LINES);
    glColor3f(0.0,1.0,0.0);
    glVertex3f( cx,cy,cz);
    glVertex3f( cx,cy+1000,cz);
    glEnd();

    glBegin(GL_LINES);
    glColor3f(0.3,0.8,0.0);
    glVertex3f( cx,cy,cz);
    glVertex3f( cx,cy-1000,cz);
    glEnd();
    #畫正負z軸
    glBegin(GL_LINES);
    glColor3f(0.0,0.0,1.0);
    glVertex3f( cx,cy,cz);
    glVertex3f( cx,cy,cz+5.0);
    glEnd();

    glBegin(GL_LINES);
    glColor3f(0.0,0.0,0.5);
    glVertex3f( cx,cy,cz);
    glVertex3f( cx,cy,cz-5.0);
    glEnd();
    glLineWidth(1.0);

def drawFunc():
    glClear(GL_COLOR_BUFFER_BIT)
    #drawCentralAxis()
    drawReferenceAxis()
    glFlush()
 
glutInit()
glutInitDisplayMode(GLUT_RGBA|GLUT_SINGLE)
glutInitWindowSize(640, 480)
glutCreateWindow("Sencond")
 
glutDisplayFunc(drawFunc)
init()
glutMainLoop()