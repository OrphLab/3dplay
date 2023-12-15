import pygame
import OpenGL as gl 
from OpenGL.GL import *
import OpenGL_accelerate
from OpenGL.GL.shaders import compileProgram, compileShader
import array
import random
import struct
import numpy as np
from dotpoints import DotPoints
    
class app:
    def __init__(self):
        
        # pygame stuff 
        self.screen = pygame.display.set_mode((800, 600), pygame.OPENGL | pygame.DOUBLEBUF) #openGL window (double buffer will be used, which employs two image bufers. Te pixel data from one bufer is displayed on screen while new data is being written into a second bufer
        self.clock = pygame.time.Clock()
        
        #openGL stuff
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 1) #anti-aliasing (smooth edges)
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, 4) #anti-aliasing (smooth edges)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE) #core profile (no deprecated functions) 

        self.running = True
        self.dots_list = []
        self.main_loop() 
        
    
    def update(self):
        pygame.display.flip()

    def fps(self):
        self.clock.tick(60)
    
    def quit(self):
        pygame.quit()
        quit()
        
    def main_loop(self):
        dot = DotPoints()
        dot2 = DotPoints()
        dot3 = DotPoints()
        
        while self.running:
                       
            DotPoints.draw_dots()
            self.update()

            self.fps()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

        self.quit()
    
if __name__ == "__main__":
    app()
    