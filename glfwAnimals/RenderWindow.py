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
        self.angle = 0.0
        self.axis = np.array([0.0, 1.0, 0.0])
        self.width = width
        self.height = height
        self.zoomf = 50
        self.actOri = 1.0
        glEnable(GL_LIGHTING)
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_LIGHT0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_NORMALIZE)

        self.objectPars = ObjParser(filepath)

    # render 
    def render(self):
        global myVBO

        glClear(GL_COLOR_BUFFER_BIT)
        vboList = self.objectPars.getVboList()
        myVBO = vbo.VBO(np.array(vboList, 'f'))
        myVBO.bind()

        glMultMatrixf(self.actOri * self.rotate(self.angle, self.axis))#rotation

        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_NORMAL_ARRAY)

        glVertexPointer(3, GL_FLOAT, 24, myVBO)
        glNormalPointer(GL_FLOAT, 24, myVBO + 12)

        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glColor3f(self.color[0], self.color[1], self.color[2])
        glDrawArrays(GL_TRIANGLES, 0, len(vboList))

        myVBO.unbind()
        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_NORMAL_ARRAY)
        glFlush()

    def setColor(self, color):
        self.color = color

    def rotate(self, angle, axis):
        c, mc = np.cos(angle), 1-np.cos(angle)
        s = np.sin(angle)
        l = np.sqrt(np.dot(np.array(axis), np.array(axis)))

        if l == 0:
            print("l : ", l, "\naxis: ", axis, "\n")
            x, y, z = np.array([0.0, 1.0, 0.0])/1.0
        else:
            x, y, z = np.array(axis) / l

        r = np.array(
            [[x*x*mc+c, x*y*mc-z*s, x*z*mc+y*s, 0],
             [x*y*mc+z*s, y*y*mc+c, y*z*mc-x*s, 0],
             [x*z*mc-y*s, y*z*mc+x*s, z*z*mc+c, 0],
             [0, 0, 0, 1]])
        #OpenGL uses column major order
        #-> transpose matrix
        return r.transpose()

    def zoom(self, factor): #FIXME 1
        f = 0
        f = 1 + factor / 100
        glScale(f, f, f)




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

        self.onSize(self.window, self.width, self.height) #Otherwise the Animald woudn't be displayed

        glMatrixMode(GL_MODELVIEW)

        # set window callbacks
        glfw.set_mouse_button_callback(self.window, self.onMouseButton)
        glfw.set_cursor_pos_callback(self.window, self.onMouseMove)
        glfw.set_key_callback(self.window, self.onKeyboard)
        glfw.set_window_size_callback(self.window, self.onSize)
        
        # create 3D
        self.scene = Scene(self.width, self.height, filepath)

        self.pressed = False
        self.leftMouse = False
        self.rightMouse = False
        self.p1 = None

        # exit flag
        self.exitNow = False


    def projectOnSphere(self, x, y, r):
        x, y = x-self.width/2.0, self.height/2.0-y
        a = min(r*r, x**2 + y**2)
        z = np.sqrt(r*r - a)
        l = np.sqrt(x**2 + y**2 + z**2)
        return x/l, y/l, z/l

    def onMouseMove(self, win, x, y):
        if self.pressed:
            print("mouse move: ", win, x, y)

            if self.leftMouse:
                r = min(self.width, self.height) / 2.0

                if self.p1 == None:
                    self.p1 = self.projectOnSphere(x, y, r)

                moveP = self.projectOnSphere(x, y, r)
                self.scene.angle = np.arccos(np.dot(self.p1, moveP))
                self.scene.axis = np.cross(self.p1, moveP)
                glutPostRedisplay() #FIXME 2

    def onMouseButton(self, win, button, action, mods):
        print("mouse button: ", win, button, action, mods)
        if action == glfw.PRESS:
            self.pressed = True
            if button == glfw.MOUSE_BUTTON_LEFT:
                print("I should rotate ...")
                self.leftMouse = True

            if button == glfw.MOUSE_BUTTON_MIDDLE:
                print("Zoom in ...")
                self.scene.zoom(self.scene.zoomf)

            if button == glfw.MOUSE_BUTTON_RIGHT:
                print("Move your body.")


        elif action == glfw.RELEASE:
            self.pressed = False
            if button == glfw.MOUSE_BUTTON_LEFT:
                print("... now.")
                self.leftMouse = False
                self.scene.actOri = self.scene.actOri * self.scene.rotate(self.scene.angle, self.scene.axis)
                self.scene.angle = 0
                self.p1 = None

            if button == glfw.MOUSE_BUTTON_MIDDLE:
                print("... zoom out.")
                self.scene.zoom(-self.scene.zoomf/2) #FIXME 1


            if button == glfw.MOUSE_BUTTON_RIGHT:
                print("Move your body.")




    def onKeyboard(self, win, key, scancode, action, mods):
        print("keyboard: ", win, key, scancode, action, mods)
        if action == glfw.PRESS:
            # ESC to quit
            if key == glfw.KEY_ESCAPE:
                self.exitNow = True

            if key == glfw.KEY_O:
                print("Now, i should switch to othogonal-projection")
            if key == glfw.KEY_P:
                print("Now, i should switch to central-projection")

            if key == glfw.KEY_F:
                self.focus = not self.focus

            if key == glfw.KEY_S:
                print("Switch color to black")
                self.scene.setColor((0.0, 0.0, 0.0))
            if key == glfw.KEY_W:
                print("Switch color to white")
                self.scene.setColor((1.0, 1.0, 1.0))
            if key == glfw.KEY_R:
                print("Switch color to red")
                self.scene.setColor((1.0, 0.0, 0.0))
            if key == glfw.KEY_B:
                print("Switch color to blue")
                self.scene.setColor((0.0, 0.0, 1.0))
            if key == glfw.KEY_G:
                print("Switch color to yellow")
                self.scene.setColor((1.0, 1.0, 0.0))



    def onSize(self, win, width, height):
        print("onsize: ", win, width, height)
        self.width = width
        self.height = height
        self.aspect = width/float(height)
        glViewport(0, 0, self.width, self.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        if width <= height:
            glOrtho(-1.5, 1.5,
                    -1.5 * height / width, 1.5 * height / width,
                    -1.0, 1.0)
        else:
            glOrtho(-1.5 * width / height, 1.5 * width / height,
                    -1.5, 1.5,
                    -1.0, 1.0)
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
                
                # render scene
                self.scene.render()
                
                glfw.swap_buffers(self.window)
                # Poll for and process events
                glfw.poll_events()
        # end
        glfw.terminate()



# main() function
def main():
    print("Simple glfw render Window")
    rw = RenderWindow("bunny.obj")
    rw.run()


# call main
if __name__ == '__main__':
    main()