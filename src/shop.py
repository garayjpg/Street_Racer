import pygame
from src.constants import *
from src.button import Button
from src.utils import DynamicBackground

SHOP_COLORS = {
    "azul": {"name": "Azul", "color": BLUE, "price": 0},
    "rojo": {"name": "Rojo", "color": RED, "price": 0},
    "verde": {"name": "Verde", "color": GREEN, "price": 100},
    "amarillo": {"name": "Amarillo", "color": YELLOW, "price": 100},
    "morado": {"name": "Morado", "color": PURPLE, "price": 200},
    "rosa": {"name": "Rosa", "color": PINK, "price": 200},
    "cyan": {"name": "Cyan", "color": CYAN, "price": 300},
    "naranja": {"name": "Naranja", "color": ORANGE, "price": 300},
    "negro": {"name": "Negro", "color": BLACK, "price": 500},
}

class Shop:
    def __init__(self, screen, progress, player1_name, player2_name):
        self.screen = screen; self.progress = progress
        self.player1_name, self.player2_name = player1_name, player2_name
        self.font_title = pygame.font.Font(None, 100); self.font_text = pygame.font.Font(None, 50); self.font_small = pygame.font.Font(None, 36)
        
        self.bg = DynamicBackground()
        
        if 'player1_owned_colors' not in self.progress: self.progress['player1_owned_colors'] = ['azul', 'rojo']
        if 'player2_owned_colors' not in self.progress: self.progress['player2_owned_colors'] = ['azul', 'rojo']
        
        self.color_buttons = []
        y_start = 280; spacing_y = 80; col1_x = SCREEN_WIDTH*0.25 - 225; col2_x = SCREEN_WIDTH*0.75 - 225
        for i, (cid, cdata) in enumerate(SHOP_COLORS.items()):
            x = col1_x if i%2==0 else col2_x; y = y_start + (i//2)*spacing_y
            btn = Button(x, y, 450, 65, "", GRAY)
            btn.color_id = cid; btn.price = cdata['price']; btn.actual_color = cdata['color']; btn.owned = False
            self.color_buttons.append(btn)
        
        self.back_button = Button(SCREEN_WIDTH//2-150, SCREEN_HEIGHT-100, 300, 60, "VOLVER", GRAY)
        self.selected_player = 1; self.message = ""; self.message_timer = 0

    def draw_color_preview_square(self, x, y, color, size=60):
        pygame.draw.rect(self.screen, color, (x, y, size, size)); pygame.draw.rect(self.screen, WHITE, (x, y, size, size), 3)

    def run(self):
        clock = pygame.time.Clock()
        while True:
            self.bg.update(); self.bg.draw(self.screen)
            p1_curr = self.progress.get('player1_color', BLUE); p2_curr = self.progress.get('player2_color', RED)
            
            if self.selected_player == 1:
                coins = self.progress.get('player1_coins', 0); name = self.player1_name; col = p1_curr; owned = self.progress['player1_owned_colors']
            else:
                coins = self.progress.get('player2_coins', 0); name = self.player2_name; col = p2_curr; owned = self.progress['player2_owned_colors']

            for btn in self.color_buttons:
                if btn.color_id in owned: btn.owned = True; btn.text = f"{SHOP_COLORS[btn.color_id]['name']} - COMPRADO"; btn.color = GRAY
                else: btn.owned = False; btn.text = f"{SHOP_COLORS[btn.color_id]['name']} - {btn.price} $"; btn.color = btn.actual_color

            title = self.font_title.render("TIENDA", True, WHITE)
            self.screen.blit(title, title.get_rect(center=(SCREEN_WIDTH//2, 60)))
            self.screen.blit(self.font_text.render(f"Monedas de {name}: {coins}", True, YELLOW), (SCREEN_WIDTH//2-200, 120))
            self.screen.blit(self.font_text.render(f"Comprando para: {name}", True, col), (SCREEN_WIDTH//2-200, 180))
            self.screen.blit(self.font_small.render("(TAB para cambiar jugador)", True, WHITE), (SCREEN_WIDTH//2-150, 220))
            
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT: return 'quit'
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: return 'menu'
                    elif event.key == pygame.K_TAB: self.selected_player = 2 if self.selected_player == 1 else 1
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for btn in self.color_buttons:
                        if btn.is_clicked(mouse_pos):
                            if not btn.owned:
                                if coins >= btn.price:
                                    if self.selected_player==1: self.progress['player1_coins']-=btn.price; self.progress['player1_owned_colors'].append(btn.color_id)
                                    else: self.progress['player2_coins']-=btn.price; self.progress['player2_owned_colors'].append(btn.color_id)
                                    self.message="¡Comprado!"; self.message_timer=120
                                else: self.message="¡Sin fondos!"; self.message_timer=120
                            else:
                                if self.selected_player==1: self.progress['player1_color']=btn.actual_color
                                else: self.progress['player2_color']=btn.actual_color
                                self.message="¡Equipado!"; self.message_timer=120
                    if self.back_button.is_clicked(mouse_pos): return 'menu'

            for btn in self.color_buttons:
                eq = (self.selected_player==1 and btn.actual_color==p1_curr) or (self.selected_player==2 and btn.actual_color==p2_curr)
                btn.draw(self.screen, mouse_pos, eq)
                if btn.owned:
                    px = btn.rect.x - 50 if btn.rect.x < SCREEN_WIDTH//2 else btn.rect.right + 10
                    self.draw_color_preview_square(px, btn.rect.y + 5, btn.actual_color, 40)
            
            self.back_button.draw(self.screen, mouse_pos)
            py = SCREEN_HEIGHT - 100
            self.screen.blit(self.font_small.render(f"Actual {self.player1_name}", True, WHITE), (100, py-30))
            self.draw_color_preview_square(100, py, p1_curr, 60)
            self.screen.blit(self.font_small.render(f"Actual {self.player2_name}", True, WHITE), (SCREEN_WIDTH-250, py-30))
            self.draw_color_preview_square(SCREEN_WIDTH-160, py, p2_curr, 60)
            
            if self.message_timer > 0:
                self.message_timer -= 1
                mtxt = self.font_text.render(self.message, True, GREEN if "!" in self.message else RED)
                pygame.draw.rect(self.screen, BLACK, mtxt.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT-200)).inflate(20,10))
                self.screen.blit(mtxt, mtxt.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT-200)))
            pygame.display.flip(); clock.tick(FPS)