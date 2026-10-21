import pygame
import os

class SoundManager:
    def __init__(self):
        if not pygame.mixer.get_init():
            try: pygame.mixer.init()
            except Exception as e: print(f"Error audio: {e}"); return

        # Rutas a los archivos
        self.music_path = os.path.join("assets", "sounds", "music.mp3")
        self.crash_path = os.path.join("assets", "sounds", "crash.wav")
        self.collect_path = os.path.join("assets", "sounds", "collect.wav")
        
        # Precargar efectos cortos para que suenen al instante
        self.crash_sound = self.load_sound(self.crash_path)
        self.collect_sound = self.load_sound(self.collect_path)
        
        self.music_volume = 0.4
        self.sfx_volume = 0.6

    def load_sound(self, path):
        if os.path.exists(path):
            try: return pygame.mixer.Sound(path)
            except: return None
        return None

    def play_music(self):
        """Reproduce música en bucle (-1) si no está sonando ya"""
        if os.path.exists(self.music_path):
            try:
                if not pygame.mixer.music.get_busy():
                    pygame.mixer.music.load(self.music_path)
                    pygame.mixer.music.set_volume(self.music_volume)
                    pygame.mixer.music.play(-1)
            except Exception as e: print(f"Error música: {e}")

    def stop_music(self):
        pygame.mixer.music.stop()

    def play_crash(self):
        if self.crash_sound:
            self.crash_sound.set_volume(self.sfx_volume)
            self.crash_sound.play()

    def play_collect(self):
        if self.collect_sound:
            self.collect_sound.set_volume(self.sfx_volume)
            self.collect_sound.play()