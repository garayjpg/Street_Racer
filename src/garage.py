import pygame
from src.constants import *
from src.button import Button
from src.utils import load_image, DynamicBackground

class Garage:
    def __init__(self, screen, progress, player1_name, player2_name):
        self.screen = screen; self.progress = progress
        self.player1_name, self.player2_name = player1_name, player2_name
        self.font_title = pygame.font.Font(None, 100); self.font_text = pygame.font.Font(None, 50); self.font_small = pygame.font.Font(None, 36)
        
        self.bg = DynamicBackground()
        self.player1_car = progress.get('player1_car', 'basic'); self.player2_car = progress.get('player2_car', 'basic')
        
        self.car_buttons = []
        y_start = 300; spacing = 90
        for i, (cid, cdata) in enumerate(CAR_TYPES.items()):
            btn = Button(SCREEN_WIDTH//2 - 250, y_start + i * spacing, 500, 70, cdata['name'], GRAY)
            btn.car_id = cid; self.car_buttons.append(btn)
        
        self.back_button = Button(SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT - 120, 300, 70, "VOLVER AL MENÚ", GRAY)
        self.selected_player = 1
    
    def draw_car_preview(self, x, y, car_type, color):
        img_name = "car_basic.png"
        if car_type == 'sport': img_name = "car_sport.png"
        elif car_type == 'racing': img_name = "car_racing.png"
        car_img = load_image(img_name, 80, 140, color)
        self.screen.blit(car_img, (x, y))

    def run(self):
        clock = pygame.time.Clock()
        while True:
            self.bg.update(); self.bg.draw(self.screen)
            p1_col = self.progress.get('player1_color', BLUE); p2_col = self.progress.get('player2_color', RED)
            act_name = self.player1_name if self.selected_player == 1 else self.player2_name
            act_col = p1_col if self.selected_player == 1 else p2_col
            
            for btn in self.car_buttons: btn.color = act_col
            
            title = self.font_title.render("GARAJE", True, WHITE)
            self.screen.blit(title, title.get_rect(center=(SCREEN_WIDTH//2, 80)))
            self.screen.blit(self.font_text.render(f"Configurando a: {act_name}", True, act_col), (SCREEN_WIDTH//2-200, 150))
            self.screen.blit(self.font_small.render("(TAB para cambiar jugador)", True, WHITE), (SCREEN_WIDTH//2-150, 190))
            
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT: return 'quit'
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_TAB: self.selected_player = 2 if self.selected_player == 1 else 1
                    elif event.key == pygame.K_ESCAPE: return 'menu'
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for btn in self.car_buttons:
                        if btn.is_clicked(mouse_pos):
                            if self.selected_player == 1: self.player1_car = btn.car_id; self.progress['player1_car'] = btn.car_id
                            else: self.player2_car = btn.car_id; self.progress['player2_car'] = btn.car_id
                    if self.back_button.is_clicked(mouse_pos): return 'menu'
            
            for btn in self.car_buttons:
                curr = self.player1_car if self.selected_player == 1 else self.player2_car
                btn.draw(self.screen, mouse_pos, btn.car_id == curr)
            self.back_button.draw(self.screen, mouse_pos)
            
            py = 650
            p1_x = SCREEN_WIDTH * 0.25
            self.screen.blit(self.font_text.render(self.player1_name, True, p1_col), (p1_x, py-40))
            self.draw_car_preview(p1_x, py, self.player1_car, p1_col)
            if self.selected_player == 1: pygame.draw.polygon(self.screen, YELLOW, [(p1_x+40, py-60), (p1_x+30, py-80), (p1_x+50, py-80)])
            
            p2_x = SCREEN_WIDTH * 0.75
            self.screen.blit(self.font_text.render(self.player2_name, True, p2_col), (p2_x, py-40))
            self.draw_car_preview(p2_x, py, self.player2_car, p2_col)
            if self.selected_player == 2: pygame.draw.polygon(self.screen, YELLOW, [(p2_x+40, py-60), (p2_x+30, py-80), (p2_x+50, py-80)])
            
            pygame.display.flip(); clock.tick(FPS)