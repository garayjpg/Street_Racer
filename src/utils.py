import pygame
import os
from src.constants import *

# Caché: Guarda imágenes ya cargadas para no leer el disco duro 60 veces por segundo
image_cache = {}

def create_placeholder(name, width, height, color):
    """
    Crea un dibujo geométrico simple si no se encuentra la imagen PNG.
    Esto evita que el juego se cierre por falta de archivos.
    """
    surf = pygame.Surface((width, height))
    if "car" in name: # Dibuja algo parecido a un carro
        surf.fill(color if color else (200, 200, 200))
        pygame.draw.rect(surf, (100, 200, 255), (5, height//4, width-10, height//3))
        pygame.draw.rect(surf, (0, 0, 0), (0, 0, width, height), 2)
    elif "heart" in name: # Dibuja un cuadrado rojo
        surf.fill((0,0,0,0)); surf.set_colorkey((0,0,0))
        c = color if color else (255, 0, 0)
        pygame.draw.rect(surf, c, (width//4, width//4, width//2, width//2))
    elif "road" in name: # Dibuja asfalto genérico
        surf.fill((40, 40, 40))
        pygame.draw.rect(surf, (255, 255, 0), (width//2 - 5, 0, 10, height))
        pygame.draw.rect(surf, (255, 255, 255), (20, 0, 10, height))
        pygame.draw.rect(surf, (255, 255, 255), (width-30, 0, 10, height))
    else: # Cuadrado fucsia de error
        surf.fill(color if color else (255, 0, 255))
        pygame.draw.rect(surf, (0,0,0), (0,0,width,height), 2)
    return surf

def load_image(name, width=None, height=None, color=None):
    """
    Carga, redimensiona y tiñe una imagen.
    """
    # Generamos una clave única para guardar esta versión específica en caché
    key = f"{name}_{width}_{height}_{color}"
    if key in image_cache: return image_cache[key]
    
    path = os.path.join("assets", "images", name)
    image = None
    
    # Intentamos cargar la imagen real
    if os.path.exists(path):
        try:
            image = pygame.image.load(path).convert_alpha() # Mantiene transparencia
            if width and height: 
                image = pygame.transform.scale(image, (width, height))
            
            # Si se pide un color, tintamos la imagen (mezclamos colores)
            if color:
                colored_image = image.copy()
                color_surface = pygame.Surface(colored_image.get_size()).convert_alpha()
                color_surface.fill(color)
                # BLEND_MULT mezcla el color blanco del sprite con el color deseado
                colored_image.blit(color_surface, (0, 0), special_flags=pygame.BLEND_MULT)
                image = colored_image
        except Exception as e: print(f"Error cargando {name}: {e}")
    
    # Si falló la carga, usamos el placeholder
    if image is None:
        w = width if width else 60; h = height if height else 60
        image = create_placeholder(name, w, h, color)

    image_cache[key] = image
    return image

class DynamicBackground:
    """Maneja el fondo de carretera en movimiento para los menús"""
    def __init__(self):
        self.y = 0
        self.speed = 5
        self.timer = 0
        self.track_index = 0
        self.switch_time = 30 * 60  # Cambia cada 30 segundos
        self.current_img = self.get_current_image()
        
        # Capa oscura para que el texto del menú resalte sobre la carretera
        self.overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.overlay.fill((0, 0, 0))
        self.overlay.set_alpha(180) 

    def get_current_image(self):
        theme = TRACK_THEMES[self.track_index]
        return load_image(theme["file"], SCREEN_WIDTH, SCREEN_HEIGHT)

    def update(self):
        # Movimiento vertical infinito
        self.y += self.speed
        if self.y >= SCREEN_HEIGHT:
            self.y = 0
            
        # Lógica de cambio de tiempo
        self.timer += 1
        if self.timer >= self.switch_time:
            self.timer = 0
            self.track_index = (self.track_index + 1) % len(TRACK_THEMES)
            self.current_img = self.get_current_image()

    def draw(self, screen):
        # Dibujar dos veces la imagen para efecto "scrolling" sin huecos
        screen.blit(self.current_img, (0, self.y - SCREEN_HEIGHT))
        screen.blit(self.current_img, (0, self.y))
        screen.blit(self.overlay, (0, 0))