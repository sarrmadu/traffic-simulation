"""
Module principal de simulation
Responsable : Ndeye Khady Syll
"""

import time
import random
from typing import Dict, Any, Optional
from scenario_manager import ScenarioManager, ScenarioType
from traffic_light import TrafficLightManager, TrafficLightState
from vehicle_behavior import VehicleManagerBehavior
from vehicle import VehicleManagerGraphic, VehicleType

class Simulation:
    """Classe principale qui orchestre toute la simulation"""
    
    def __init__(self, logger=None):
        """
        Initialise la simulation
        
        Args:
            logger: Instance du logger (optionnel)
        """
        self.logger = logger
        self.running = False
        self.paused = False
        self.simulation_timer = None
        
        # Composants (à initialiser dans setup())
        self.scenario_manager = None
        self.traffic_light_manager = None
        self.vehicle_manager_behavior = None
        self.vehicle_manager_graphic = None
        self.road_scene = None
        
        # Statistiques
        self.frame_count = 0
        self.start_time = 0
        self.vehicles_spawned = 0
        self.vehicles_removed = 0
        self.spawn_timer = 0
        self._last_light_update = 0
        self._last_spawn_update = 0
        
        print("✓ Simulation initialisée")
    
    def setup(self) -> bool:
        """
        Configure tous les composants de la simulation
        
        Returns:
            bool: True si la configuration a réussi
        """
        try:
            print("\nConfiguration de la simulation...")
            
            # 1. Gestionnaire de scénarios
            print("1. Initialisation ScenarioManager...")
            self.scenario_manager = ScenarioManager()
            print("   ✓ ScenarioManager prêt")
            
            # 2. Gestionnaire de feux
            print("2. Initialisation TrafficLightManager...")
            self.traffic_light_manager = TrafficLightManager()
            print("   ✓ TrafficLightManager prêt")
            
            # 3. Vérifier que les gestionnaires de véhicules sont déjà connectés
            print("3. Vérification gestionnaires véhicules...")
            if not self.vehicle_manager_behavior or not self.vehicle_manager_graphic:
                print("   ⚠ Gestionnaires de véhicules non connectés")
                print("   ℹ Ils doivent être connectés depuis main.py")
            else:
                print("   ✓ Gestionnaires de véhicules connectés")
            
            # Journaliser l'initialisation
            if self.logger:
                self.logger.log_simulation_event("SETUP_COMPLETE", "Simulation configurée")
            
            print("✓ Simulation configurée avec succès")
            return True
            
        except Exception as e:
            print(f"✗ Erreur configuration simulation: {e}")
            return False
    
    def start(self) -> bool:
        """
        Démarre la simulation avec un timer au lieu d'un thread
        
        Returns:
            bool: True si démarrage réussi
        """
        if self.running:
            print("⚠ Simulation déjà en cours")
            return False
        
        print("Démarrage de la simulation...")
        self.running = True
        self.paused = False
        self.start_time = time.time()
        self.frame_count = 0
        self.spawn_timer = 0
        self._last_light_update = time.time()
        self._last_spawn_update = time.time()
        
        # Démarrer la boucle via un timer (pas de thread)
        self._start_simulation_timer()
        
        # Journaliser
        if self.logger:
            scenario = self.scenario_manager.get_current_scenario_name()
            self.logger.log_simulation_event("SIMULATION_START", f"Scénario: {scenario}")
        
        print("✓ Simulation démarrée")
        return True
    
    def _start_simulation_timer(self):
        """Démarre la boucle de simulation via un timer"""
        if not self.running:
            return
        
        if self.paused:
            # Reprogrammer dans 100ms si en pause
            if self._has_tkinter_root():
                self._schedule_next_frame(100)
            return
        
        frame_start_time = time.time()
        
        try:
            # Mettre à jour la simulation
            self._update_components(0.033)  # ~30 FPS
            
            # Incrémenter le compteur
            self.frame_count += 1
            
            # Afficher les FPS occasionnellement
            if self.frame_count % 150 == 0:  # Toutes les 5 secondes (30 FPS * 5)
                elapsed = time.time() - frame_start_time
                fps = 1.0 / elapsed if elapsed > 0 else 0
                print(f"Frame {self.frame_count} - FPS: {fps:.1f}")
                
        except Exception as e:
            print(f"⚠ Erreur dans boucle simulation: {e}")
            # Continuer malgré l'erreur
        
        # Calculer le temps écoulé et programmer le prochain tick
        frame_time = time.time() - frame_start_time
        target_frame_time = 1.0 / 30  # 30 FPS
        delay_ms = max(1, int((target_frame_time - frame_time) * 1000))
        
        # Reprogrammer
        self._schedule_next_frame(delay_ms)
    
    def _has_tkinter_root(self):
        """Vérifie si on a accès à une racine Tkinter"""
        if self.road_scene and hasattr(self.road_scene, 'screen'):
            if hasattr(self.road_scene.screen, '_root'):
                return self.road_scene.screen._root is not None
        return False
    
    def _schedule_next_frame(self, delay_ms):
        """Programme la prochaine frame"""
        if self._has_tkinter_root():
            self.road_scene.screen._root.after(delay_ms, self._start_simulation_timer)
        else:
            # Fallback: utiliser time.sleep si pas de Tkinter
            time.sleep(delay_ms / 1000.0)
            if self.running and not self.paused:
                self._start_simulation_timer()
    
    def pause(self) -> None:
        """Met en pause ou reprend la simulation"""
        self.paused = not self.paused
        action = "PAUSE" if self.paused else "RESUME"
        
        print(f"Simulation {'mise en pause' if self.paused else 'reprise'}")
        
        if self.logger:
            self.logger.log_simulation_event(f"SIMULATION_{action}", "")
    
    def stop(self) -> None:
        """Arrête la simulation"""
        if not self.running:
            return
        
        print("Arrêt de la simulation...")
        self.running = False
        
        # Annuler le timer s'il existe
        if self.simulation_timer and self._has_tkinter_root():
            try:
                self.road_scene.screen._root.after_cancel(self.simulation_timer)
            except:
                pass
        
        # Calculer les statistiques
        duration = time.time() - self.start_time
        print(f"Simulation arrêtée après {duration:.1f} secondes")
        print(f"Frames: {self.frame_count}")
        print(f"Véhicules générés: {self.vehicles_spawned}")
        print(f"Véhicules supprimés: {self.vehicles_removed}")
        
        if self.logger:
            stats = {
                "duration": duration,
                "frames": self.frame_count,
                "vehicles_spawned": self.vehicles_spawned,
                "vehicles_removed": self.vehicles_removed
            }
            self.logger.log_simulation_event("SIMULATION_STOP", stats)
    
    def reset(self) -> None:
        """Réinitialise la simulation"""
        print("Réinitialisation de la simulation...")
        
        self.stop()
        time.sleep(0.1)
        
        # Réinitialiser les statistiques
        self.frame_count = 0
        self.vehicles_spawned = 0
        self.vehicles_removed = 0
        self.spawn_timer = 0
        self._last_light_update = 0
        self._last_spawn_update = 0
        
        # Réinitialiser les composants
        if self.traffic_light_manager:
            self.traffic_light_manager.change_all_states(TrafficLightState.RED, manual=True)
        
        # Supprimer tous les véhicules
        if self.vehicle_manager_behavior:
            self.vehicle_manager_behavior.clear_all_vehicles()
        
        if self.vehicle_manager_graphic:
            self.vehicle_manager_graphic.clear_all_vehicles()
        
        if self.logger:
            self.logger.log_simulation_event("SIMULATION_RESET", "")
        
        print("✓ Simulation réinitialisée")
    
    def change_scenario(self, scenario_name: str) -> bool:
        """
        Change le scénario de circulation
        
        Args:
            scenario_name: Nom du scénario (normal, rush_hour, night, manual)
        
        Returns:
            bool: True si changement réussi
        """
        try:
            # Convertir le nom en ScenarioType
            scenario_map = {
                "normal": ScenarioType.NORMAL,
                "rush_hour": ScenarioType.RUSH_HOUR,
                "night": ScenarioType.NIGHT,
                "manual": ScenarioType.MANUAL
            }
            
            if scenario_name not in scenario_map:
                print(f"✗ Scénario inconnu: {scenario_name}")
                return False
            
            scenario_type = scenario_map[scenario_name]
            success = self.scenario_manager.change_scenario(scenario_type)
            
            if success:
                # Appliquer les paramètres du nouveau scénario
                self._apply_scenario_settings()
                
                # Journaliser
                if self.logger:
                    old_name = self.scenario_manager.previous_scenario.name
                    new_name = self.scenario_manager.get_current_scenario_name()
                    self.logger.log_simulation_event(
                        "SCENARIO_CHANGE", 
                        f"{old_name} -> {new_name}"
                    )
                
                print(f"✓ Scénario changé vers: {scenario_name}")
                return True
            
            return False
            
        except Exception as e:
            print(f"✗ Erreur changement scénario: {e}")
            return False
    
    def change_traffic_light_manual(self, state: str) -> None:
        """
        Change manuellement l'état du feu
        
        Args:
            state: État désiré (red, orange, green)
        """
        if not self.traffic_light_manager:
            print("⚠ TrafficLightManager non initialisé")
            return
        
        # Convertir l'état
        state_map = {
            "red": TrafficLightState.RED,
            "orange": TrafficLightState.ORANGE,
            "green": TrafficLightState.GREEN
        }
        
        if state not in state_map:
            print(f"✗ État inconnu: {state}")
            return
        
        new_state = state_map[state]
        self.traffic_light_manager.change_all_states(new_state, manual=True)
        
        # Journaliser
        if self.logger:
            self.logger.log_simulation_event(
                "TRAFFIC_LIGHT_MANUAL", 
                f"Changement manuel vers {state.upper()}"
            )
        
        print(f"✓ Feux changés manuellement vers: {state}")
    
    def _apply_scenario_settings(self) -> None:
        """Applique les paramètres du scénario actuel"""
        if not self.scenario_manager:
            return
        
        scenario = self.scenario_manager.get_current_scenario()
        scenario_name = scenario.name.lower().replace(" ", "_")
        
        # Appliquer aux feux
        if self.traffic_light_manager:
            if "nuit" in scenario_name.lower():
                self.traffic_light_manager.set_all_blinking(True)
            else:
                self.traffic_light_manager.set_all_blinking(False)
        
        # Appliquer aux véhicules
        if self.vehicle_manager_behavior:
            self.vehicle_manager_behavior.set_scenario(scenario_name)
    
    def _update_components(self, delta_time: float) -> None:
        """Met à jour tous les composants"""
        try:
            # 1. Récupérer l'état du feu
            light_state = None
            if self.traffic_light_manager:
                states = self.traffic_light_manager.get_current_states()
                # Prendre l'état du premier feu (tous les feux ont le même état)
                if states:
                    light_state = list(states.values())[0]  # Déjà une string comme "ROUGE", "VERT", etc.
            
            # 2. Mettre à jour les feux (seulement toutes les 0.5 secondes)
            current_time = time.time()
            if self.scenario_manager and self.traffic_light_manager:
                if current_time - self._last_light_update > 0.5:  # 0.5 secondes
                    durations = self.scenario_manager.get_traffic_light_durations()
                    self.traffic_light_manager.update_all(durations)
                    self._last_light_update = current_time
            
            # 3. Gérer l'apparition de nouveaux véhicules
            self._handle_vehicle_spawning(delta_time)
            
            # 4. Mettre à jour le comportement des véhicules
            if self.vehicle_manager_behavior:
                # Mettre à jour les véhicules existants
                removed_ids = self.vehicle_manager_behavior.update(light_state)
                
                # Gérer la suppression graphique des véhicules
                for vehicle_id in removed_ids:
                    if self.vehicle_manager_graphic:
                        self.vehicle_manager_graphic.remove_vehicle(vehicle_id)
                    self.vehicles_removed += 1
                
                # Mettre à jour les positions graphiques
                self._update_vehicle_graphics()
                
                # Mettre à jour les statistiques
                self.vehicles_spawned = self.vehicle_manager_behavior.vehicles_spawned
            
            # 5. Mettre à jour l'affichage (seulement toutes les 2 frames pour économiser CPU)
            if self.road_scene and self.frame_count % 2 == 0:
                self.road_scene.update_display()
                
        except Exception as e:
            print(f"⚠ Erreur dans update_components: {e}")
            if self.logger:
                try:
                    self.logger.log_simulation_event("SIMULATION_ERROR", str(e))
                except:
                    pass
    
    def _handle_vehicle_spawning(self, delta_time: float) -> None:
        """Gère l'apparition de nouveaux véhicules"""
        if not self.vehicle_manager_behavior:
            return
        
        # Incrémenter le timer
        self.spawn_timer += delta_time
        
        # Déterminer le taux d'apparition selon le scénario
        spawn_rates = {
            "normal": 0.01,      # 1% de chance par frame
            "rush_hour": 0.03,   # 3% de chance
            "night": 0.002,      # 0.2% de chance
            "manual": 0.01       # 1% de chance
        }
        
        # Récupérer le nom du scénario
        scenario_name = "normal"
        if self.scenario_manager:
            scenario_name = self.scenario_manager.get_current_scenario_name().lower().replace(" ", "_")
        
        spawn_rate = spawn_rates.get(scenario_name, 0.01)
        
        # Essayer de faire apparaître un véhicule (basé sur probabilité)
        if random.random() < spawn_rate:
            vehicle_id = self.vehicle_manager_behavior.spawn_vehicle()
            
            # Créer aussi le véhicule graphique
            if vehicle_id and self.vehicle_manager_graphic:
                # Choisir un type aléatoire (80% voiture, 20% camion)
                vehicle_type = VehicleType.CAR if random.random() < 0.8 else VehicleType.TRUCK
                
                # Vérifier si le véhicule existe déjà
                existing_vehicle = self.vehicle_manager_graphic.get_vehicle(vehicle_id)
                if not existing_vehicle:
                    # Créer le véhicule graphique
                    graphic_id = self.vehicle_manager_graphic.create_vehicle(vehicle_type)
                    
                    # Récupérer la position initiale du véhicule comportemental
                    vehicle_behavior = self.vehicle_manager_behavior.vehicles.get(vehicle_id)
                    if vehicle_behavior:
                        position = vehicle_behavior.get_position()
                        direction = vehicle_behavior.direction
                        # Dessiner immédiatement le véhicule
                        self.vehicle_manager_graphic.draw_vehicle(graphic_id, position, direction)
                    
                    # S'assurer que les IDs correspondent
                    if graphic_id != vehicle_id:
                        print(f"⚠ Incohérence ID véhicule: comportement={vehicle_id}, graphique={graphic_id}")
    
    def _update_vehicle_graphics(self) -> None:
        """Met à jour les positions graphiques des véhicules"""
        if not self.vehicle_manager_behavior or not self.vehicle_manager_graphic:
            return
        
        try:
            # Récupérer les positions et directions des véhicules comportementaux
            positions = self.vehicle_manager_behavior.get_vehicle_positions()
            directions = self.vehicle_manager_behavior.get_vehicle_directions()
            
            # Mettre à jour chaque véhicule graphique
            for vehicle_id, position in positions.items():
                if vehicle_id in directions:
                    direction = directions[vehicle_id]
                    
                    # Vérifier si le véhicule graphique existe
                    vehicle_graphic = self.vehicle_manager_graphic.get_vehicle(vehicle_id)
                    
                    # S'il n'existe pas, le créer
                    if not vehicle_graphic:
                        vehicle_type = VehicleType.CAR  # Par défaut
                        self.vehicle_manager_graphic.create_vehicle(vehicle_type)
                        vehicle_graphic = self.vehicle_manager_graphic.get_vehicle(vehicle_id)
                    
                    # Mettre à jour la position
                    if vehicle_graphic:
                        self.vehicle_manager_graphic.draw_vehicle(vehicle_id, position, direction)
                        
        except Exception as e:
            print(f"⚠ Erreur update_vehicle_graphics: {e}")
    
    def is_running(self) -> bool:
        """Vérifie si la simulation est en cours"""
        return self.running
    
    def is_paused(self) -> bool:
        """Vérifie si la simulation est en pause"""
        return self.paused
    
    def get_statistics(self) -> Dict[str, Any]:
        """Retourne des statistiques sur la simulation"""
        duration = time.time() - self.start_time if self.start_time > 0 else 0
        
        vehicle_count = 0
        if self.vehicle_manager_behavior:
            vehicle_count = self.vehicle_manager_behavior.get_vehicle_count()
        
        return {
            "running": self.running,
            "paused": self.paused,
            "frame_count": self.frame_count,
            "duration": duration,
            "vehicles_spawned": self.vehicles_spawned,
            "vehicles_removed": self.vehicles_removed,
            "current_vehicles": vehicle_count,
            "current_scenario": self.scenario_manager.get_current_scenario_name() if self.scenario_manager else "N/A",
            "fps": self.frame_count / duration if duration > 0 else 0
        }


def test_simulation():
    """Teste le module Simulation"""
    print("\n=== TEST Simulation ===")
    
    simulation = Simulation()
    
    if simulation.setup():
        print("\n1. Test démarrage/arrêt:")
        simulation.start()
        time.sleep(2)
        simulation.stop()
        
        print("\n2. Test changement scénario:")
        simulation.change_scenario("rush_hour")
        simulation.change_scenario("night")
        simulation.change_scenario("normal")
        
        print("\n3. Test contrôle manuel feux:")
        simulation.change_traffic_light_manual("red")
        simulation.change_traffic_light_manual("green")
        simulation.change_traffic_light_manual("orange")
        
        print("\n4. Test statistiques:")
        stats = simulation.get_statistics()
        for key, value in stats.items():
            print(f"  {key}: {value}")
        
        print("\n✓ Tests Simulation terminés")
    else:
        print("✗ Échec configuration simulation")


if __name__ == "__main__":
    test_simulation()