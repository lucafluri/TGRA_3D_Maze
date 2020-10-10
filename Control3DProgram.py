
# from OpenGL.GL import *
# from OpenGL.GLU import *
from math import *

import pygame
from pygame.locals import *

import sys
import time

from Shaders import *
from Matrices import *

class GraphicsProgram3D:
    # Array of Walls
    # [x, y, x-length, y-length]
    walls = [[0, 0.0, 0.1, -4], [2.5, 2, 5, 0.1], [5, 3.0, 0.1, 2], 
            [4.0, 4, -2, 0.1], [3, 5.0, 0.1, 2], [4.0, 6, 2, 0.1], 
            [5, 7.0, 0.1, 2], [8.0, 8, 6, 0.1], [11, 6.0, 0.1, -4], 
            [10.0, 4, -2, 0.1], [9, 5.0, 0.1, 2], [8.0, 6, -2, 0.1], 
            [7, 4.0, 0.1, -4], [8.5, 2, 3, 0.1], [10, -2.0, 0.1, -8], 
            [11.5, -6, 3, 0.1], [13, -3.0, 0.1, 6], [14.0, 0, 2, 0.1], 
            [15, -4.0, 0.1, -8], [12.5, -8, -5, 0.1], [10, -9.0, 0.1, -2], 
            [9.0, -10, -2, 0.1], [8, -9.0, 0.1, 2], [6.5, -8, -3, 0.1], 
            [5, -10.5, 0.1, -5], [4.0, -13, -2, 0.1], [3, -12.0, 0.1, 2], 
            [2.0, -11, -2, 0.1], [1, -10.0, 0.1, 2], [2.0, -9, 2, 0.1], 
            [3, -7.5, 0.1, 3], [2.0, -6, -2, 0.1], [1, -5.0, 0.1, 2], 
            [3.0, -4, 4, 0.1], [5, -5.0, 0.1, -2], [6.5, -6, 3, 0.1], 
            [8, -4.0, 0.1, 4], [4.0, -2, -8, 0.1]]


    def __init__(self):

        pygame.init() 
        pygame.display.set_mode((800,600), pygame.OPENGL|pygame.DOUBLEBUF)

        self.shader = Shader3D()
        self.shader.use()

        self.model_matrix = ModelMatrix()

        self.view_matrix = ViewMatrix()

        self.view_matrix.look(Point(1, 0, 4), Point(10, 0, 4), Vector(0, 0, 1))

        self.shader.set_view_matrix(self.view_matrix.get_matrix())

        self.projection_matrix = ProjectionMatrix()
        self.fov = 90
        # self.projection_matrix.set_orthographic(-2, 2, -2, 2, 0.5, 10)
        self.projection_matrix.set_perspective(120, 800/600, 0.001, 10 )
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())

        self.cube = Cube()

        self.clock = pygame.time.Clock()
        self.clock.tick()

        self.angle = 0

        self.UP_key_down = False  
        self.W_key_down = False  
        self.S_key_down = False  
        self.A_key_down = False  
        self.D_key_down = False  
        self.E_key_down = False  
        self.Q_key_down = False  
        self.T_key_down = False  
        self.G_key_down = False
        self.LEFT_key_down = False
        self.RIGHT_key_down = False
        self.TOP_key_down = False
        self.DOWN_key_down = False


        self.white_background = False

    def update(self):
        delta_time = self.clock.tick() / 1000.0

        self.angle += (pi * delta_time) * 180.0/pi
        # if angle > 2 * pi:
        #     angle -= (2 * pi)


        if self.W_key_down:
            self.view_matrix.slide(0, 0, -1 * delta_time)
        if self.S_key_down:
            self.view_matrix.slide(0, 0, 1 * delta_time)
        if self.A_key_down:
            self.view_matrix.slide(-1 * delta_time, 0, 0)
            # self.view_matrix.yaw(180 * delta_time)
        if self.D_key_down:
            self.view_matrix.slide(1 * delta_time, 0, 0)
            # self.view_matrix.yaw(-180 * delta_time)
        if self.LEFT_key_down:
            # self.view_matrix.slide(1 * delta_time, 0, 0)
            self.view_matrix.yaw(180 * delta_time)
        if self.RIGHT_key_down:
            # self.view_matrix.slide(1 * delta_time, 0, 0)
            self.view_matrix.yaw(-180 * delta_time)

        if self.T_key_down:
            self.fov -= 1.5 * delta_time
        if self.G_key_down:
            self.fov += 1.5 * delta_time

        if self.UP_key_down:
            self.white_background = True
        else:
            self.white_background = False

        for wall in self.walls:
            x, y, xlength, ylength = wall
            # self.drawWall(x, y, xlength, ylength)
            # TODO Change to all Walls
            if(x == 2.5): self.checkWallCollision(x, y, xlength, ylength)
            # self.checkWallCollision(x, y, xlength, ylength)
    

    def display(self):
        glEnable(GL_DEPTH_TEST)  ### --- NEED THIS FOR NORMAL 3D BUT MANY EFFECTS BETTER WITH glDisable(GL_DEPTH_TEST) ... try it! --- ###

        if self.white_background:
            glClearColor(1.0, 1.0, 1.0, 1.0)
        else:
            glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)  ### --- YOU CAN ALSO CLEAR ONLY THE COLOR OR ONLY THE DEPTH --- ###

        glViewport(0, 0, 800, 600)

        self.projection_matrix.set_perspective(self.fov, 800/600, 0.001, 10 )
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())

        self.shader.set_view_matrix(self.view_matrix.get_matrix())


        self.model_matrix.load_identity()

        self.shader.set_solid_color(1.0, 1.0, 0.0)

        self.cube.set_vertices(self.shader)

        # Floor
        self.shader.set_solid_color(1.0, 1.0, 1.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(0.0, 0.0 , 0.0)  
        self.model_matrix.add_scale(100, 100, 0.1)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw(self.shader)
        self.model_matrix.pop_matrix()

        # Walls
        # TODO Enlarge Maze Paths
        for wall in self.walls:
            x, y, xlength, ylength = wall
            self.drawWall(x, y, xlength, ylength)


        # Draw Maze Walls in Clockwise Direction starting with back wall
        # self.drawWall_y(2,-2, 0)
        # self.drawWall_x(0, 5, 2)
        # self.drawWall_y(2, 4, 5)
        # self.drawWall_x(5, 3, 4)
        # self.drawWall_y(4, 6, 3)
        # self.drawWall_x(3, 5, 6)
        # self.drawWall_y(6, 8, 5)
        # self.drawWall_x(5, 11, 8)
        # self.drawWall_y(8, 4, 11)
        # self.drawWall_x(11, 9, 4)
        # self.drawWall_y(4, 6, 9)
        # self.drawWall_x(9, 7, 6)
        # self.drawWall_y(6, 2, 7)
        # self.drawWall_x(7, 10, 2)
        # self.drawWall_y(2, -6, 10)
        # self.drawWall_x(10, 13, -6)
        # self.drawWall_y(-6, 0, 13)
        # self.drawWall_x(13, 15, 0)
        # self.drawWall_y(0, -8, 15)
        # self.drawWall_x(15, 10, -8)
        # self.drawWall_y(-8, -10, 10)
        # self.drawWall_x(10, 8, -10)
        # self.drawWall_y(-10, -8, 8)
        # self.drawWall_x(8, 5, -8)
        # self.drawWall_y(-8, -13, 5)
        # self.drawWall_x(5, 3, -13)
        # self.drawWall_y(-13, -11, 3)
        # self.drawWall_x(3, 1, -11)
        # self.drawWall_y(-11, -9, 1)
        # self.drawWall_x(1, 3, -9)
        # self.drawWall_y(-9, -6, 3)
        # self.drawWall_x(3, 1, -6)
        # self.drawWall_y(-6, -4, 1)
        # self.drawWall_x(1, 5, -4)
        # self.drawWall_y(-4, -6, 5)
        # self.drawWall_x(5, 8, -6)
        # self.drawWall_y(-6, -2, 8)
        # self.drawWall_x(8, 0, -2)

        pygame.display.flip()



    def clamp(self, val, minVal, maxVal):
        return max(minVal, min(maxVal, val))

    def checkWallCollision(self, x, y, xlength, ylength):
        # Camera Collision Circle radius:
        radius = 1

        w = xlength / 2
        h = ylength / 2
        B = Point(x, y, 0)
        C = self.view_matrix.eye

        D = B-C
        P = Point(self.clamp(D.x, 0, w), self.clamp(D.y, 0, h), 0)

        V = (P - C)
        distance = sqrt(V.x**2 + V.y**2) 
        collision = distance < radius

        V_tmp = V
        V_tmp.__mul__(radius/V_tmp.__len__())
        # Used to reposition Camera
        R = (V_tmp) - V

        if(collision): 
            # print("Collision detected")
            # print("P: ", P.x, P.y)
            # print("V: ", V.x, V.y)
            # print("V_norm: ", V_tmp.x, V_tmp.y)
            # print("R: ", R.x, R.y)

            

            self.view_matrix.eye -= R

        else: 
            # print("\nWidth, height: ", w, h)
            # print("B: ", B.x, B.y)
            # print("C: ", C.x, C.y)
            # print("D: ", D.x, D.y)
            # print("D_len: ", sqrt(D.x**2 + D.y**2))
            # print("Distance: ", distance)
            # print("P: ", P.x, P.y)
            # print("No Collision")
        return collision


    def drawWall(self, x, y, xlength, ylength):
        self.shader.set_solid_color(1.0, 0.0, 0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(x, y, 4.0) 
        self.model_matrix.add_scale(xlength, ylength, 8)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw(self.shader)
        self.model_matrix.pop_matrix()

    # Draws a wall from startPoint to EndPoint with thickness of 0.1
    # def drawWall_x(self, start, end, y):
    #     length = end - start
    #     self.shader.set_solid_color(1.0, 0.0, 0.0)
    #     self.model_matrix.push_matrix()
    #     self.model_matrix.add_translation(length/2 + start, y, 4.0) 
    #     self.model_matrix.add_scale(length, 0.1, 8)
    #     self.shader.set_model_matrix(self.model_matrix.matrix)
    #     self.cube.draw(self.shader)
    #     self.model_matrix.pop_matrix()

    #     # Store Center Point and Width and height in Array
    #     #                           X        Y  X-Width Y-Height
    #     self.walls.append([length/2 + start, y, length, 0.1])

    # def drawWall_y(self, start, end, x):
    #     length = end - start
    #     self.shader.set_solid_color(1.0, 0.0, 0.0)
    #     self.model_matrix.push_matrix()
    #     self.model_matrix.add_translation(x, length/2 + start, 4.0) 
    #     self.model_matrix.add_scale(0.1, length, 8)
    #     self.shader.set_model_matrix(self.model_matrix.matrix)
    #     self.cube.draw(self.shader)
    #     self.model_matrix.pop_matrix()
        
    #     self.walls.append([x, length/2 + start, 0.1, length])

    def program_loop(self):
        exiting = False
        while not exiting:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Quitting!")
                    exiting = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        print("Escaping!")
                        exiting = True
                        
                    if event.key == K_UP:
                        self.UP_key_down = True
                    if event.key == K_w:
                        self.W_key_down = True
                    if event.key == K_s:
                        self.S_key_down = True
                    if event.key == K_a:
                        self.A_key_down = True
                    if event.key == K_d:
                        self.D_key_down = True
                    if event.key == K_e:
                        self.E_key_down = True
                    if event.key == K_q:
                        self.Q_key_down = True
                    if event.key == K_t:
                        self.T_key_down = True
                    if event.key == K_g:
                        self.G_key_down = True
                    if event.key == K_LEFT:
                        self.LEFT_key_down = True
                    if event.key == K_RIGHT:
                        self.RIGHT_key_down = True

                elif event.type == pygame.KEYUP:
                    if event.key == K_UP:
                        self.UP_key_down = False
                    if event.key == K_w:
                        self.W_key_down = False
                    if event.key == K_s:
                        self.S_key_down = False
                    if event.key == K_a:
                        self.A_key_down = False
                    if event.key == K_d:
                        self.D_key_down = False
                    if event.key == K_e:
                        self.E_key_down = False
                    if event.key == K_q:
                        self.Q_key_down = False
                    if event.key == K_t:
                        self.T_key_down = False
                    if event.key == K_g:
                        self.G_key_down = False
                    if event.key == K_LEFT:
                        self.LEFT_key_down = False
                    if event.key == K_RIGHT:
                        self.RIGHT_key_down = False
            
            self.update()
            self.display()

        #OUT OF GAME LOOP
        pygame.quit()

    def start(self):
        self.program_loop()

if __name__ == "__main__":
    GraphicsProgram3D().start()