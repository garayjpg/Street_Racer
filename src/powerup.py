import pygame
from src.constants import *
from src.utils import load_image

class PowerUp:
    def __init__(self, x, y, p_type="health"):
        self.x = x; self.y = y; self.width = 100; self.height = 100
        self.powerup_type = p_type; self.speed = 5; self.collected = False
        self.pulse = 0; self.pulse_speed = 0.1
    
    def update(self):
        self.y += self.speed; self.pulse += self.pulse_speed
        if self.pulse > 1 or self.pulse < 0: self.pulse_speed *= -1
    
    def draw(self, screen):
        if self.powerup_type == "health":
            sz = int(100 + self.pulse * 15); off = (sz - 100) // 2
            img = load_image("heart.png", sz, sz, GREEN) # Se pinta de verde en la pista
            screen.blit(img, (self.x - off, self.y - off))