import glfw, os, sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.arrays import vbo
import numpy as np





class Scene():
    def __init__(self):
        self.points = []
        self.curvepoints = []
        self.degree = 4
        self.curvepoints_count = 0
        self.knotvector = []


    def render(self):
        glClear(GL_COLOR_BUFFER_BIT)

        myVbo = vbo.VBO(np.array(self.points, 'f'))
        myVbo.bind()

        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(2, GL_FLOAT, 0, myVbo)

        glColor([0.0, 0.0, 0.0])
        glPointSize(5.0)  # size of GL_POINTS

        # wenn ein punkt GL_POINT wenn mehr GL_LINE_STRIP
        glDrawArrays(GL_POINTS, 0, len(self.points))
        if len(self.points) > 1:
            glDrawArrays(GL_LINE_STRIP, 0, len(self.points))

        if len(self.points) >= self.degree:
            curveVbo = vbo.VBO(np.array(self.curvepoints, 'f'))
            curveVbo.bind()

            glEnableClientState(GL_VERTEX_ARRAY)
            glVertexPointer(2, GL_FLOAT, 0, curveVbo)

            glColor([1.0, 0, 0])

            glDrawArrays(GL_LINE_STRIP, 0, len(self.curvepoints))
            curveVbo.unbind()

        myVbo.unbind()
        glDisableClientState(GL_VERTEX_ARRAY)

        glFlush()


    def calc_curve(self):
        if len(self.points) >= self.degree:
            self.curvepoints = []

            self.knotvector = self.calc_knotvector(len(self.points), self.degree)

            m = len(self.knotvector) - 1

            for j in range(self.degree - 1, m - self.degree + 1):  # FIXME - 1, + 1
                if self.knotvector[j] != self.knotvector[j + 1]:
                    for t in np.linspace(self.knotvector[j], self.knotvector[j + 1], self.curvepoints_count):
                        p = self.deboor(self.degree, self.points, self.knotvector, j, t)
                        self.curvepoints.append(p)
                        # print("p: ", p)


    def calc_knotvector(self, points_len, degree):
        knotvector = []

        for t in range(degree):  # FIXME + 1
            knotvector.append(0)
        for t in range(1, (points_len - (degree - 2))):  # (n - (k - 2)) FIXME - 1
            knotvector.append(t)
        for t in range(degree):  # (n - (k - 2))
            knotvector.append((points_len - (degree - 2)))  # FIXME - 2

        print(knotvector)
        return knotvector

    def deboor(self, degree, controlpoints, knotvector, j, t):
        n = len(knotvector) - len(controlpoints) - 1

        if degree == 0:
            if j == len(controlpoints):
                return np.array(controlpoints[j - 1])
            if j < 0:
                return np.array(controlpoints[0])
            return np.array(controlpoints[j])

        else:
            w1 = self.calc_w(knotvector, j, n - degree + 1, t)
            w2 = self.calc_w(knotvector, j, n - degree + 1, t)

            d1 = self.deboor(degree - 1, controlpoints, knotvector, j - 1, t)
            d2 = self.deboor(degree - 1, controlpoints, knotvector, j, t)

            return (1 - w1) * d1 + w2 * d2

    def calc_w(self, knotvector, i, n, t):
        if knotvector[i] < knotvector[i + n]:
            return (t - knotvector[i]) / (knotvector[i + n] - knotvector[i])
        else:
            return 0


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
        glClearColor(1.0, 1.0, 1.0, 1.0)  # Background Color

        glMatrixMode(GL_PROJECTION)
        glMatrixMode(GL_MODELVIEW)

        # callbacks
        glfw.set_key_callback(self.window, self.keyboardCall)
        glfw.set_mouse_button_callback(self.window, self.mouseButtonCall)

        self.scene = Scene()


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

                self.scene.points.append(np.array([x, y]))
                self.scene.curvepoints_count += 1

                self.scene.calc_curve()




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

            if key == glfw.KEY_M:
                if self.shiftFlag:
                    # print("curvepoints ++")
                    self.scene.curvepoints_count += 1
                else:
                    # print("curvepoints --")
                    if self.scene.curvepoints_count > 1:
                        self.scene.curvepoints_count -= 1

                self.scene.calc_curve()

            if key == glfw.KEY_K:
                if self.shiftFlag:
                    #print("degree ++")
                    self.scene.degree += 1
                else:
                    #print("degree --")
                    if self.scene.degree > 2: # k min 2
                        self.scene.degree -= 1

                self.scene.calc_curve()

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