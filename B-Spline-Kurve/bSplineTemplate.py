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
        self.degree = 4
        self.curvepoints = 0
        self.knotvector = []


    def render(self):
        glClear(GL_COLOR_BUFFER_BIT)

        myVbo = vbo.VBO(np.array(self.points, 'f'))
        myVbo.bind()

        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(2, GL_FLOAT, 0, myVbo)

        glColor(self.color)

        # wenn ein punkt GL_POINT wenn mehr GL_LINE_STRIP
        glDrawArrays(GL_POINTS, 0, len(self.points))
        if len(self.points) > 1:
            glDrawArrays(GL_LINE_STRIP, 0, len(self.points))


            #calc knotvector [kann eventuell nur aufgerufen werden wenn neuer punkt o.a veränderung kommt]
            self.knotvector = []

            points_len = len(self.points) - 1

            if points_len < self.degree:
                return

            for t in range(self.degree):
                self.knotvector.append(0)

            for t in range(1, (points_len - (self.degree - 2))): #(n - (k - 2))
                self.knotvector.append(t)

            for t in range(self.degree):#(n - (k - 2))
                self.knotvector.append((points_len - (self.degree - 2)))


            curve_points = []
            for i in range(self.degree):
                t = max(self.knotvector) + (i / self.curvepoints) #FIXME + oder * ?

                r = None
                #which j in knotV is the nearest to t
                for j, item in enumerate(self.knotvector):
                    if item <= t < self.knotvector[j + 1]:
                        r = j
                        print("r: ", r)
                        break

                if r is not None:
                    pass

                p = self.deboor(self.degree, self.points, self.knotvector, t)

                curve_points.append(p)


            myVbo = vbo.VBO(np.array(curve_points, 'f'))
            myVbo.bind()

            glEnableClientState(GL_VERTEX_ARRAY)
            glVertexPointer(2, GL_FLOAT, 0, myVbo)

            glColor([1.0, 1.0, 0])

            glDrawArrays(GL_LINE_STRIP, 0, len(curve_points))

        myVbo.unbind()
        glDisableClientState(GL_VERTEX_ARRAY)

        glFlush()


    def deboor(self, degree, controlpoints, knotvector, t): #TODO
        print("Draw a curve, pikachu!")


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
        self.window = glfw.create_window(self.width, self.height, "B-Spline-Kurve", None, None)
        if not self.window:
            glfw.terminate()
            return

        # Make the window's context current
        glfw.make_context_current(self.window)

        # initialize GL
        glViewport(0, 0, self.width, self.height)
        glPointSize(5.0) #size of GL_POINTS
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
        #self.pointStack = []


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
                self.scene.render()

                glfw.swap_buffers(self.window)
                # Poll for and process events
                glfw.poll_events()

        # end
        glfw.terminate()



    def mouseButtonCall(self, window, button, action, mods):
        if action == glfw.PRESS:
            if button == glfw.MOUSE_BUTTON_LEFT:
                x, y = glfw.get_cursor_pos(window)
                x = x / self.width * 2 - 1
                y = - (y / self.height * 2 - 1)

                self.scene.points.append([x,y])
                self.scene.curvepoints += 1





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
                    #print("curvepoints ++")
                    self.scene.curvepoints += 1
                else:
                    #print("curvepoints --")
                    self.scene.curvepoints -= 1

            if key == glfw.KEY_M:
                if self.shiftFlag:
                    #print("degree ++")
                    self.scene.degree += 1
                else:
                    #print("degree --")
                    if self.scene.degree > 2: # k min 2
                        self.scene.degree -= 1


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