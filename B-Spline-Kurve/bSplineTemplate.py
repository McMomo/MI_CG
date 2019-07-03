import glfw, os, sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.arrays import vbo
import numpy as np

class Scene():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.color = [0.0, 1.0, 0.0]
        self.background = [1.0, 1.0, 1.0, 1.0]
        self.points = []
        self.counter = 0

    def render(self):
        glClearColor(self.background[0],self.background[1],self.background[2],self.background[3])

        myVbo = vbo.VBO(np.array(self.points, 'f'))
        myVbo.bind()

        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(3, GL_FLOAT, 24, myVbo)

        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        glColor(self.color)

        glDrawArrays(GL_LINE, 0, len(self.points))

        myVbo.unbind()
        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_NORMAL_ARRAY)

        glFlush()




class RenderWindow():
    def __init__(self):
        # save current working directory
        cwd = os.getcwd()

        # Initialize the library
        if not glfw.init():
            return

        # restore cwd
        os.chdir(cwd)

        # version hints
        # glfw.WindowHint(glfw.CONTEXT_VERSION_MAJOR, 3)
        # glfw.WindowHint(glfw.CONTEXT_VERSION_MINOR, 3)
        # glfw.WindowHint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
        # glfw.WindowHint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

        # buffer hints
        glfw.window_hint(glfw.DEPTH_BITS, 32)

        # define desire frame rate
        self.frame_rate = 100

        # make a window
        self.width, self.height = 640, 480
        self.aspect = self.width / float(self.height)
        self.window = glfw.create_window(self.width, self.height, "GLFW Animals", None, None)
        if not self.window:
            glfw.terminate()
            return

        # Make the window's context current
        glfw.make_context_current(self.window)

        # initialize GL
        glViewport(0, 0, self.width, self.height)
        glEnable(GL_DEPTH_TEST)
        glClearColor(1.0, 1.0, 1.0, 1.0)  # Background Color
        glMatrixMode(GL_PROJECTION)
        glMatrixMode(GL_MODELVIEW)

        # callbacks
        glfw.set_key_callback(self.window, self.keyboardCall)
        glfw.set_mouse_button_callback(self.window, self.mouseButtonCall)

        self.scene = Scene(self.width, self.height)

        self.shiftFlag = False
        self.exitNow = False
        self.render = False

    def run(self):
        glfw.set_time(0.0)
        t = 0.0
        while not glfw.window_should_close(self.window) and not self.exitNow:
            # update everx x seconds
            currT = glfw.get_time()
            if currT - t > 1.0/self.frame_rate:
                # update time
                t = currT
                # clear
                glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

                #render
                #self.scene.render()

                glfw.swap_buffers(self.window)
                # Poll for and process events
                glfw.poll_events()

        # end
        glfw.terminate()


    def mouseButtonCall(self, window, button, action, mods):
        if action == glfw.PRESS:
            if button == glfw.MOUSE_BUTTON_LEFT:
                x, y = glfw.get_cursor_pos(window)
                x = x / self.width
                y = y / self.height

                self.scene.points.append((x,y,))
                self.scene.counter += 1

                self.scene.render()

    def keyboardCall(self, window, key, scancode, action, mods):
        if action == glfw.PRESS:

            # ESC to quit
            if key == glfw.KEY_ESCAPE:
                self.exitNow = True
            # Q to quit
            if key == glfw.KEY_Q:
                self.exitNow = True

            if key == glfw.KEY_LEFT_SHIFT or key == glfw.KEY_RIGHT_SHIFT:
                self.shiftFlag = True

            if key == glfw.KEY_K:
                if self.shiftFlag:
                    print("curvepoints ++")
                else:
                    print("curvepoints --")

            if key == glfw.KEY_M:
                if self.shiftFlag:
                    print("degree ++")
                else:
                    print("degree --")

            self.scene.render()

        if action == glfw.RELEASE:

            if key == glfw.KEY_LEFT_SHIFT or key == glfw.KEY_RIGHT_SHIFT:
                self.shiftFlag = False



# main() function
def main():
    print("Simple glfw B-SPLINE")
    rw = RenderWindow()
    rw.run()


# call main
if __name__ == '__main__':
    main()