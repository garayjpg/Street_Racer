import pygame
from src.constants import *
from src.utils import load_image

class Car:
    def __init__(self, x, y, color, controls, is_traffic=False, car_type="basic"):
        self.x = x; self.y = y; self.width = 70; self.height = 120
        self.hitbox_margin_x = 15; self.hitbox_margin_y = 15
        self.color = color; self.controls = controls; self.is_traffic = is_traffic; self.car_type = car_type
        stats = {"max_speed": 5, "acceleration": 0, "turn_speed": 0} if is_traffic else CAR_TYPES[car_type]
        self.speed = 0; self.turn_speed = stats["turn_speed"] if not is_traffic else 0
        self.lives = 3; self.invulnerable = False; self.invulnerable_timer = 0; self.invulnerable_duration = 120
        self.slowdown_active = False; self.slowdown_timer = 0; self.slowdown_duration = 0
        self.vertical_speed = 0; self.prev_x = x; self.prev_y = y; self.traffic_speed = 0

    def get_hitbox(self):
        return pygame.Rect(self.x+self.hitbox_margin_x, self.y+self.hitbox_margin_y, self.width-(self.hitbox_margin_x*2), self.height-(self.hitbox_margin_y*2))

    def update(self, keys, other=None):
        self.prev_x = self.x; self.prev_y = self.y
        if self.invulnerable: self.invulnerable_timer -= 1; 
        if self.invulnerable_timer <= 0: self.invulnerable = False
        if self.slowdown_active: self.slowdown_timer -= 1; 
        if self.slowdown_timer <= 0: self.slowdown_active = False
        
        if not self.is_traffic and self.controls:
            tsp = self.turn_speed * (0.4 if self.slowdown_active else 1.0)
            vsp = 6 * (0.4 if self.slowdown_active else 1.0)
            if self.controls == 'WASD':
                if keys[pygame.K_a]: self.x -= tsp
                if keys[pygame.K_d]: self.x += tsp
                if keys[pygame.K_w]: self.vertical_speed = -vsp
                elif keys[pygame.K_s]: self.vertical_speed = vsp
                else: self.vertical_speed = 0
            elif self.controls == 'ARROWS':
                if keys[pygame.K_LEFT]: self.x -= tsp
                if keys[pygame.K_RIGHT]: self.x += tsp
                if keys[pygame.K_UP]: self.vertical_speed = -vsp
                elif keys[pygame.K_DOWN]: self.vertical_speed = vsp
                else: self.vertical_speed = 0
            self.y += self.vertical_speed
            self.x = max(ROAD_LEFT-5, min(self.x, SCREEN_WIDTH-ROAD_RIGHT-self.width+5))
            self.y = max(50, min(self.y, SCREEN_HEIGHT-self.height-10))
            if other and self.check_collision(other): self.x = self.prev_x; self.y = self.prev_y

    def lose_life(self):
        if not self.invulnerable: self.lives -= 1; self.invulnerable = True; self.invulnerable_timer = 120; return True
        return False
    def gain_life(self):
        if self.lives < 5: self.lives += 1; return True
        return False
    def apply_slowdown(self, dur): self.slowdown_active = True; self.slowdown_timer = dur * 60; self.slowdown_duration = dur * 60
    
    def draw(self, screen):
        name = "car_basic.png"
        if self.car_type == 'sport': name = "car_sport.png"
        elif self.car_type == 'racing': name = "car_racing.png"
        col = self.color
        if self.invulnerable and (self.invulnerable_timer // 10) % 2 == 0: col = (255, 255, 255)
        screen.blit(load_image(name, self.width, self.height, col), (self.x, self.y))
        if self.slowdown_active:
            pygame.draw.rect(screen, RED, (self.x, self.y - 15, self.width, 8))
            pygame.draw.rect(screen, ORANGE, (self.x, self.y - 15, int(self.width * (self.slowdown_timer/self.slowdown_duration)), 8))
            
    def check_collision(self, other):
        my_rect = self.get_hitbox()
        if isinstance(other, Car): other_rect = other.get_hitbox()
        else: other_rect = pygame.Rect(other.x+15, other.y+15, other.width-30, other.height-30)
        return my_rect.colliderect(other_rect)