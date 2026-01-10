"""
Module de gestion des scénarios de circulation
Responsable : Ndeye Khady Syll
"""

from enum import Enum
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod
from constants import *

class ScenarioType(Enum):
    """
    Types de scénarios disponibles
    """
    NORMAL = "normal"
    RUSH_HOUR = "rush_hour"
    NIGHT = "night"
    MANUAL = "manual"

class Scenario(ABC):
    """
    Classe abstraite pour les scénarios
    """
    
    def __init__(self, name: ScenarioType):
        """
        Initialise un scénario
        """
        pass
    
    @abstractmethod
    def apply_traffic_light_settings(self, traffic_light) -> None:
        """
        Applique les paramètres du scénario aux feux
        """
        pass
    
    @abstractmethod
    def apply_vehicle_settings(self, vehicle_manager) -> None:
        """
        Applique les paramètres du scénario aux véhicules
        """
        pass
    
    @abstractmethod
    def get_spawn_rate(self) -> float:
        """
        Retourne le taux d'apparition des véhicules
        """
        pass
    
    @abstractmethod
    def get_max_vehicles(self) -> int:
        """
        Retourne le nombre maximum de véhicules
        """
        pass


class NormalScenario(Scenario):
    """
    Scénario de circulation normale
    """
    
    def __init__(self):
        """
        Initialise le scénario normal
        """
        pass


class RushHourScenario(Scenario):
    """
    Scénario heure de pointe
    """
    
    def __init__(self):
        """
        Initialise le scénario heure de pointe
        """
        pass


class NightScenario(Scenario):
    """
    Scénario mode nuit
    """
    
    def __init__(self):
        """
        Initialise le scénario nuit
        """
        pass


class ManualScenario(Scenario):
    """
    Scénario mode manuel
    """
    
    def __init__(self):
        """
        Initialise le scénario manuel
        """
        pass


class ScenarioManager:
    """
    Gère les différents scénarios de circulation
    """
    
    def __init__(self, logger=None):
        """
        Initialise le gestionnaire de scénarios
        """
        pass
    
    def setup(self) -> None:
        """
        Configure le gestionnaire
        """
        pass
    
    def change_scenario(self, scenario_type: ScenarioType) -> bool:
        """
        Change le scénario actuel
        """
        pass
    
    def get_current_scenario(self) -> Scenario:
        """
        Retourne le scénario actuel
        """
        pass
    
    def get_current_scenario_name(self) -> str:
        """
        Retourne le nom du scénario actuel
        """
        pass
    
    def apply_current_scenario(self, traffic_light, vehicle_manager) -> None:
        """
        Applique le scénario actuel aux composants
        """
        pass


if __name__ == "__main__":
    pass