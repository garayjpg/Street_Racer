# --- CONFIGURACIÓN DE PANTALLA ---
SCREEN_WIDTH = 1920  # Ancho Full HD
SCREEN_HEIGHT = 1080 # Alto Full HD
FPS = 60             # Fotogramas por segundo

# --- LÍMITES DE LA CARRETERA (Física) ---
# Estos valores definen las paredes invisibles a los lados de la pista.
# 620px de margen significa que la pista es estrecha y centrada.
ROAD_LEFT = 620
ROAD_RIGHT = 620

# --- COLORES (Formato RGB) ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 50, 50)
GREEN = (50, 200, 50)
BLUE = (50, 100, 220)
YELLOW = (255, 220, 0)
ORANGE = (255, 140, 0)
GRAY = (100, 100, 100)
DARK_GRAY = (40, 40, 40)
LIGHT_BLUE = (150, 200, 255)
PURPLE = (150, 50, 200)
PINK = (255, 100, 150)
CYAN = (0, 200, 200)

# --- TEMAS DE PISTAS ---
# Define qué imagen y colores usar en cada nivel.
TRACK_THEMES = [
    {"name": "Ciudad",          "file": "road_city.png",      "line": YELLOW, "border": WHITE},
    {"name": "Desierto",        "file": "road_desert.png",    "line": WHITE,  "border": ORANGE},
    {"name": "Nieve",           "file": "road_snow.png",      "line": BLUE,   "border": CYAN},
    {"name": "Bosque",          "file": "road_forest.png",    "line": YELLOW, "border": GREEN},
    {"name": "Atardecer",       "file": "road_sunset.png",    "line": ORANGE, "border": PINK},
    {"name": "Cyberpunk",       "file": "road_cyberpunk.png", "line": CYAN,   "border": PURPLE},
]

# Colores posibles para los carros enemigos (tráfico)
TRAFFIC_COLORS = [GRAY, (80, 80, 80), (120, 120, 120), (60, 60, 80), (80, 60, 60)]

# --- ESTADÍSTICAS DE CARROS ---
# Define la velocidad y manejo de cada tipo de vehículo
CAR_TYPES = {
    "basic": {"name": "Sedán Básico", "max_speed": 180, "acceleration": 0.5, "turn_speed": 8, "price": 0},
    "sport": {"name": "Deportivo", "max_speed": 220, "acceleration": 0.7, "turn_speed": 10, "price": 500},
    "racing": {"name": "Fórmula 1", "max_speed": 280, "acceleration": 1.0, "turn_speed": 12, "price": 1500}
}