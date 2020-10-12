
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
    thickness = 0.01
    walls = [[0, 0.0, thickness, 4], [2.5, 2, 5, thickness], [5, 3.0, thickness, 2], 
            [4.0, 4, 2, thickness], [3, 5.0, thickness, 2], [4.0, 6, 2, thickness], 
            [5, 7.0, thickness, 2], [8.0, 8, 6, thickness], [11, 6.0, thickness, 4], 
            [10.0, 4, 2, thickness], [9, 5.0, thickness, 2], [8.0, 6, 2, thickness], 
            [7, 4.0, thickness, 4], [8.5, 2, 3, thickness], [10, -2.0, thickness, 8], 
            [11.5, -6, 3, thickness], [13, -3.0, thickness, 6], [14.0, 0, 2, thickness], 
            [15, -4.0, thickness, -8], [12.5, -8, 5, thickness], [10, -9.0, thickness, 2], 
            [9.0, -10, 2, thickness], [8, -9.0, thickness, 2], [6.5, -8, 3, thickness], 
            [5, -10.5, thickness, 5], [4.0, -13, 2, thickness], [3, -12.0, thickness, 2], 
            [2.0, -11, 2, thickness], [1, -10.0, thickness, 2], [2.0, -9, 2, thickness], 
            [3, -7.5, thickness, 3], [2.0, -6, 2, thickness], [1, -5.0, thickness, 2], 
            [3.0, -4, 4, thickness], [5, -5.0, thickness, 2], [6.5, -6, 3, thickness], 
            [8, -4.0, thickness, 4], [4.0, -2, 8, thickness]]

    weirdObjectColor = [1.0, 1.0, 0.0]


    def __init__(self):

        pygame.init() 
        pygame.display.set_caption('TGRA Assignment 34 -- Luca Fluri / Andy Méry')

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
        self.UP_key_down = False
        self.DOWN_key_down = False


        self.white_background = False

    def update(self):
        delta_time = self.clock.tick() / 1000.0

        self.angle += (pi * delta_time) * 180.0/pi
        # if self.angle > 180:
        #     self.angle -= 180


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
            self.view_matrix.yaw(90 * delta_time)
        if self.RIGHT_key_down:
            self.view_matrix.yaw(-90 * delta_time)
        # if self.UP_key_down:
        #     self.view_matrix.pitch(90 * delta_time)
        # if self.DOWN_key_down:
        #     self.view_matrix.pitch(-90 * delta_time)

        if self.T_key_down:
            self.fov -= 1.5 * delta_time
        if self.G_key_down:
            self.fov += 1.5 * delta_time

        
        
    

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
        for wall in self.walls:
            x, y, xlength, ylength = wall
            if self.checkWallCollision(x, y, xlength, ylength):
                self.drawWall(x, y, xlength, ylength, [0.0, 1.0, 0.0])
            else:
                self.drawWall(x, y, xlength, ylength)

        # Rotating Cube
        if self.checkWallCollision(8, 0, sqrt(2), sqrt(2)):
            self.weirdObjectColor=[random(), random(), random()]
        self.drawWeirdRotatingObject()

        pygame.display.flip()


    def clamp(self, val, minVal, maxVal):
        return max(minVal, min(maxVal, val))

    def checkWallCollision(self, x, y, xlength, ylength):
        # Camera Collision Circle radius:
        radius = 0.25

        # Get closest point on box to camera center
        camera = self.view_matrix.eye

        P = Point(self.clamp(camera.x, x-xlength/2, x+xlength/2),
                self.clamp(camera.y, y-ylength/2, y+ylength/2),
                camera.z)

        # Vector Camera to closest Point
        V = P - camera
        distance = V.__len__()

        collision = distance < radius

        # Hard Copy V
        V_tmp = Vector(V.x, V.y, V.z)
        # V_tmp.normalize()
        mult = radius/distance
        V_tmp.x *= mult
        V_tmp.y *= mult
        # Used to reposition Camera
        # V_tmp = radius Vector
        R = (V_tmp) - V


        if(collision): 
            # Reposition Camera
            self.view_matrix.eye -= R

        return collision


    def drawWall(self, x, y, xlength, ylength, color = [1.0, 0.0, 0.0]):
        r, g, b = color
        self.shader.set_solid_color(r, g, b)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(x, y, 4.0) 
        self.model_matrix.add_scale(xlength, ylength, 8)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw(self.shader)
        self.model_matrix.pop_matrix()

    
    def drawWeirdRotatingObject(self):
        r, g, b = self.weirdObjectColor
        for i in range(0, 360, 30):
            self.shader.set_solid_color(r, g, b)
            self.model_matrix.push_matrix()
            self.model_matrix.add_translation(8.0, 0.0 , 3.0)  
            self.model_matrix.add_scale(1, 1, 1)
            self.model_matrix.add_rotation_x(i + self.angle)
            self.model_matrix.add_rotation_z(self.angle)
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
                    if event.key == K_UP:
                        self.UP_key_down = True
                    if event.key == K_DOWN:
                        self.DOWN_key_down = True

                elif event.type == pygame.KEYUP:
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
                    if event.key == K_UP:
                        self.UP_key_down = False
                    if event.key == K_DOWN:
                        self.DOWN_key_down = False
            
            self.update()
            self.display()

        #OUT OF GAME LOOP
        pygame.quit()

    def start(self):
        self.program_loop()

if __name__ == "__main__":
    GraphicsProgram3D().start()