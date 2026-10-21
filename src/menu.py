import pygame
from src.constants import *
from src.button import Button
from src.utils import DynamicBackground

class Menu:
    def __init__(self, screen, progress):
        self.screen = screen; self.progress = progress
        self.font_title = pygame.font.Font(None, 120); self.font_text = pygame.font.Font(None, 50); self.font_small = pygame.font.Font(None, 36)
        
        self.bg = DynamicBackground()
        
        btn_w = 400; btn_h = 70; sp = 90; start_y = 550
        self.buttons = [
            Button(SCREEN_WIDTH//2 - btn_w//2, start_y, btn_w, btn_h, "CARRERA", GREEN),
            Button(SCREEN_WIDTH//2 - btn_w//2, start_y + sp, btn_w, btn_h, "GARAJE", BLUE),
            Button(SCREEN_WIDTH//2 - btn_w//2, start_y + sp*2, btn_w, btn_h, "TIENDA", YELLOW),
            Button(SCREEN_WIDTH//2 - btn_w//2, start_y + sp*3, btn_w, btn_h, "SALIR", RED)
        ]
        self.selected_button = 0
        self.player1_name = "Jugador 1"; self.player2_name = "Jugador 2"
        self.editing_name = None; self.temp_name = ""
        
        self.name_button_p1 = Button(SCREEN_WIDTH//2 - 370, 320, 350, 50, self.player1_name, BLUE)
        self.name_button_p2 = Button(SCREEN_WIDTH//2 + 20, 320, 350, 50, self.player2_name, RED)
    
    def get_player_names(self): return self.player1_name, self.player2_name
    
    def run(self):
        clock = pygame.time.Clock()
        while True:
            self.bg.update(); self.bg.draw(self.screen)
            
            p1_col = self.progress.get('player1_color', BLUE); p2_col = self.progress.get('player2_color', RED)
            self.name_button_p1.color = p1_col; self.name_button_p2.color = p2_col
            
            title = self.font_title.render("STREET RACERS 2D", True, WHITE)
            self.screen.blit(title, title.get_rect(center=(SCREEN_WIDTH//2, 100)))
            self.screen.blit(self.font_text.render("Multijugador Local", True, YELLOW), (SCREEN_WIDTH//2-150, 150))
            self.screen.blit(self.font_small.render("Haz clic para editar nombres:", True, LIGHT_BLUE), (SCREEN_WIDTH//2-180, 280))
            
            # Mostrar texto en tiempo real mientras se edita
            self.name_button_p1.text = (self.temp_name + "|") if self.editing_name=='p1' else self.player1_name
            self.name_button_p2.text = (self.temp_name + "|") if self.editing_name=='p2' else self.player2_name
            
            mouse_pos = pygame.mouse.get_pos()
            self.name_button_p1.draw(self.screen, mouse_pos, self.editing_name=='p1')
            self.name_button_p2.draw(self.screen, mouse_pos, self.editing_name=='p2')
            
            self.screen.blit(self.font_title.render("P1", True, p1_col), (self.name_button_p1.rect.x - 100, 320))
            self.screen.blit(self.font_title.render("P2", True, p2_col), (self.name_button_p2.rect.right + 20, 320))
            
            if self.editing_name: self.screen.blit(self.font_small.render("Escribe y ENTER", True, GREEN), (SCREEN_WIDTH//2-100, 390))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT: return 'quit'
                if self.editing_name:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            if self.temp_name.strip():
                                if self.editing_name=='p1': self.player1_name = self.temp_name[:12]
                                else: self.player2_name = self.temp_name[:12]
                            self.editing_name = None
                        elif event.key == pygame.K_ESCAPE: self.editing_name = None
                        elif event.key == pygame.K_BACKSPACE: self.temp_name = self.temp_name[:-1]
                        elif event.unicode.isprintable() and len(self.temp_name) < 12: self.temp_name += event.unicode
                else:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_DOWN: self.selected_button = (self.selected_button+1)%4
                        elif event.key == pygame.K_UP: self.selected_button = (self.selected_button-1)%4
                        elif event.key == pygame.K_RETURN: return ['race','garage','shop','quit'][self.selected_button]
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.name_button_p1.is_clicked(mouse_pos): self.editing_name='p1'; self.temp_name=self.player1_name
                        elif self.name_button_p2.is_clicked(mouse_pos): self.editing_name='p2'; self.temp_name=self.player2_name
                        else:
                            for i,b in enumerate(self.buttons):
                                if b.is_clicked(mouse_pos): return ['race','garage','shop','quit'][i]

            for i,b in enumerate(self.buttons): b.draw(self.screen, mouse_pos, i==self.selected_button and not self.editing_name)
            pygame.display.flip(); clock.tick(FPS)