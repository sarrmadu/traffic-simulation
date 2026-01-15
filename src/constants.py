
## **6. src/constants.py**


"""
Constantes globales pour la simulation de feu tricolore
"""

# ==================== VERSION ====================
VERSION = "1.0.0"
AUTHOR = "Équipe Simulation - Ville de Thiès"
YEAR = 2025

# ==================== DIMENSIONS ====================
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
ROAD_WIDTH = 300
INTERSECTION_SIZE = 300
LANE_WIDTH = 100
SIDEWALK_WIDTH = 20

# ==================== COULEURS ====================
# Environnement
BACKGROUND_COLOR = "#87CEEB"  # Bleu ciel
GRASS_COLOR = "#90EE90"       # Vert clair
ROAD_COLOR = "#696969"        # Gris foncé
SIDEWALK_COLOR = "#C0C0C0"    # Gris clair
MARKING_COLOR = "#FFFFFF"     # Blanc

# Feux tricolores
RED = "#FF0000"
ORANGE = "#FFA500"
GREEN = "#00FF00"
LIGHT_OFF = "#333333"

# Véhicules
CAR_COLORS = [
    "#FF0000",  # Rouge
    "#0000FF",  # Bleu
    "#008000",  # Vert foncé
    "#FFFF00",  # Jaune
    "#FFA500",  # Orange
    "#800080",  # Violet
    "#00FFFF",  # Cyan
    "#FF69B4",  # Rose
]

TRUCK_COLORS = [
    "#8B4513",  # Marron
    "#2F4F4F",  # Gris ardoise
    "#000000",  # Noir
]

# ==================== TEMPS (en secondes) ====================
# Durées des feux par scénario
TRAFFIC_LIGHT_TIMINGS = {
    "normal": {
        "green": 10,
        "orange": 3,
        "red": 8
    },
    "rush_hour": {
        "green": 15,
        "orange": 2,
        "red": 5
    },
    "night": {
        "blink_interval": 1.0
    },
    "manual": {
        "green": 10,
        "orange": 3,
        "red": 8
    }
}

# ==================== VÉHICULES ====================
VEHICLE_CONFIG = {
    "car": {
        "width": 40,
        "height": 20,
        "min_speed": 1.5,
        "max_speed": 2.5,
        "acceleration": 0.1,
        "deceleration": 0.2
    },
    "truck": {
        "width": 60,
        "height": 25,
        "min_speed": 1.0,
        "max_speed": 2.0,
        "acceleration": 0.05,
        "deceleration": 0.15
    }
}

# Taux d'apparition (probabilité par frame)
SPAWN_RATES = {
    "normal": 0.02,
    "rush_hour": 0.05,
    "night": 0.005,
    "manual": 0.02
}

# Limites de véhicules
MAX_VEHICLES = {
    "normal": 15,
    "rush_hour": 25,
    "night": 8,
    "manual": 15
}

# ==================== SIMULATION ====================
FPS = 60
UPDATE_INTERVAL = 16.67  # 1000ms / 60 FPS
SIMULATION_SPEED = 1.0

# ==================== POSITIONS ====================
# Positions des feux tricolores
TRAFFIC_LIGHT_POSITIONS = [
    (0, 200),    # Nord
    (0, -200),   # Sud
    (200, 0),    # Est
    (-200, 0)    # Ouest
]

# Départ des voies
LANE_STARTS = {
    "north": [
        (-LANE_WIDTH, -400),
        (0, -400),
        (LANE_WIDTH, -400)
    ],
    "south": [
        (-LANE_WIDTH, 400),
        (0, 400),
        (LANE_WIDTH, 400)
    ],
    "east": [
        (-400, -LANE_WIDTH),
        (-400, 0),
        (-400, LANE_WIDTH)
    ],
    "west": [
        (400, -LANE_WIDTH),
        (400, 0),
        (400, LANE_WIDTH)
    ]
}

# ==================== BASE DE DONNÉES ====================
DB_NAME = "traffic_simulation.db"
EVENTS_TABLE = "simulation_events"
STATS_TABLE = "statistics"

# ==================== INTERFACE ====================
BUTTON_COLORS = {
    "start": "#4CAF50",    # Vert
    "pause": "#FF9800",    # Orange
    "stop": "#F44336",     # Rouge
    "reset": "#2196F3",    # Bleu
    "scenario": "#9C27B0"  # Violet
}

# ==================== ÉVÉNEMENTS ====================
EVENT_TYPES = [
    "SIMULATION_START",
    "SIMULATION_PAUSE",
    "SIMULATION_STOP",
    "SIMULATION_RESET",
    "TRAFFIC_LIGHT_CHANGE",
    "VEHICLE_CREATED",
    "VEHICLE_REMOVED",
    "SCENARIO_CHANGED",
    "USER_ACTION"
]

# ==================== VÉHICULES - COMPORTEMENT ====================
# Distances de sécurité
SAFE_DISTANCE = 60      # Distance minimale entre véhicules
STOP_DISTANCE = 120     # Distance pour s'arrêter au feu rouge
SLOW_DOWN_DISTANCE = 200  # Distance pour ralentir (feu orange ou feu rouge loin)

# Autres paramètres de comportement
VEHICLE_REACTION_TIME = 0.5  # Temps de réaction (secondes)
MIN_FOLLOWING_DISTANCE = 40  # Distance de suivi minimale
MAX_FOLLOWING_DISTANCE = 100  # Distance de suivi maximale

# Probabilités
PROBABILITY_CHANGE_LANE = 0.1  # Probabilité de changer de voie
PROBABILITY_SPEED_UP = 0.3     # Probabilité d'accélérer
PROBABILITY_SLOW_DOWN = 0.2    # Probabilité de ralentir
# ==================== CHEMINS D'IMPORT ====================
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))