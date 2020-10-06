
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
    def __init__(self):

        pygame.init() 
        pygame.display.set_mode((800,600), pygame.OPENGL|pygame.DOUBLEBUF)

        self.shader = Shader3D()
        self.shader.use()

        self.model_matrix = ModelMatrix()

        self.view_matrix = ViewMatrix()

        self.view_matrix.look(Point(0, 0, 4), Point(1, 0, 4), Vector(0, 0, 1))

        self.shader.set_view_matrix(self.view_matrix.get_matrix())

        self.projection_matrix = ProjectionMatrix()
        self.fov = 90
        # self.projection_matrix.set_orthographic(-2, 2, -2, 2, 0.5, 10)
        self.projection_matrix.set_perspective(120, 800/600, 0.5, 10 )
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
        if self.Q_key_down:
            # self.view_matrix.slide(1 * delta_time, 0, 0)
            self.view_matrix.yaw(180 * delta_time)
        if self.E_key_down:
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
    

    def display(self):
        glEnable(GL_DEPTH_TEST)  ### --- NEED THIS FOR NORMAL 3D BUT MANY EFFECTS BETTER WITH glDisable(GL_DEPTH_TEST) ... try it! --- ###

        if self.white_background:
            glClearColor(1.0, 1.0, 1.0, 1.0)
        else:
            glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)  ### --- YOU CAN ALSO CLEAR ONLY THE COLOR OR ONLY THE DEPTH --- ###

        glViewport(0, 0, 800, 600)

        self.projection_matrix.set_perspective(self.fov, 800/600, 0.5, 10 )
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
        # self.shader.set_solid_color(1.0, 0.0, 0.0)
        # self.model_matrix.push_matrix()
        # self.model_matrix.add_translation(3.5, 2.0 , 4.0) 
        # self.model_matrix.add_scale(7, 0.1, 8)
        # self.shader.set_model_matrix(self.model_matrix.matrix)
        # self.cube.draw(self.shader)
        # self.model_matrix.pop_matrix()


        # Draw Maze Walls in Clockwise Direction starting with back wall
        self.drawWall_y(2,-2, 0)
        self.drawWall_x(0, 5, 2)
        self.drawWall_y(2, 4, 5)
        self.drawWall_x(5, 3, 4)
        self.drawWall_y(4, 6, 3)
        self.drawWall_x(3, 5, 6)
        self.drawWall_y(6, 8, 5)
        self.drawWall_x(5, 11, 8)
        self.drawWall_y(8, 4, 11)
        self.drawWall_x(11, 9, 4)
        self.drawWall_y(4, 6, 9)
        self.drawWall_x(9, 7, 6)
        self.drawWall_y(6, 2, 7)
        self.drawWall_x(7, 10, 2)
        self.drawWall_y(2, -6, 10)
        self.drawWall_x(10, 13, -6)
        self.drawWall_y(-6, 0, 13)
        self.drawWall_x(13, 15, 0)
        self.drawWall_y(0, -8, 15)
        self.drawWall_x(15, 10, -8)
        self.drawWall_y(-8, -10, 10)
        self.drawWall_x(10, 8, -10)
        self.drawWall_y(-10, -8, 8)
        self.drawWall_x(8, 5, -8)
        self.drawWall_y(-8, -13, 5)
        self.drawWall_x(5, 3, -13)
        self.drawWall_y(-13, -11, 3)
        self.drawWall_x(3, 1, -11)
        self.drawWall_y(-11, -9, 1)
        self.drawWall_x(1, 3, -9)
        self.drawWall_y(-9, -6, 3)
        self.drawWall_x(3, 1, -6)
        self.drawWall_y(-6, -4, 1)
        self.drawWall_x(1, 5, -4)
        self.drawWall_y(-4, -6, 5)
        self.drawWall_x(5, 8, -6)
        self.drawWall_y(-6, -2, 8)
        self.drawWall_x(8, 0, -2)

        # self.drawWall_x(0, 10, -2)
        # self.drawWall_y(2, 10, 5)
        # self.drawWall_y(2, 10, 7)
        # self.drawWall_y(0 , 10, 7)

        # self.shader.set_solid_color(1.0, 0.0, 1.0)

        # self.model_matrix.push_matrix()
        # self.model_matrix.add_translation(0.0, 0.0 , -3.0)  
        # self.model_matrix.add_rotation_x(self.angle * 0.5)
        # self.model_matrix.add_rotation_y(self.angle * 0.25)
        # self.model_matrix.add_scale(3.0, 1.0 , 2.0)  
        # self.shader.set_model_matrix(self.model_matrix.matrix)
        # self.cube.draw(self.shader)
        # self.model_matrix.pop_matrix()

        pygame.display.flip()

    # Draws a wall from startPoint to EndPoint with thickness of 0.1
    def drawWall_x(self, start, end, y):
        length = end - start
        self.shader.set_solid_color(1.0, 0.0, 0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(length/2 + start, y, 4.0) 
        self.model_matrix.add_scale(length, 0.1, 8)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw(self.shader)
        self.model_matrix.pop_matrix()

    def drawWall_y(self, start, end, x):
        length = end - start
        self.shader.set_solid_color(1.0, 0.0, 0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(x, length/2 + start, 4.0) 
        self.model_matrix.add_scale(0.1, length, 8)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw(self.shader)
        self.model_matrix.pop_matrix()
        
        

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
            
            self.update()
            self.display()

        #OUT OF GAME LOOP
        pygame.quit()

    def start(self):
        self.program_loop()

if __name__ == "__main__":
    GraphicsProgram3D().start()