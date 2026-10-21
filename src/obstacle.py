import pygame
from src.constants import *
from src.utils import load_image

class Obstacle:
    def __init__(self, x, y, obs_type):
        self.x = x; self.y = y; self.obs_type = obs_type
        if obs_type == 'cone': self.width = 80; self.height = 80; self.slowdown_duration = 3
        else: self.width = 180; self.height = 50; self.color = RED; self.slowdown_duration = 8
        self.speed = 5; self.has_collided = False
    
    def get_hitbox(self):
        if self.obs_type == 'barrier': return pygame.Rect(self.x+5, self.y+15, self.width-10, self.height-30)
        else: return pygame.Rect(self.x+20, self.y+20, self.width-40, self.height-40)
    
    def update(self): self.y += self.speed
    def draw(self, screen):
        img_name = "cone.png" if self.obs_type == 'cone' else "barrier.png"
        screen.blit(load_image(img_name, self.width, self.height), (self.x, self.y))