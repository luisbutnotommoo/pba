import pygame
from OpenGL.GLU import*
from OpenGL.GL import*
from OpenGL.GLUT import*
from pygame.locals import*
from PIL import*
import objetos as obj

class textos:
    def display_text(self, text, x, y):
        glColor3f(0, 0, 0)  # Color negro para el texto
        font = pygame.font.SysFont("Arial", 18, True)  # Tamaño de fuente reducido a 24
        lines = text.split('\n')  # Dividir el texto por líneas usando '\n'

        # Dibujar cada línea, desplazándola verticalmente
        for i, line in enumerate(lines):
                text_surface = font.render(line, True, (0, 0, 0), (255, 223, 191))
                text_data = pygame.image.tostring(text_surface, "RGBA", True)
                glWindowPos2d(x, y - i * 30)  # Ajustar el espaciado entre líneas (30 píxeles entre líneas)
                glDrawPixels(text_surface.get_width(), text_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, text_data)
