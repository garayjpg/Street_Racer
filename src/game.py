import pygame
import json
import os
from src.menu import Menu
from src.race import Race
from src.garage import Garage
from src.shop import Shop
from src.constants import *
from src.sound import SoundManager

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Street Racers 2D")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Iniciar música globalmente aquí
        self.sound_manager = SoundManager()
        self.sound_manager.play_music()
        
        self.load_progress()
        self.menu = Menu(self.screen, self.progress)
        self.race = None
    
    def load_progress(self):
        # MODO ARCADE: Reseteamos los datos cada vez que se abre el juego
        self.progress = self.create_default_progress()
        self.save_progress()
    
    def create_default_progress(self):
        return {
            # Monedas separadas por jugador
            'coins': 0, 'player1_coins': 0, 'player2_coins': 0,
            'experience': 0,
            'unlocked_cars': ['basic', 'sport', 'racing'],
            'unlocked_tracks': ['city'],
            'car_upgrades': {},
            'owned_cars': ['basic', 'sport', 'racing'],
            'player1_car': 'basic', 'player2_car': 'basic',
            'current_track': 0,
            'player1_lives': 3, 'player2_lives': 3,
            'player1_color': BLUE, 'player2_color': RED,
            # Inventarios de colores separados
            'player1_owned_colors': ['azul', 'rojo'],
            'player2_owned_colors': ['azul', 'rojo']
        }
    
    def save_progress(self):
        os.makedirs('data', exist_ok=True)
        with open('data/progress.json', 'w') as f:
            json.dump(self.progress, f, indent=4)
    
    def reset_game(self):
        # Reinicia solo nivel y vidas, NO monedas
        print("🔄 Reiniciando partida...")
        self.progress['current_track'] = 0
        self.progress['player1_lives'] = 3
        self.progress['player2_lives'] = 3
        self.save_progress()
    
    def run(self):
        # Bucle principal de estados
        while self.running:
            action = self.menu.run()
            self.screen = self.menu.screen
            
            if action == 'quit':
                self.running = False
            
            elif action == 'race':
                self.reset_game()
                player1_name, player2_name = self.menu.get_player_names()
                p1_car = self.progress.get('player1_car', 'basic')
                p2_car = self.progress.get('player2_car', 'basic')
                
                racing = True
                while racing:
                    self.race = Race(self.screen, self.progress, p1_car, p2_car, player1_name, player2_name)
                    result = self.race.run()
                    if result:
                        if result['action'] == 'restart': self.reset_game(); racing = False 
                        elif result['action'] == 'menu': self.reset_game(); racing = False
                    else: racing = False
            
            elif action == 'garage':
                player1_name, player2_name = self.menu.get_player_names()
                garage = Garage(self.screen, self.progress, player1_name, player2_name)
                if garage.run() == 'quit': self.running = False
                self.save_progress()
            
            elif action == 'shop':
                player1_name, player2_name = self.menu.get_player_names()
                shop = Shop(self.screen, self.progress, player1_name, player2_name)
                if shop.run() == 'quit': self.running = False
                self.save_progress()
            
            self.clock.tick(FPS)