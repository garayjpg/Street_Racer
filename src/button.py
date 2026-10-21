import pygame
from src.constants import *

class Button:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.font = pygame.font.Font(None, 40)
    
    def draw(self, screen, mouse_pos, is_selected=False):
        # Si el mouse está encima o está seleccionado con teclado, brilla
        if self.rect.collidepoint(mouse_pos) or is_selected:
            hover_color = tuple(min(c + 30, 255) for c in self.color)
            pygame.draw.rect(screen, hover_color, self.rect)
            pygame.draw.rect(screen, WHITE, self.rect, 4) # Borde blanco
        else:
            pygame.draw.rect(screen, self.color, self.rect)
            pygame.draw.rect(screen, BLACK, self.rect, 2) # Borde negro
        
        # Renderizar texto centrado
        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)