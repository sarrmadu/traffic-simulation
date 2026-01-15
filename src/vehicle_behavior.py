"""
Module de gestion des véhicules - Partie Comportement
Responsable : Ndeye Khady Syll
"""

import random
import math
from typing import Tuple, List, Optional, Dict, Any
from enum import Enum
from constants import *

class VehicleState(Enum):
    """États possibles d'un véhicule"""
    MOVING = "moving"
    STOPPED = "stopped"
    SLOWING = "slowing"
    ACCELERATING = "accelerating"

class VehicleBehavior:
    """Gère le comportement d'un véhicule"""
    
    def __init__(self, vehicle_id: int, lane_id: int, direction: str, scenario: str = "normal"):
        """
        Initialise un véhicule comportemental
        
        Args:
            vehicle_id: ID unique du véhicule
            lane_id: ID de la voie
            direction: Direction du véhicule
            scenario: Scénario actuel
        """
        self.id = vehicle_id
        self.lane_id = lane_id
        self.direction = direction
        self.scenario = scenario
        
        # Position et vitesse
        self.position = self._get_start_position()
        self.speed = self._get_initial_speed()
        self.target_speed = self.speed
        self.acceleration = 0.1
        self.deceleration = 0.2
        
        # État
        self.state = VehicleState.MOVING
        self.is_stopped = False
        self.is_slowing = False
        self.waiting_time = 0
        self.distance_traveled = 0
        
        # Feu tricolore
        self.reacting_to_light = False
        self.light_state = None
        
        print(f"✓ Véhicule #{self.id} initialisé ({direction}, scénario: {scenario})")
    
    def _get_start_position(self) -> Tuple[float, float]:
        """Retourne la position de départ selon la direction"""
        # Positions de départ hors écran
        if self.direction == "east":
            return (-400, self._get_lane_y())
        elif self.direction == "west":
            return (400, self._get_lane_y())
        elif self.direction == "north":
            return (self._get_lane_x(), -300)
        elif self.direction == "south":
            return (self._get_lane_x(), 300)
        return (0, 0)
    
    def _get_lane_y(self) -> float:
        """Retourne la position Y selon la voie"""
        # 3 voies par direction: -50, 0, 50
        lane_positions = {-1: -50, 0: 0, 1: 50}
        return lane_positions.get(self.lane_id % 3, 0)
    
    def _get_lane_x(self) -> float:
        """Retourne la position X selon la voie"""
        # 3 voies par direction: -50, 0, 50
        lane_positions = {-1: -50, 0: 0, 1: 50}
        return lane_positions.get(self.lane_id % 3, 0)
    
    def _get_initial_speed(self) -> float:
        """Retourne la vitesse initiale selon le scénario"""
        speeds = {
            "normal": random.uniform(1.5, 2.5),
            "rush_hour": random.uniform(1.0, 1.8),
            "night": random.uniform(1.0, 1.5),
            "manual": random.uniform(1.5, 2.5)
        }
        return speeds.get(self.scenario, 2.0)
    
    def update(self, traffic_light_state: Optional[str] = None, 
               vehicles_ahead: List['VehicleBehavior'] = None) -> bool:
        """
        Met à jour la position et l'état du véhicule
        
        Returns:
            True si le véhicule est toujours actif, False s'il doit être supprimé
        """
        # Vérifier si le véhicule est sorti de l'écran
        if self._is_off_screen():
            return False
        
        # Mettre à jour la réaction au feu
        self.light_state = traffic_light_state
        
        # Ajuster la vitesse selon le feu et les autres véhicules
        self._adjust_speed(vehicles_ahead)
        
        # Mettre à jour la position
        self._move()
        
        return True
    
    def _is_off_screen(self) -> bool:
        """Vérifie si le véhicule est hors de l'écran"""
        x, y = self.position
        
        if self.direction in ["east", "west"]:
            return abs(x) > 450
        else:  # north, south
            return abs(y) > 350
    
    def _adjust_speed(self, vehicles_ahead: Optional[List['VehicleBehavior']]) -> None:
        """Ajuste la vitesse selon les conditions"""
        distance_to_intersection = self._get_distance_to_intersection()
        
        # Réinitialiser l'état de ralentissement
        self.is_slowing = False
        
        # 1. Vérifier les véhicules devant (priorité haute)
        if vehicles_ahead:
            closest = self._get_closest_vehicle_ahead(vehicles_ahead)
            if closest:
                distance = self._distance_to(closest)
                
                if distance < SAFE_DISTANCE * 0.5:  # Très proche
                    self.target_speed = max(closest.speed * 0.5, 0.5)
                    self.is_slowing = True
                    self.state = VehicleState.SLOWING
                    return
                
                elif distance < SAFE_DISTANCE:  # Proche
                    self.target_speed = closest.speed * 0.8
                    self.is_slowing = True
                    self.state = VehicleState.SLOWING
                    return
        
        # 2. Réagir au feu tricolore
        if self.light_state:
            reaction_distance = self._get_reaction_distance()
            
            if self.light_state == "ROUGE":
                if distance_to_intersection < reaction_distance * 0.3:  # Très proche du feu rouge
                    self.target_speed = 0
                    self.is_slowing = True
                    self.state = VehicleState.STOPPED
                    self.is_stopped = True
                    self.waiting_time += 1
                    return
                
                elif distance_to_intersection < reaction_distance:  # Dans zone d'arrêt
                    # Ralentir progressivement
                    slowdown_factor = distance_to_intersection / reaction_distance
                    self.target_speed = self.speed * slowdown_factor * 0.5
                    self.is_slowing = True
                    self.state = VehicleState.SLOWING
            
            elif self.light_state == "ORANGE":
                if distance_to_intersection < reaction_distance:
                    # Ralentir mais ne pas s'arrêter complètement si trop proche
                    if distance_to_intersection < reaction_distance * 0.5:
                        self.target_speed = self.speed * 0.7  # Ralentir légèrement
                    else:
                        self.target_speed = self.speed * 0.5  # Ralentir davantage
                    self.is_slowing = True
                    self.state = VehicleState.SLOWING
            
            elif self.light_state == "VERT":
                if self.is_stopped:
                    # Redémarrer progressivement
                    if distance_to_intersection > 50:
                        self.is_stopped = False
                        self.waiting_time = 0
                        self.state = VehicleState.ACCELERATING
                        self.target_speed = self._get_max_speed()
                else:
                    # Accélérer vers la vitesse max
                    self.target_speed = self._get_max_speed()
                    self.state = VehicleState.MOVING
        
        # 3. Comportement normal (pas d'obstacle, feu vert ou absent)
        if not self.is_slowing and not self.is_stopped:
            # Accélérer progressivement vers la vitesse max
            if self.speed < self._get_max_speed():
                self.target_speed = self._get_max_speed()
                self.state = VehicleState.ACCELERATING
            else:
                self.state = VehicleState.MOVING
        
        # 4. Ajustement progressif de la vitesse
        self._adjust_speed_gradually()
    
    def _get_reaction_distance(self) -> float:
        """Retourne la distance de réaction selon le scénario"""
        base_distance = 150  # Distance de base
        
        # Ajuster selon le scénario
        multipliers = {
            "normal": 1.0,
            "rush_hour": 0.8,    # Réaction plus rapide
            "night": 1.2,        # Réaction plus lente (prudence)
            "manual": 1.0
        }
        
        multiplier = multipliers.get(self.scenario, 1.0)
        return base_distance * multiplier
    
    def _adjust_speed_gradually(self) -> None:
        """Ajuste progressivement la vitesse actuelle vers la vitesse cible"""
        if self.speed < self.target_speed:
            # Accélération
            accel_rate = self.acceleration
            if self.scenario == "rush_hour":
                accel_rate *= 0.7  # Accélération plus lente
            self.speed = min(self.speed + accel_rate, self.target_speed)
        
        elif self.speed > self.target_speed:
            # Freinage
            decel_rate = self.deceleration
            if self.state == VehicleState.STOPPED:
                decel_rate *= 2  # Freinage d'urgence
            self.speed = max(self.speed - decel_rate, self.target_speed)
    def _get_closest_vehicle_ahead(self, vehicles_ahead: List['VehicleBehavior']) -> Optional['VehicleBehavior']:
        """Retourne le véhicule le plus proche devant"""
        if not vehicles_ahead:
            return None
        
        closest = None
        min_distance = float('inf')
        
        for vehicle in vehicles_ahead:
            if vehicle.direction == self.direction:
                distance = self._distance_to(vehicle)
                if distance < min_distance:
                    min_distance = distance
                    closest = vehicle
        
        return closest if min_distance < SAFE_DISTANCE * 3 else None
    
    def _distance_to(self, other: 'VehicleBehavior') -> float:
        """Calcule la distance à un autre véhicule"""
        x1, y1 = self.position
        x2, y2 = other.position
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    def _get_distance_to_intersection(self) -> float:
        """Calcule la distance jusqu'à l'intersection"""
        x, y = self.position
        
        if self.direction in ["east", "west"]:
            return abs(x)
        else:  # north, south
            return abs(y)
    
    def _get_max_speed(self) -> float:
        """Retourne la vitesse max selon le scénario"""
        max_speeds = {
            "normal": 2.5,
            "rush_hour": 1.8,
            "night": 1.5,
            "manual": 2.5
        }
        return max_speeds.get(self.scenario, 2.5)
    
    def _move(self) -> None:
        """Déplace le véhicule selon sa direction et sa vitesse"""
        x, y = self.position
        
        if self.direction == "east":
            x += self.speed
        elif self.direction == "west":
            x -= self.speed
        elif self.direction == "north":
            y += self.speed
        elif self.direction == "south":
            y -= self.speed
        
        self.position = (x, y)
        self.distance_traveled += abs(self.speed)
    
    def get_position(self) -> Tuple[float, float]:
        """Retourne la position actuelle"""
        return self.position
    
    def get_speed(self) -> float:
        """Retourne la vitesse actuelle"""
        return self.speed
    
    def get_state(self) -> VehicleState:
        """Retourne l'état actuel"""
        return self.state
    
    def is_in_intersection(self) -> bool:
        """Vérifie si le véhicule est dans l'intersection"""
        x, y = self.position
        return abs(x) < 100 and abs(y) < 100
    
    def should_be_removed(self) -> bool:
        """Vérifie si le véhicule doit être supprimé"""
        return self._is_off_screen()
    
    def is_approaching_intersection(self) -> bool:
        """Vérifie si le véhicule approche de l'intersection"""
        distance = self._get_distance_to_intersection()
        return distance < 200
    
    def should_yield(self, other_vehicle: 'VehicleBehavior') -> bool:
        """
        Détermine si ce véhicule doit céder le passage à un autre
        
        Args:
            other_vehicle: L'autre véhicule
        
        Returns:
            True si ce véhicule doit céder le passage
        """
        # Règles de priorité à l'intersection
        if not (self.is_approaching_intersection() and other_vehicle.is_approaching_intersection()):
            return False
        
        # Priorité à droite (simplifiée)
        priorities = {
            "east": 1,   # Doit céder au nord
            "west": 2,   # Doit céder au sud  
            "north": 3,  # Doit céder à l'est
            "south": 4   # Doit céder à l'ouest
        }
        
        return priorities.get(self.direction, 0) < priorities.get(other_vehicle.direction, 0)


