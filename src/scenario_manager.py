"""
Module de gestion des scénarios de circulation
Responsable : Ndeye Khady Syll
"""

from enum import Enum
from typing import Dict, Any

class ScenarioType(Enum):
    """Types de scénarios disponibles"""
    NORMAL = "normal"
    RUSH_HOUR = "rush_hour"
    NIGHT = "night"
    MANUAL = "manual"

class Scenario:
    """Classe de base pour un scénario"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.traffic_light_durations = {}
        self.vehicle_settings = {}
    
    def get_traffic_light_durations(self) -> Dict[str, float]:
        """Retourne les durées des feux"""
        return self.traffic_light_durations
    
    def get_vehicle_settings(self) -> Dict[str, Any]:
        """Retourne les paramètres des véhicules"""
        return self.vehicle_settings
    
    def __str__(self) -> str:
        return f"Scénario {self.name}: {self.description}"

class NormalScenario(Scenario):
    """Scénario de circulation normale"""
    
    def __init__(self):
        super().__init__(
            name="Circulation Normale",
            description="Comportement standard pour une journée typique"
        )
        # Durées en secondes
        self.traffic_light_durations = {
            "green": 10,
            "orange": 3,
            "red": 8
        }
        # Paramètres véhicules
        self.vehicle_settings = {
            "spawn_rate": 0.02,  # Probabilité par frame
            "max_vehicles": 15,
            "min_speed": 1.5,
            "max_speed": 2.5
        }

class RushHourScenario(Scenario):
    """Scénario heure de pointe"""
    
    def __init__(self):
        super().__init__(
            name="Heure de Pointe",
            description="Trafic dense, feux adaptés pour fluidité"
        )
        self.traffic_light_durations = {
            "green": 15,  # Vert prolongé
            "orange": 2,  # Orange réduit
            "red": 5      # Rouge raccourci
        }
        self.vehicle_settings = {
            "spawn_rate": 0.05,
            "max_vehicles": 25,
            "min_speed": 1.0,
            "max_speed": 1.8
        }

class NightScenario(Scenario):
    """Scénario mode nuit"""
    
    def __init__(self):
        super().__init__(
            name="Mode Nuit",
            description="Faible circulation, feu orange clignotant"
        )
        self.traffic_light_durations = {
            "blink_interval": 1.0  # Clignotement chaque seconde
        }
        self.vehicle_settings = {
            "spawn_rate": 0.005,
            "max_vehicles": 8,
            "min_speed": 1.2,
            "max_speed": 2.0
        }

class ManualScenario(Scenario):
    """Scénario mode manuel"""
    
    def __init__(self):
        super().__init__(
            name="Mode Manuel",
            description="Contrôle complet par l'utilisateur"
        )
        self.traffic_light_durations = {
            "green": 10,
            "orange": 3,
            "red": 8
        }
        self.vehicle_settings = {
            "spawn_rate": 0.02,
            "max_vehicles": 15,
            "min_speed": 1.5,
            "max_speed": 2.5
        }

class ScenarioManager:
    """Gère les différents scénarios de circulation"""
    
    def __init__(self):
        self.scenarios = {}
        self.current_scenario = None
        self.previous_scenario = None
        self._initialize_scenarios()
    
    def _initialize_scenarios(self) -> None:
        """Initialise les 4 scénarios"""
        self.scenarios = {
            ScenarioType.NORMAL: NormalScenario(),
            ScenarioType.RUSH_HOUR: RushHourScenario(),
            ScenarioType.NIGHT: NightScenario(),
            ScenarioType.MANUAL: ManualScenario()
        }
        # Par défaut : scénario normal
        self.current_scenario = self.scenarios[ScenarioType.NORMAL]
        print("✓ Scénarios initialisés")
    
    def change_scenario(self, scenario_type: ScenarioType) -> bool:
        """Change le scénario actuel"""
        if scenario_type in self.scenarios:
            self.previous_scenario = self.current_scenario
            self.current_scenario = self.scenarios[scenario_type]
            print(f"✓ Scénario changé: {self.previous_scenario.name} → {self.current_scenario.name}")
            return True
        return False
    
    def get_current_scenario(self) -> Scenario:
        """Retourne le scénario actuel"""
        return self.current_scenario
    
    def get_current_scenario_name(self) -> str:
        """Retourne le nom du scénario actuel"""
        return self.current_scenario.name
    
    def get_scenario_names(self) -> Dict[ScenarioType, str]:
        """Retourne tous les noms de scénarios"""
        return {sc_type: scenario.name for sc_type, scenario in self.scenarios.items()}
    
    def get_traffic_light_durations(self) -> Dict[str, float]:
        """Retourne les durées des feux pour le scénario actuel"""
        return self.current_scenario.get_traffic_light_durations()
    
    def get_vehicle_settings(self) -> Dict[str, Any]:
        """Retourne les paramètres véhicules pour le scénario actuel"""
        return self.current_scenario.get_vehicle_settings()


def test_scenario_manager():
    """Teste le module ScenarioManager"""
    print("\n=== TEST ScenarioManager ===")
    
    manager = ScenarioManager()
    
    # Afficher le scénario courant
    print(f"Scénario initial: {manager.get_current_scenario_name()}")
    print(f"Durées feux: {manager.get_traffic_light_durations()}")
    print(f"Paramètres véhicules: {manager.get_vehicle_settings()}")
    
    # Tester changement de scénario
    print("\n--- Test changement scénario ---")
    for scenario_type in ScenarioType:
        success = manager.change_scenario(scenario_type)
        if success:
            print(f"✓ Changé vers: {manager.get_current_scenario_name()}")
            print(f"  Durées: {manager.get_traffic_light_durations()}")
        else:
            print(f"✗ Échec: {scenario_type}")
    
    print("\n✓ Tests ScenarioManager terminés")


if __name__ == "__main__":
    test_scenario_manager()