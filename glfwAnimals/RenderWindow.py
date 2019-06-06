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

import numpy as np

from helper import ObjParser, BBox

myVBO = None

class Scene:
    """ OpenGL 2D scene class """
    # initialization
    def __init__(self, width, height):
        global myVBO
        self.width = width
        self.height = height

        self.object = ObjParser("cow.obj")

        self.bbox = BBox(self.object)
        self.bbox.move_to_origin()
        self.bbox.scale_to_kanonisches_Sichtvolumen()

        self.points = self.bbox.points

        #self.points = [p/np.linalg.norm(p) for p in self.points]

        #self.points = self.points*width

        myVBO = vbo.VBO(np.array(self.points, 'f'))

    # render 
    def render(self):
        global myVBO

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glColor3f(.75,.75,.75)
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        myVBO.bind()
        glVertexPointerf(myVBO)
        glEnableClientState(GL_VERTEX_ARRAY)
        glDrawArrays(GL_POLYGON, 0, len(self.points))
        myVBO.unbind()

        glDisableClientState(GL_VERTEX_ARRAY)
        glFlush()







class RenderWindow:
    """GLFW Rendering window class"""
    def __init__(self):
        
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
        self.window = glfw.create_window(self.width, self.height, "2D Graphics", None, None)
        if not self.window:
            glfw.terminate()
            return

        # Make the window's context current
        glfw.make_context_current(self.window)
    
        # initialize GL
        glViewport(0, 0, self.width, self.height)
        glEnable(GL_DEPTH_TEST)
        glClearColor(1.0, 1.0, 1.0, 1.0)
        glMatrixMode(GL_PROJECTION)
        glOrtho(-self.width/2,self.width/2,-self.height/2,self.height/2,-2,2)
        glMatrixMode(GL_MODELVIEW)

        
        # set window callbacks
        glfw.set_mouse_button_callback(self.window, self.onMouseButton)
        glfw.set_key_callback(self.window, self.onKeyboard)
        glfw.set_window_size_callback(self.window, self.onSize)
        
        # create 3D
        self.scene = Scene(self.width, self.height)
        
        # exit flag
        self.exitNow = False

        # animation flag
        self.animation = True

        # change color of the background or the object
    
    
    def onMouseButton(self, win, button, action, mods):
        print("mouse button: ", win, button, action, mods)
        if action == glfw.PRESS:
            if button == glfw.MOUSE_BUTTON_LEFT:
                print("I should rotate now.")
            if button == glfw.MOUSE_BUTTON_MIDDLE:
                print("Zoom in zoom out.")
            if button == glfw.MOUSE_BUTTON_RIGHT:
                print("Move your body.")


    def onKeyboard(self, win, key, scancode, action, mods):
        print("keyboard: ", win, key, scancode, action, mods)
        if action == glfw.PRESS:
            # ESC to quit
            if key == glfw.KEY_ESCAPE:
                self.exitNow = True
            if key == glfw.KEY_V:
                # toggle show vector
                self.scene.showVector = not self.scene.showVector
            if key == glfw.KEY_A:
                # toggle animation
                self.animation = not self.animation

            if key == glfw.KEY_O:
                print("Now, i should switch to othogonal-projection")
            if key == glfw.KEY_P:
                print("Now, i should switch to central-projection")

            if key == glfw.KEY_F:
                self.focus = not self.focus

            if key == glfw.KEY_S:
                print("Switch color to black")
            if key == glfw.KEY_W:
                print("Switch color to white")
            if key == glfw.KEY_R:
                print("Switch color to red")
            if key == glfw.KEY_B:
                print("Switch color to blue")
            if key == glfw.KEY_G:
                print("Switch color to yellow")



    def onSize(self, win, width, height):
        print("onsize: ", win, width, height)
        self.width = width
        self.height = height
        self.aspect = width/float(height)
        glViewport(0, 0, self.width, self.height)
    

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
    rw = RenderWindow()
    rw.run()


# call main
if __name__ == '__main__':
    main()