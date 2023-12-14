import pygame
import OpenGL as gl 
from OpenGL.GL import *
import OpenGL_accelerate
from OpenGL.GL.shaders import compileProgram, compileShader
import array
import random
import struct
import numpy as np
    
class app:
    def __init__(self):
        
        self.screen = pygame.display.set_mode((800, 600), pygame.OPENGL | pygame.DOUBLEBUF) #openGL window (double buffer will be used, which employs two image bufers. Te pixel data from one bufer is displayed on screen while new data is being written into a second bufer
        self.clock = pygame.time.Clock()
        
        #openGL stuff
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 1) #anti-aliasing (smooth edges)
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, 4) #anti-aliasing (smooth edges)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE) #core profile (no deprecated functions) 
        
        #shaders
        self.shader  = self.create_shader_program('shaders/vertex_shader.txt', 'shaders/fragment_shader.txt')
        
        self.running = True
        self.main_loop() 
        self.vbo = None
        
    def create_shader_program(self, vertex_filepath, fragment_filepath):
        #region reader vertex and fragment shader files
        with open(vertex_filepath, 'r') as f:
            vertex_src = f.readlines() #read all lines in file and return them as a list of strings
        
        with open(fragment_filepath, 'r') as f:
            fragment_src = f.readlines()
        #endregion
        
        #region compile shaders (vertex and fragment)
        vertex_shader = compileShader(''.join(vertex_src), GL_VERTEX_SHADER)
        fragment_shader = compileShader(''.join(fragment_src), GL_FRAGMENT_SHADER)
        #endregion
        
        #region create shader program (vertex and fragment shader)
        shader = compileProgram(vertex_shader, fragment_shader)
        #endregion
        
        #region link shader program to openGL
        glLinkProgram(shader)
        #check if shader program was linked successfully
        if glGetProgramiv(shader, GL_LINK_STATUS) != GL_TRUE:
            raise RuntimeError(glGetProgramInfoLog(shader))
        #endregion
        
        return shader
    
    def initialize(self):
        glPointSize(1.0) #size of point
        glEnable(GL_POINT_SMOOTH) #smooth point
        glUseProgram(self.shader) #use shader program (vertex and fragment shader)
    
    def init_vbo(self, vertices):
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        
        # Convert vertices to NumPy array
        vertices_np = np.array(vertices, dtype=np.float32)
        
        # Upload data to GPU (convert NumPy array to ctypes array)
        glBufferData(GL_ARRAY_BUFFER, 
                     vertices_np.nbytes, 
                     vertices_np, 
                     GL_STATIC_DRAW)
        
        position_loc = glGetAttribLocation(self.shader, "inPosition") #get location of inPosition in vertex shader
        glEnableVertexAttribArray(position_loc) #enable vertex attribute array
        glVertexAttribPointer(position_loc, 
                              3, 
                              GL_FLOAT, 
                              False, 
                              3 * sizeof(GLfloat), 
                              ctypes.c_void_p(0)) #specify how openGL should interpret the vertex data (index, size, type, normalized, stride, pointer)
        
    def gl_draw(self):
        vertices =[]
        glClear(GL_COLOR_BUFFER_BIT) #clear screen

        for i in range(3):
            vertices.extend([random.uniform(-1, 1), random.uniform(-1, 1), 0.0]) #create random points (x, y, z)
        #vertices.extend([0.0, 0.0, 0.0])
            
        self.init_vbo(vertices) #initialize buffer object (vertices)
        
        
        try:
            glDrawArrays(GL_POINTS, 0, len(vertices)//3)
        except Exception as e:
            print(e)

    
    
    def update(self):
        pygame.display.flip()

    def fps(self):
        self.clock.tick(60)
    
    def quit(self):
        pygame.quit()
        quit()
        
    def main_loop(self):
        self.initialize()

        while self.running:
            self.gl_draw()

            self.update()

            self.fps()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

        self.quit()
    

if __name__ == "__main__":
    app()
    