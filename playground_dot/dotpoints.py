import random
from OpenGL.GL.shaders import compileProgram, compileShader
import OpenGL as gl 
from OpenGL.GL import *
import OpenGL_accelerate
import numpy as np

class DotPoints:
    def __init__(self):
        self.x = random.uniform(-1,1)
        self.y = random.uniform(-1,1)
        self.z = 0
        # self.r = r
        # self.g = g
        # self.b = b
        self.time = 0
        self.shader = self.create_shader_program('shaders/vertex_shader.txt', 'shaders/fragment_shader.txt')
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
    
    def inititialize(self):
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
        
        # Specify layout of point data
        position_loc = glGetAttribLocation(self.shader, "inPosition") #get location of inPosition in vertex shader
        glEnableVertexAttribArray(position_loc) #enable vertex attribute array
        glVertexAttribPointer(position_loc, 
                              3, 
                              GL_FLOAT, 
                              False, 
                              3 * sizeof(GLfloat), 
                              ctypes.c_void_p(0)) #specify how openGL should interpret the vertex data (index, size, type, normalized, stride, pointer)
        
    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT) # clear screen 
        
        self.init_vbo([self.x, self.y, self.z])
        
        try:
            glDrawArrays(GL_POINTS, 0, 1)
            glEnable(GL_POINT_SMOOTH)
        except Exception as e:
            print(e)
        
    
    
        
        