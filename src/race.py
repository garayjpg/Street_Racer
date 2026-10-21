import pygame
import random
from src.constants import *
from src.car import Car
from src.obstacle import Obstacle
from src.powerup import PowerUp
from src.utils import load_image
from src.sound import SoundManager

class Race:
    def __init__(self, screen, progress, player1_car="basic", player2_car="basic", player1_name="Jugador 1", player2_name="Jugador 2"):
        self.screen = screen; self.progress = progress
        self.sound_manager = SoundManager()
        self.font = pygame.font.Font(None, 80); self.font_small = pygame.font.Font(None, 48)
        self.font_game_over_title = pygame.font.Font(None, 110); self.font_winner = pygame.font.Font(None, 80)
        
        self.player1_name, self.player2_name = player1_name, player2_name
        self.player1_color = progress.get('player1_color', BLUE)
        self.player2_color = progress.get('player2_color', RED)
        
        self.player1 = Car(SCREEN_WIDTH//2-100, SCREEN_HEIGHT-250, self.player1_color, 'WASD', car_type=player1_car)
        self.player2 = Car(SCREEN_WIDTH//2+100, SCREEN_HEIGHT-250, self.player2_color, 'ARROWS', car_type=player2_car)
        
        if 'player1_lives' in progress: self.player1.lives = progress['player1_lives']; self.player2.lives = progress['player2_lives']
        
        self.obstacles = []; self.traffic_cars = []; self.powerups = []
        self.spawn_timer = 0; self.powerup_timer = 0
        self.current_track = progress.get('current_track', 0)
        self.track_theme = TRACK_THEMES[self.current_track % len(TRACK_THEMES)]
        self.road_img = load_image(self.track_theme["file"], SCREEN_WIDTH, SCREEN_HEIGHT)
        
        self.time_played = 0; self.difficulty_level = 1; self.difficulty = 1.0
        self.time_per_level = 30 * 60; self.next_level_time = self.time_per_level; self.difficulty_increase = 0.5
        self.road_offset = 0; self.score = 0; self.score_multiplier = 1.0
        self.race_finished = False; self.race_started = False; self.countdown = 3; self.countdown_timer = 0
        self.level_up_notification = False; self.level_up_timer = 0; self.reward_given = False; self.road_speed = 5

    def draw_heart_ui(self, x, y, size, color):
        img = load_image("heart.png", size, size, color)
        self.screen.blit(img, (x, y))

    def spawn_obstacle(self):
        min_x = ROAD_LEFT + 20; max_x = SCREEN_WIDTH - ROAD_RIGHT - 100
        if max_x > min_x: self.obstacles.append(Obstacle(random.randint(min_x, max_x), -100, random.choice(['cone', 'barrier'])))
    
    def spawn_traffic(self):
        min_x = ROAD_LEFT + 20; max_x = SCREEN_WIDTH - ROAD_RIGHT - 80
        if max_x > min_x:
            tc = Car(random.randint(min_x, max_x), -150, random.choice(TRAFFIC_COLORS), None, True)
            tc.traffic_speed = 4 + (self.difficulty * 0.8)
            if random.random() < 0.2 + (self.difficulty * 0.15):
                tc.traffic_lateral_movement = True; tc.lateral_direction = random.choice([-1, 1])
                tc.lateral_speed = random.uniform(1, 2 + self.difficulty * 0.4); tc.lateral_timer = random.randint(20, 60)
            self.traffic_cars.append(tc)
    
    def spawn_powerup(self): 
        min_x = ROAD_LEFT + 20; max_x = SCREEN_WIDTH - ROAD_RIGHT - 100
        if max_x > min_x: self.powerups.append(PowerUp(random.randint(min_x, max_x), -100, "health"))

    def update(self):
        if not self.race_started: return
        keys = pygame.key.get_pressed()
        if not self.race_finished:
            self.player1.update(keys, self.player2); self.player2.update(keys, self.player1)
        
        self.time_played += 1
        if self.time_played >= self.next_level_time:
            self.difficulty_level += 1; self.difficulty = 1.0 + (self.difficulty_level - 1) * self.difficulty_increase
            self.next_level_time += self.time_per_level; self.level_up_notification = True; self.level_up_timer = 180
            self.score += 1000 * self.difficulty_level; self.current_track = (self.current_track + 1) % len(TRACK_THEMES)
            self.track_theme = TRACK_THEMES[self.current_track]; self.road_img = load_image(self.track_theme["file"], SCREEN_WIDTH, SCREEN_HEIGHT)
        
        if self.level_up_notification:
            self.level_up_timer -= 1
            if self.level_up_timer <= 0: self.level_up_notification = False
        
        self.road_speed = 5 + (self.difficulty * 1.5); self.road_offset += self.road_speed
        self.score_multiplier = 1.0 + (self.difficulty - 1.0) * 0.5; self.score += int(0.5 * self.score_multiplier)
        
        spawn_rate = max(10, 55 - int(self.difficulty * 12)); self.spawn_timer += 1
        if self.spawn_timer > spawn_rate:
            self.spawn_timer = 0; r = random.random()
            if r < max(0.2, 0.5 - (self.difficulty*0.05)):
                self.spawn_obstacle()
                if random.random() < 0.9: pygame.time.wait(5); self.spawn_obstacle()
            else:
                self.spawn_traffic()
                if self.difficulty > 1.5 and random.random() < 0.6: pygame.time.wait(10); self.spawn_traffic()

        self.powerup_timer += 1
        if self.powerup_timer > min(1200, 600 + int(self.difficulty * 100)) and len(self.powerups) < 2:
            self.spawn_powerup(); self.powerup_timer = 0
        
        for o in self.obstacles[:]:
            o.speed = self.road_speed; o.update()
            if o.y > SCREEN_HEIGHT: self.obstacles.remove(o); self.score += int(10 * self.score_multiplier)
            elif not o.has_collided:
                if self.player1.check_collision(o): self.player1.apply_slowdown(o.slowdown_duration); o.has_collided=True; self.sound_manager.play_crash()
                if self.player2.check_collision(o): self.player2.apply_slowdown(o.slowdown_duration); o.has_collided=True; self.sound_manager.play_crash()
        
        for c in self.traffic_cars[:]:
            c.y += self.road_speed + c.traffic_speed
            if hasattr(c, 'traffic_lateral_movement') and c.traffic_lateral_movement:
                c.lateral_timer -= 1; c.x += c.lateral_direction * c.lateral_speed
                if c.lateral_timer <= 0: c.lateral_direction *= -1; c.lateral_timer = random.randint(20, 60)
                c.x = max(ROAD_LEFT, min(c.x, SCREEN_WIDTH-ROAD_RIGHT-c.width))
            if c.y > SCREEN_HEIGHT: self.traffic_cars.remove(c); self.score += int(20 * self.score_multiplier); continue
            if self.player1.check_collision(c):
                if self.player1.lose_life(): self.traffic_cars.remove(c); self.sound_manager.play_crash(); continue
            if self.player2.check_collision(c):
                if self.player2.lose_life(): self.traffic_cars.remove(c); self.sound_manager.play_crash(); continue
        
        for p in self.powerups[:]:
            p.speed = self.road_speed; p.update()
            if p.y > SCREEN_HEIGHT: self.powerups.remove(p)
            elif not p.collected:
                if self.player1.check_collision(p): p.collected=True; self.powerups.remove(p); self.score+=int(50*self.score_multiplier); self.player1.gain_life(); self.sound_manager.play_collect()
                elif self.player2.check_collision(p): p.collected=True; self.powerups.remove(p); self.score+=int(50*self.score_multiplier); self.player2.gain_life(); self.sound_manager.play_collect()

        if self.player1.lives <= 0 or self.player2.lives <= 0:
            self.race_finished = True
            if not self.reward_given:
                if self.player1.lives > 0: self.progress['player1_coins'] += 100
                elif self.player2.lives > 0: self.progress['player2_coins'] += 100
                self.reward_given = True

    def draw(self):
        ry = (self.time_played * self.road_speed) % SCREEN_HEIGHT
        self.screen.blit(self.road_img, (0, ry - SCREEN_HEIGHT)); self.screen.blit(self.road_img, (0, ry))
        
        for o in self.obstacles: o.draw(self.screen)
        for c in self.traffic_cars: c.draw(self.screen)
        for p in self.powerups: p.draw(self.screen)
        self.player1.draw(self.screen); self.player2.draw(self.screen)
        
        self.screen.blit(self.font_small.render(f"Pista: {self.track_theme['name']}", True, WHITE), (20, 20))
        
        p1t = self.font_small.render(f"{self.player1_name}:", True, self.player1_color)
        self.screen.blit(p1t, (20, 80))
        for i in range(self.player1.lives):
            self.draw_heart_ui(40 + p1t.get_width() + i * 45, 80, 30, self.player1_color)
        
        p2t = self.font_small.render(f"{self.player2_name}:", True, self.player2_color)
        self.screen.blit(p2t, (20, 140))
        for i in range(self.player2.lives):
            self.draw_heart_ui(40 + p2t.get_width() + i * 45, 140, 30, self.player2_color)

        level_txt = self.font_small.render(f"Nivel: {self.difficulty_level}", True, ORANGE); self.screen.blit(level_txt, (SCREEN_WIDTH - 300, 20))
        time_txt = self.font_small.render(f"Tiempo: {(self.time_played//3600):02d}:{(self.time_played//60)%60:02d}", True, YELLOW); self.screen.blit(time_txt, (SCREEN_WIDTH - 300, 70))
        
        if self.level_up_notification:
            txt = self.font.render(f"¡NIVEL {self.difficulty_level}!", True, YELLOW)
            r = txt.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2-200))
            pygame.draw.rect(self.screen, BLACK, r.inflate(20,20)); self.screen.blit(txt, r)

        if not self.race_started:
            txt = self.font.render(str(self.countdown) if self.countdown > 0 else "GO!", True, GREEN)
            self.screen.blit(txt, txt.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)))

        if self.race_finished:
            box_w, box_h = 900, 600
            gr = pygame.Rect(0, 0, box_w, box_h); gr.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
            overlay = pygame.Surface(gr.size, pygame.SRCALPHA); overlay.fill((0, 0, 0, 200)); self.screen.blit(overlay, gr.topleft)
            pygame.draw.rect(self.screen, RED, gr, 5)
            cx, cy = gr.centerx, gr.centery
            
            self.screen.blit(self.font_game_over_title.render("GAME OVER", True, RED), self.font_game_over_title.render("GAME OVER", True, RED).get_rect(center=(cx, cy-180)))
            
            win_txt = f"¡{self.player1_name} GANÓ!" if self.player1.lives > 0 else (f"¡{self.player2_name} GANÓ!" if self.player2.lives > 0 else "¡EMPATE!")
            self.screen.blit(self.font_winner.render(win_txt, True, YELLOW), self.font_winner.render(win_txt, True, YELLOW).get_rect(center=(cx, cy-60)))
            self.screen.blit(self.font_small.render("+100 Monedas", True, GREEN), self.font_small.render("+100 Monedas", True, GREEN).get_rect(center=(cx, cy+40)))
            self.screen.blit(self.font_small.render("ENTER: Reiniciar | ESC: Menú", True, LIGHT_BLUE), self.font_small.render("ENTER: Reiniciar | ESC: Menú", True, LIGHT_BLUE).get_rect(center=(cx, cy+180)))

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    self.sound_manager.stop_music() 
                    return None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11:
                        if self.screen.get_flags() & pygame.FULLSCREEN: self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                        else: self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
                    if event.key == pygame.K_ESCAPE: 
                        self.sound_manager.stop_music()
                        return {'action': 'menu', 'score': self.score}
                    elif self.race_finished and event.key == pygame.K_RETURN: 
                        self.sound_manager.stop_music()
                        return {'action': 'restart', 'score': self.score}
            
            if not self.race_started:
                self.countdown_timer += 1
                if self.countdown_timer >= 60: self.countdown_timer = 0; self.countdown -= 1
                if self.countdown < 0: self.race_started = True
            
            self.update(); self.draw(); pygame.display.flip(); clock.tick(FPS)
        return None