class VehicleManagerBehavior:
    """Gère le comportement de tous les véhicules"""
    
    def __init__(self, logger=None):
        self.vehicles = {}
        self.next_id = 1
        self.logger = logger
        self.spawn_timer = 0
        self.max_vehicles = 15
        self.scenario = "normal"
        self.graphic_manager = None  # Ajouter cette ligne
        self.vehicles_spawned = 0  # Ajouter cette ligne
        
        print("✓ VehicleManagerBehavior initialisé")
    
    def set_scenario(self, scenario: str) -> None:
        """Configure les paramètres selon le scénario"""
        self.scenario = scenario
        
        # Mettre à jour les limites selon le scénario
        max_vehicles_map = {
            "normal": 15,
            "rush_hour": 25,
            "night": 8,
            "manual": 15
        }
        self.max_vehicles = max_vehicles_map.get(scenario, 15)
        
        print(f"✓ Scénario véhicules: {scenario} (max: {self.max_vehicles})")
    
    def update(self, traffic_light_state: Optional[str] = None) -> List[int]:
        """
        Met à jour tous les véhicules
        
        Returns:
            Liste des IDs des véhicules à supprimer
        """
        vehicles_to_remove = []
        
        for vehicle_id, vehicle in list(self.vehicles.items()):
            # Récupérer les véhicules devant
            vehicles_ahead = self._get_vehicles_ahead(vehicle)
            
            # Mettre à jour le véhicule
            if not vehicle.update(traffic_light_state, vehicles_ahead):
                vehicles_to_remove.append(vehicle_id)
            
            # Journaliser l'arrêt au feu rouge
            if (traffic_light_state == "ROUGE" and 
                vehicle.is_stopped and 
                vehicle.waiting_time == 1 and
                self.logger):
                self.logger.log_vehicle_event(
                    vehicle_id=vehicle_id,
                    event="ARRET_FEU_ROUGE",
                    position_x=vehicle.position[0],
                    position_y=vehicle.position[1],
                    vitesse=0,
                    etat_feu=traffic_light_state,
                    scenario=vehicle.scenario
                )
        
        # Supprimer les véhicules sortis
        for vehicle_id in vehicles_to_remove:
            self.remove_vehicle(vehicle_id)
        
        return vehicles_to_remove
    
    def _get_vehicles_ahead(self, current_vehicle: VehicleBehavior) -> List[VehicleBehavior]:
        """Retourne les véhicules devant un véhicule donné"""
        ahead = []
        
        for vehicle in self.vehicles.values():
            if (vehicle.id != current_vehicle.id and 
                vehicle.direction == current_vehicle.direction):
                
                # Vérifier si le véhicule est devant
                if self._is_vehicle_ahead(current_vehicle, vehicle):
                    ahead.append(vehicle)
        
        return ahead
    
    def _is_vehicle_ahead(self, current: VehicleBehavior, other: VehicleBehavior) -> bool:
        """Vérifie si un véhicule est devant un autre"""
        if current.direction == "east":
            return other.position[0] > current.position[0]
        elif current.direction == "west":
            return other.position[0] < current.position[0]
        elif current.direction == "north":
            return other.position[1] > current.position[1]
        elif current.direction == "south":
            return other.position[1] < current.position[1]
        return False
    
    def spawn_vehicle(self) -> Optional[int]:
        """
        Crée un nouveau véhicule
        
        Returns:
            ID du véhicule créé, ou None si limite atteinte
        """
        if len(self.vehicles) >= self.max_vehicles:
            return None
        
        # Choisir une direction aléatoire
        directions = ["east", "west", "north", "south"]
        direction = random.choice(directions)
        
        # Choisir une voie (0, 1, 2)
        lane_id = random.randint(0, 2)
        
        # Créer le véhicule
        vehicle_id = self.next_id
        self.next_id += 1
        
        vehicle = VehicleBehavior(
            vehicle_id=vehicle_id,
            lane_id=lane_id,
            direction=direction,
            scenario=self.scenario
        )
        
        self.vehicles[vehicle_id] = vehicle
        
        # Journaliser la création
        if self.logger:
            self.logger.log_vehicle_event(
                vehicle_id=vehicle_id,
                event="CREATION",
                position_x=vehicle.position[0],
                position_y=vehicle.position[1],
                vitesse=vehicle.speed,
                scenario=self.scenario
            )
        
        print(f"✓ Véhicule #{vehicle_id} apparu ({direction})")
        return vehicle_id
    
    def remove_vehicle(self, vehicle_id: int) -> bool:
        """Supprime un véhicule"""
        if vehicle_id in self.vehicles:
            vehicle = self.vehicles[vehicle_id]
            
            # Journaliser la suppression
            if self.logger:
                self.logger.log_vehicle_event(
                    vehicle_id=vehicle_id,
                    event="SUPPRESSION",
                    position_x=vehicle.position[0],
                    position_y=vehicle.position[1],
                    vitesse=vehicle.speed,
                    scenario=vehicle.scenario
                )
            
            del self.vehicles[vehicle_id]
            print(f"✓ Véhicule #{vehicle_id} supprimé")
            return True
        
        return False
    
    def get_vehicle_count(self) -> int:
        """Retourne le nombre de véhicules actifs"""
        return len(self.vehicles)
    
    def get_vehicle_positions(self) -> Dict[int, Tuple[float, float]]:
        """Retourne les positions de tous les véhicules"""
        return {vid: vehicle.position for vid, vehicle in self.vehicles.items()}
    
    def get_vehicle_directions(self) -> Dict[int, str]:
        """Retourne les directions de tous les véhicules"""
        return {vid: vehicle.direction for vid, vehicle in self.vehicles.items()}
    
    def clear_all_vehicles(self) -> None:
        """Supprime tous les véhicules"""
        for vehicle_id in list(self.vehicles.keys()):
            self.remove_vehicle(vehicle_id)


