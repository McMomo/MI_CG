"""
/*******************************************************************************
 *
 *            #, #,         CCCCCC  VV    VV MM      MM RRRRRRR
 *           %  %(  #%%#   CC    CC VV    VV MMM    MMM RR    RR
 *           %    %## #    CC        V    V  MM M  M MM RR    RR
 *            ,%      %    CC        VV  VV  MM  MM  MM RRRRRR
 *            (%      %,   CC    CC   VVVV   MM      MM RR   RR
 *              #%    %*    CCCCCC     VV    MM      MM RR    RR
 *             .%    %/
 *                (%.      Computer Vision & Mixed Reality Group
 *
 ******************************************************************************/
/**          @copyright:   Hochschule RheinMain,
 *                         University of Applied Sciences
 *              @author:   Prof. Dr. Ulrich Schwanecke
 *             @version:   0.9
 *                @date:   03.06.2019
 ******************************************************************************/
/**         RenderWindow.py
 *
 *          Simple Python OpenGL program that uses PyOpenGL + GLFW to get an
 *          OpenGL 3.2 context and display some 2D animation.
 ****
"""

import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.arrays import vbo

from ObjParser import ObjParser

import numpy as np

myVBO = None

class Scene():
    """ OpenGL 2D scene class """
    # initialization
    def __init__(self, width, height, filepath):
        self.color = (1.0, 0, 0)
        #self.background = (1.0, 1.0, 1.0, 1.0)
        self.angle = 0.0
        self.axis = np.array([0.0, 1.0, 0.0])
        self.width = width
        self.height = height
        self.zoomf = 0
        self.actOri = 1.0
        self.shadow = True

        glEnable(GL_LIGHTING)
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_LIGHT0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_NORMALIZE)

        self.objectPars = ObjParser(filepath)


    # render 
    def render(self, shadowFlag): # bool in render da die Flexiblität von self. in dem Fall schlecht ist
        global myVBO

        glTranslatef(0,-self.objectPars.bbox.bottom, 0)

        if not shadowFlag:
            glClear(GL_COLOR_BUFFER_BIT)
            glEnable(GL_LIGHT0)
        else:
            glDisable(GL_LIGHT0)

        vboList = self.objectPars.getVboList()
        myVBO = vbo.VBO(np.array(vboList, 'f'))
        myVBO.bind()

        glMultMatrixf(np.dot(self.actOri,self.rotate(self.angle, self.axis)))#rotation
        self.angle = 0.0
        self.actOri = 1.0

        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(3, GL_FLOAT, 24, myVBO)
        if not shadowFlag:
            glEnableClientState(GL_NORMAL_ARRAY)
            glNormalPointer(GL_FLOAT, 24, myVBO + 12)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        if shadowFlag:
            glColor3fv([1, 1, 1])
        else:
            glColor3f(self.color[0], self.color[1], self.color[2])

        glDrawArrays(GL_TRIANGLES, 0, len(vboList))

        myVBO.unbind()
        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_NORMAL_ARRAY)

        glTranslatef(0,self.objectPars.bbox.bottom, 0)

        glFlush()

    def shadowRender(self):
        glClear(GL_COLOR_BUFFER_BIT)
        light = [-5, -5, -5]
        p = [1.0, 0, 0, 0, 0, 1.0, 0, -1.0/light[1], 0, 0, 1.0, 0, 0, 0, 0, 0]

        self.render(not self.shadow)#render

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glTranslatef(light[0], light[1], light[2])
        glMultMatrixf(p)
        glTranslatef(-light[0], -light[1], -light[2])

        self.render(self.shadow)#render again

        glPopMatrix()



    def setColor(self, color, background):
        if background:
            glClearColor(color[0], color[1], color[2], 1.0)
        else:
            self.color = color


    def rotate(self, angle, axis):
        c, mc = np.cos(angle), 1-np.cos(angle)
        s = np.sin(angle)
        l = np.sqrt(np.dot(np.array(axis), np.array(axis)))

        x, y, z = np.array(axis) / l

        r = np.array(
            [[x*x*mc+c, x*y*mc-z*s, x*z*mc+y*s, 0],
             [x*y*mc+z*s, y*y*mc+c, y*z*mc-x*s, 0],
             [x*z*mc-y*s, y*z*mc+x*s, z*z*mc+c, 0],
             [0, 0, 0, 1]])
        #OpenGL uses column major order
        #-> transpose matrix
        return r.transpose()

    def zoom(self, factor): # führt bei schnellem scrollen zu fehlern
        self.zoomf = self.zoomf + factor
        max_zoom = 500

        if abs(self.zoomf) < max_zoom:
            f = 1 + factor / 100
            glScale(f, f, f)

        #Zoom limiter
        elif self.zoomf < -max_zoom:
            self.zoomf = -max_zoom
        elif self.zoomf > max_zoom:
            self.zoomf = max_zoom


    def move(self, moveTo):
        x, y = moveTo
        z = 0
        glTranslate(x, y, z)



