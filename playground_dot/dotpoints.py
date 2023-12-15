import random
from OpenGL.GL.shaders import compileProgram, compileShader
import OpenGL as gl 
from OpenGL.GL import *
import OpenGL_accelerate
import numpy as np

class DotPoints:
    all_dots = []
    
    def __init__(self, self_x = None, self_y= None, self_z=None):
        self.x = self_x if self_x is not None else random.uniform(-1, 1)
        self.y = self_y if self_y is not None else random.uniform(-1, 1)
        self.z = self_z if self_z is not None else 0
        # self.r = r
        # self.g = g
        # self.b = b
        self.time = 0
        self.shader = self.create_shader_program('shaders/vertex_shader.txt', 'shaders/fragment_shader.txt')
        self.vbo = None
        self.add_to_list(self)
        self.inititialize()
        
    def add_to_list(self, dot): 
        DotPoints.all_dots.append(dot)
        
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
      
    def update_vbo(self):
        self.init_vbo([self.x, self.y, self.z])
        
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
        
    def draw(self, x = None, y = None, z = None):
        self.init_vbo([x or self.x, y or self.y, z or self.z])
        
        try:
            glDrawArrays(GL_POINTS, 0, 1)
            glEnable(GL_POINT_SMOOTH)
        except Exception as e:
            print(e)
            
    @classmethod
    def draw_dots(cls):
        glClear(GL_COLOR_BUFFER_BIT)  # clear screen
        
        for dot in cls.all_dots:
            print(dot)
            dot.update_vbo()
            print(dot.x, dot.y, dot.z)
            dot.draw()
            
    
        
        