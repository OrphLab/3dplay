import pygame
import OpenGL as gl 
from OpenGL.GL import *
import OpenGL_accelerate
from OpenGL.GL.shaders import compileProgram, compileShader
import array
import random
import struct
import numpy as np

class App:
    def __init__(self):
        self.width, self.height = 800, 600
        pygame.init()
        pygame.display.set_mode((self.width, self.height), DOUBLEBUF | OPENGL)
        self.clock = pygame.time.Clock()

        pygame.display.gl_set_attribute(GL_MULTISAMPLEBUFFERS, 1)
        pygame.display.gl_set_attribute(GL_MULTISAMPLESAMPLES, 4)
        pygame.display.gl_set_attribute(GL_CONTEXT_PROFILE_MASK, GL_CONTEXT_PROFILE_CORE)

        self.shader = self.create_shader_program('shaders/vertex_shader.txt', 'shaders/fragment_shader.txt')

        self.running = True
        self.main_loop()

    def create_shader_program(self, vertex_filepath, fragment_filepath):
        with open(vertex_filepath, 'r') as f:
            vertex_src = f.readlines()

        with open(fragment_filepath, 'r') as f:
            fragment_src = f.readlines()

        vertex_shader = compileShader(''.join(vertex_src), GL_VERTEX_SHADER)
        fragment_shader = compileShader(''.join(fragment_src), GL_FRAGMENT_SHADER)

        shader = compileProgram(vertex_shader, fragment_shader)

        glLinkProgram(shader)

        if glGetProgramiv(shader, GL_LINK_STATUS) != GL_TRUE:
            raise RuntimeError(glGetProgramInfoLog(shader))

        return shader

    def initialize(self):
        glEnable(GL_MULTISAMPLE)
        glEnable(GL_POINT_SMOOTH)
        glUseProgram(self.shader)

        # Create Vertex Array Object (VAO)
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

    def init_vbo(self, vertices):
        vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)

        vertices_np = np.array(vertices, dtype=np.float32)
        glBufferData(GL_ARRAY_BUFFER, vertices_np.nbytes, vertices_np, GL_STATIC_DRAW)

        position_loc = glGetAttribLocation(self.shader, "inPosition")
        glEnableVertexAttribArray(position_loc)
        glVertexAttribPointer(position_loc, 3, GL_FLOAT, False, 3 * sizeof(GLfloat), ctypes.c_void_p(0))

    def gl_draw(self):
        vertices = []

        for i in range(1000):
            vertices.extend([random.uniform(-1, 1), random.uniform(-1, 1), 0.0])

        self.init_vbo(vertices)

        glBindVertexArray(self.vao)
        glDrawArrays(GL_POINTS, 0, len(vertices) // 3)

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
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.gl_draw()
            self.update()
            self.fps()

        self.quit()

if __name__ == "__main__":
    App()
