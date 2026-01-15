"""
Module de gestion des feux tricolores
Responsable : Mbene Diagne
"""

import time
from enum import Enum
from typing import Tuple

class TrafficLightState(Enum):
    """États du feu tricolore"""
    RED = "ROUGE"
    ORANGE = "ORANGE"
    GREEN = "VERT"

class TrafficLight:
    """Représente un feu tricolore"""
    
    def __init__(self, position: Tuple[float, float]):
        pass
    
    def update(self) -> None:
        """Met à jour l'état du feu"""
        pass
    
    def get_current_state(self) -> str:
        """Retourne l'état actuel"""
        pass


if __name__ == "__main__":
    print("TrafficLight module créé")