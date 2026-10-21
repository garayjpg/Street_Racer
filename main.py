import pygame
import sys
import os

# Esto es vital: le dice a Python que busque archivos dentro de la carpeta 'src'
sys.path.insert(0, os.path.dirname(__file__))

from src.game import Game

def main():
    # Inicializa todos los módulos de Pygame (video, sonido, input)
    pygame.init()
    # Inicializa el mezclador de sonido para evitar retrasos en el audio
    pygame.mixer.init()
    
    # Crea la instancia principal del juego
    game = Game()
    # Arranca el bucle principal (Menu -> Juego -> Fin)
    game.run()
    
    # Si el bucle termina, cerramos todo limpiamente
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()