def test_vehicle_behavior():
    """Teste le comportement des véhicules"""
    print("\n=== TEST Vehicle Behavior ===")
    
    manager = VehicleManagerBehavior()
    manager.set_scenario("normal")
    
    print("\n1. Test création véhicules:")
    
    # Créer quelques véhicules
    vehicle_ids = []
    for i in range(3):
        vid = manager.spawn_vehicle()
        if vid:
            vehicle_ids.append(vid)
            vehicle = manager.vehicles[vid]
            print(f"  ✓ Véhicule #{vid}: pos={vehicle.position}, vitesse={vehicle.speed:.1f}")
    
    print(f"\n2. Test mise à jour véhicules (feu ROUGE):")
    
    # Simuler quelques updates avec feu rouge
    for i in range(5):
        removed = manager.update(traffic_light_state="ROUGE")
        
        for vid in vehicle_ids:
            if vid in manager.vehicles:
                vehicle = manager.vehicles[vid]
                print(f"  Frame {i+1}: Véhicule #{vid} - pos={vehicle.position}, vitesse={vehicle.speed:.1f}, état={vehicle.state.value}")
        
        if removed:
            print(f"  Véhicules supprimés: {removed}")
    
    print(f"\n3. Test statistiques:")
    print(f"  Nombre véhicules: {manager.get_vehicle_count()}")
    print(f"  Positions: {manager.get_vehicle_positions()}")
    
    print("\n✓ Tests Vehicle Behavior terminés")


if __name__ == "__main__":
    test_vehicle_behavior()