class RenderWindow():
    """GLFW Rendering window class"""
    def __init__(self, filepath):
        
        # save current working directory
        cwd = os.getcwd()
        
        # Initialize the library
        if not glfw.init():
            return
        
        # restore cwd
        os.chdir(cwd)
        
        # version hints
        #glfw.WindowHint(glfw.CONTEXT_VERSION_MAJOR, 3)
        #glfw.WindowHint(glfw.CONTEXT_VERSION_MINOR, 3)
        #glfw.WindowHint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
        #glfw.WindowHint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        
        # buffer hints
        glfw.window_hint(glfw.DEPTH_BITS, 32)

        # define desired frame rate
        self.frame_rate = 100

        # True = othogonal & False = central
        self.projection = True

        #Who run the world? Flags!
        self.background = False
        self.pressed = False
        self.leftMouse = False
        self.middleMouse = False
        self.rightMouse = False
        self.p1 = None

        # exit flag
        self.exitNow = False

        # make a window
        self.width, self.height = 640, 480
        self.aspect = self.width/float(self.height)
        self.window = glfw.create_window(self.width, self.height, "GLFW Animals", None, None)
        if not self.window:
            glfw.terminate()
            return

        # Make the window's context current
        glfw.make_context_current(self.window)
    
        # initialize GL
        glViewport(0, 0, self.width, self.height)
        glEnable(GL_DEPTH_TEST)
        glClearColor(1.0, 1.0, 1.0, 1.0) #Background Color
        glMatrixMode(GL_PROJECTION)
        glMatrixMode(GL_MODELVIEW)

        # set window callbacks
        glfw.set_mouse_button_callback(self.window, self.onMouseButton)
        glfw.set_cursor_pos_callback(self.window, self.onMouseMove)
        glfw.set_scroll_callback(self.window, self.onScroll)
        glfw.set_key_callback(self.window, self.onKeyboard)
        glfw.set_window_size_callback(self.window, self.onSize)
        
        # create Scene
        self.scene = Scene(self.width, self.height, filepath)

        # Otherwise the Animald woudn't be displayed
        self.onSize(self.window, self.width, self.height)

        #"eye", otherwise you cant see the central
        gluLookAt(0.0, 0.0, 2, 0, 0, 1.0, 0.0, 1.0, 0.0)

        #Move animal in the middle of the Window
        self.scene.move((0, self.scene.objectPars.bbox.bottom))


    def projectOnSphere(self, x, y, r):
        x, y = x-self.width/2.0, self.height/2.0-y
        a = min(r*r, x**2 + y**2)
        z = np.sqrt(r*r - a)
        l = np.sqrt(x**2 + y**2 + z**2)
        return x/l, y/l, z/l


    def onScroll(self, win, x, y):
        self.scene.zoom(y)

    def onMouseMove(self, win, x, y):
        if self.pressed:

            if self.leftMouse:
                r = min(self.width, self.height) / 2.0

                if self.p1 == None:
                    self.p1 = self.projectOnSphere(x, y, r)

                else: # umgeht den l = 0 axis = [0, 0, 0] fehler wenn p1 == moveP taucht dieser auf
                    moveP = self.projectOnSphere(x, y, r)

                    self.scene.angle = np.arccos(np.dot(self.p1, moveP))
                    self.scene.axis = np.cross(self.p1, moveP)

                #weil jede bewegung vom letzten Punkt aus berechnet werden soll und nicht vom ersten punkt aus
                self.p1 = self.projectOnSphere(x, y, r)


            elif self.middleMouse:
                if self.p1 == None:
                    self.p1 = (x, y)

                if (self.p1[1] - y) > 0:
                    self.scene.zoom(1)
                elif (self.p1[1] - y) < 0:
                    self.scene.zoom(-1)


            # nach 180° rotation ist die Bewegung gespiegelt
            elif self.rightMouse:
                if self.p1 == None:
                    self.p1 = (x, y)

                difX = (x - self.p1[0]) #warum x -
                difY = (self.p1[1] - y) #und - y ??

                moveX = difX/self.width
                moveY = difY/self.height

                self.scene.move((moveX, moveY))

                #jede bewegung wird berechnet
                self.p1 = (x, y)




    def onMouseButton(self, win, button, action, mods):
        if action == glfw.PRESS:
            self.pressed = True

            if button == glfw.MOUSE_BUTTON_LEFT:
                #print("I should rotate ...")
                self.leftMouse = True

            elif button == glfw.MOUSE_BUTTON_MIDDLE:
                #print("Zoom in ...")
                self.middleMouse = True

            elif button == glfw.MOUSE_BUTTON_RIGHT:
                #print("Move your body.")
                self.rightMouse = True

        elif action == glfw.RELEASE:
            self.pressed = False

            if button == glfw.MOUSE_BUTTON_LEFT:
                self.leftMouse = False
                self.p1 = None
                np.dot(self.scene.actOri, self.scene.rotate(self.scene.angle, self.scene.axis))

            elif button == glfw.MOUSE_BUTTON_MIDDLE:
                self.middleMouse = False
                self.p1 = None

            elif button == glfw.MOUSE_BUTTON_RIGHT:
                self.rightMouse = False
                self.p1 = None



    def onKeyboard(self, win, key, scancode, action, mods):
        if action == glfw.PRESS:

            # ESC to quit
            if key == glfw.KEY_ESCAPE:
                self.exitNow = True
            # Q to quit
            if key == glfw.KEY_Q:
                self.exitNow = True

            if key == glfw.KEY_O:
                self.projection = True
                self.onSize(self.window, self.width, self.height)

            if key == glfw.KEY_P:
                self.projection = False
                self.onSize(self.window, self.width, self.height)


            if key == glfw.KEY_F: #press this to switch background color
                self.background = not self.background

            if key == glfw.KEY_S:
                self.scene.setColor((0.0, 0.0, 0.0), self.background)

            if key == glfw.KEY_W:
                self.scene.setColor((1.0, 1.0, 1.0), self.background)

            if key == glfw.KEY_R:
                self.scene.setColor((1.0, 0.0, 0.0), self.background)

            if key == glfw.KEY_B:
                self.scene.setColor((0.0, 0.0, 1.0), self.background)

            if key == glfw.KEY_G:
                self.scene.setColor((1.0, 1.0, 0.0), self.background)

            #shadow flag
            if key == glfw.KEY_H:
                self.scene.shadow = not self.scene.shadow


    def onSize(self, win, width, height):
        self.width = width
        self.height = height
        self.aspect = width/float(height)
        glViewport(0, 0, self.width, self.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        if self.projection:
            if width <= height:
                glOrtho(-1.5, 1.5,
                        -1.5 * height / width, 1.5 * height / width,
                        -4.0, 10.0)
            else:
                glOrtho(-1.5 * width / height, 1.5 * width / height,
                        -1.5, 1.5,
                        -4.0, 10.0)


        else:
            if self.width <= self.height:
                glFrustum(
                    -0.1, 0.1,
                    -0.1 * height / width, 0.1 * height / width,
                    0.1, 10.0
                )
            else:
                glFrustum(
                    -0.1 * width / height, 0.1 * width / height,
                    -0.1, 0.1,
                    0.1, 10.0
                )

        glMatrixMode(GL_MODELVIEW)
    

    def run(self):
        # initializer timer
        glfw.set_time(0.0)
        t = 0.0
        while not glfw.window_should_close(self.window) and not self.exitNow:
            # update every x seconds
            currT = glfw.get_time()
            if currT - t > 1.0/self.frame_rate:
                # update time
                t = currT
                # clear
                glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

                if self.scene.shadow: # render scene with shadow
                    self.scene.shadowRender()
                else: # render scene without shadow
                    self.scene.render(False)
                
                glfw.swap_buffers(self.window)
                # Poll for and process events
                glfw.poll_events()
        # end
        glfw.terminate()



# main() function
def main():
    print("Simple glfw render Window")
    rw = RenderWindow("cow.obj")
    rw.run()


# call main
if __name__ == '__main__':
    main()