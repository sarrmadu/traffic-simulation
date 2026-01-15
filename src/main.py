"""
Point d'entrée principal de l'application
Responsable : Modou Sarr
"""

import sys
import os
import argparse
import threading
import time

# Ajouter le répertoire courant au path Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import des modules de l'application
try:
    from simulation import Simulation
    from gui import ControlInterface
    from logger import EventLogger
    from database import DatabaseManager
    from road_scene import RoadScene
    from constants import VERSION, AUTHOR, YEAR
    from vehicle import VehicleManagerGraphic, VehicleType
    from vehicle_behavior import VehicleManagerBehavior
    print("✓ Modules importés avec succès")
except ImportError as e:
    print(f"✗ Erreur d'importation: {e}")
    print("Vérifiez que tous les fichiers sont dans le répertoire src/")
    sys.exit(1)


class TrafficSimulationApp:
    """
    Application principale de simulation de trafic
    """
    
    def __init__(self, debug: bool = False):
        """
        Initialise l'application
        
        Args:
            debug: Mode débogage activé
        """
        self.debug = debug
        self.simulation = None
        self.interface = None
        self.logger = None
        self.database = None
        self.road_scene = None
        self.vehicle_manager_graphic = None
        self.vehicle_manager_behavior = None
        self.running = False
        
        print("\n" + "=" * 60)
        print(f"SIMULATION FEU TRICOLORE - VILLE DE THIÈS")
        print(f"Version {VERSION} - {YEAR}")
        print(f"Développé par: {AUTHOR}")
        print("=" * 60)
        
        if debug:
            print("Mode débogage activé")
    
    def setup(self) -> bool:
        """
        Configure tous les composants de l'application
        
        Returns:
            bool: True si la configuration a réussi
        """
        print("\nInitialisation de l'application...")
        
        try:
            # 1. Initialiser la base de données
            print("1. Configuration de la base de données...")
            self.database = DatabaseManager()
            if self.database.connect():
                print("   ✓ Base de données connectée")
            else:
                print("   ✗ Erreur de connexion à la base de données")
                return False
            
            # 2. Initialiser le logger
            print("2. Configuration du logger...")
            self.logger = EventLogger(self.database)
            print("   ✓ Logger configuré")
            
            # 3. Initialiser la scène routière (TRÈS IMPORTANT - doit être fait avant Turtle)
            print("3. Configuration de la scène routière...")
            self.road_scene = RoadScene()
            if self.road_scene.setup():
                print("   ✓ Scène routière configurée")
                # Dessiner le carrefour
                self.road_scene.draw_road_network()
                print("   ✓ Carrefour dessiné")
            else:
                print("   ✗ Erreur de configuration de la scène routière")
                return False
            
            # 4. Initialiser les gestionnaires de véhicules
            print("4. Configuration des véhicules...")
            
            # Gestionnaire graphique
            self.vehicle_manager_graphic = VehicleManagerGraphic()
            if hasattr(self.vehicle_manager_graphic, 'setup'):
                self.vehicle_manager_graphic.setup(self.road_scene.screen)
                print("   ✓ Gestionnaire graphique configuré")
            
            # Gestionnaire comportemental
            self.vehicle_manager_behavior = VehicleManagerBehavior(logger=self.logger)
            self.vehicle_manager_behavior.set_scenario("normal")
            print("   ✓ Gestionnaire comportemental configuré")
            
            # Connecter les deux gestionnaires
            self._connect_vehicle_managers()
            
            # 5. Initialiser la simulation
            print("5. Configuration de la simulation...")
            self.simulation = Simulation(self.logger)
            
            # Passer les composants à la simulation
            self.simulation.road_scene = self.road_scene
            self.simulation.vehicle_manager_graphic = self.vehicle_manager_graphic
            self.simulation.vehicle_manager_behavior = self.vehicle_manager_behavior
            
            if self.simulation.setup():
                print("   ✓ Simulation configurée")
            else:
                print("   ✗ Erreur de configuration de la simulation")
                return False
            
            # 6. Initialiser l'interface
            print("6. Configuration de l'interface...")
            # Créer une fonction callback pour gérer les actions
            def handle_gui_action(action):
                self._handle_gui_action(action)
            
            self.interface = ControlInterface(simulation_callback=handle_gui_action)
            
            # Configurer l'interface (sans la lancer encore)
            if hasattr(self.interface, 'setup'):
                if self.interface.setup():
                    print("   ✓ Interface configurée")
                else:
                    print("   ✗ Erreur de configuration de l'interface")
                    return False
            else:
                print("   ⚠ Interface n'a pas de méthode setup(), continuation...")
            
            # 7. Journaliser le démarrage
            self.logger.log_simulation_event("APPLICATION_START", "Application démarrée")
            
            print("\n✓ Application initialisée avec succès!")
            return True
            
        except Exception as e:
            print(f"\n✗ Erreur lors de l'initialisation: {e}")
            if self.debug:
                import traceback
                traceback.print_exc()
            return False
    
    def _connect_vehicle_managers(self):
        """Connecte les gestionnaires de véhicules pour qu'ils communiquent"""
        if not self.vehicle_manager_graphic or not self.vehicle_manager_behavior:
            return
        
        # Stocker les références mutuelles
        self.vehicle_manager_graphic.behavior_manager = self.vehicle_manager_behavior
        self.vehicle_manager_behavior.graphic_manager = self.vehicle_manager_graphic
        
        print("   ✓ Gestionnaires de véhicules connectés")
    
    def _handle_gui_action(self, action: str) -> None:
        """
        Gère les actions provenant de l'interface graphique
        """
        print(f"Action reçue de l'interface: {action}")
        
        if not self.simulation:
            print("⚠ Simulation non initialisée")
            return
        
        # Journaliser l'action utilisateur
        self.logger.log_user_action(f"Interface: {action}")
        
        # Traiter l'action
        if action == "start":
            if self.simulation.start():
                print("🎬 Simulation démarrée")
                if hasattr(self.interface, 'update_status'):
                    self.interface.update_status("EN COURS", "#4CAF50")
        
        elif action == "pause":
            self.simulation.pause()
            if self.simulation.is_paused():
                print("⏸ Simulation mise en pause")
                if hasattr(self.interface, 'update_status'):
                    self.interface.update_status("EN PAUSE", "#FF9800")
            else:
                print("▶ Simulation reprise")
                if hasattr(self.interface, 'update_status'):
                    self.interface.update_status("EN COURS", "#4CAF50")
        
        elif action == "stop":
            self.simulation.stop()
            print("⏹ Simulation arrêtée")
            if hasattr(self.interface, 'update_status'):
                self.interface.update_status("ARRÊTÉE", "#F44336")
        
        elif action == "reset":
            self.simulation.reset()
            print("🔄 Simulation réinitialisée")
            if hasattr(self.interface, 'update_status'):
                self.interface.update_status("RÉINITIALISÉE", "#2196F3")
            
            # Redessiner le carrefour
            if self.road_scene:
                self.road_scene.draw_road_network()
            
            time.sleep(0.5)
            if hasattr(self.interface, 'update_status'):
                self.interface.update_status("ARRÊTÉE", "#F44336")
        
        elif action.startswith("scenario:"):
            scenario = action.split(":")[1]
            if self.simulation.change_scenario(scenario):
                scenario_names = {
                    "normal": "Circulation Normale",
                    "rush_hour": "Heure de Pointe",
                    "night": "Mode Nuit",
                    "manual": "Mode Manuel"
                }
                display_name = scenario_names.get(scenario, scenario)
                print(f"📋 Scénario changé: {display_name}")
                
                if hasattr(self.interface, 'update_scenario'):
                    self.interface.update_scenario(display_name)
        
        elif action.startswith("light:"):
            color = action.split(":")[1]
            self.simulation.change_traffic_light_manual(color)
            light_name = color.upper()
            print(f"🚦 Feu changé manuellement: {light_name}")
            
            if hasattr(self.interface, 'update_traffic_light'):
                self.interface.update_traffic_light(light_name)
    
    def _update_stats(self):
        """Met à jour les statistiques dans l'interface"""
        while self.running and self.simulation and self.interface:
            try:
                if self.simulation.is_running() and not self.simulation.is_paused():
                    # Récupérer les statistiques
                    stats = self.simulation.get_statistics()
                    
                    # Mettre à jour l'interface
                    if hasattr(self.interface, 'update_vehicle_count'):
                        vehicle_count = self.vehicle_manager_behavior.get_vehicle_count() if self.vehicle_manager_behavior else 0
                        self.interface.update_vehicle_count(vehicle_count)
                
                time.sleep(1)  # Mettre à jour toutes les secondes
                
            except Exception as e:
                if self.debug:
                    print(f"⚠ Erreur mise à jour stats: {e}")
                time.sleep(1)
    
    def run(self) -> int:
        """
        Exécute l'application
        
        Returns:
            int: Code de retour (0 = succès, autre = erreur)
        """
        if not self.setup():
            return 1
        
        print("\n" + "=" * 60)
        print("DÉMARRAGE DE L'APPLICATION")
        print("=" * 60)
        print("\nInstructions importantes:")
        print("1. L'application va maintenant s'ouvrir")
        print("2. Vous verrez DEUX fenêtres:")
        print("   - Fenêtre Turtle (carrefour avec feux)")
        print("   - Fenêtre Tkinter (interface de contrôle)")
        print("3. Utilisez l'interface Tkinter pour contrôler")
        print("4. Ne fermez PAS la fenêtre Turtle!")
        print("\nAppuyez sur Ctrl+C dans ce terminal pour quitter")
        print("=" * 60)
        
        try:
            # Démarrer le thread de mise à jour des stats
            self.running = True
            stats_thread = threading.Thread(target=self._update_stats, daemon=True)
            stats_thread.start()
            
            print("\nLancement de l'interface de contrôle...")
            print("La fenêtre Turtle devrait déjà être visible.")
            print("\nEn attente des commandes depuis l'interface...")
            
            # Lancer l'interface (cette fonction est bloquante)
            self.interface.run()
            
            # Quand l'interface se ferme
            print("\nInterface fermée par l'utilisateur")
            self.cleanup()
            
            return 0
            
        except KeyboardInterrupt:
            print("\n\nArrêt demandé par l'utilisateur (Ctrl+C)")
            self.cleanup()
            return 0
            
        except Exception as e:
            print(f"\n✗ Erreur d'exécution: {e}")
            if self.debug:
                import traceback
                traceback.print_exc()
            self.cleanup()
            return 1
    
    def cleanup(self) -> None:
        """
        Nettoie les ressources de l'application
        """
        print("\nNettoyage des ressources...")
        
        self.running = False
        
        try:
            # Arrêter la simulation si elle tourne
            if self.simulation and hasattr(self.simulation, 'stop'):
                self.simulation.stop()
                print("   ✓ Simulation arrêtée")
            
            # Fermer l'interface
            if self.interface and hasattr(self.interface, 'close'):
                self.interface.close()
                print("   ✓ Interface fermée")
            
            # Fermer la scène routière (fenêtre Turtle)
            if self.road_scene and hasattr(self.road_scene, 'close'):
                self.road_scene.close()
                print("   ✓ Scène routière fermée")
            
            # Supprimer tous les véhicules
            if self.vehicle_manager_graphic:
                self.vehicle_manager_graphic.clear_all_vehicles()
                print("   ✓ Véhicules graphiques nettoyés")
            
            if self.vehicle_manager_behavior:
                self.vehicle_manager_behavior.clear_all_vehicles()
                print("   ✓ Véhicules comportementaux nettoyés")
            
            # Journaliser la fermeture
            if self.logger:
                self.logger.log_simulation_event("APPLICATION_STOP", "Application fermée")
                print("   ✓ Événement de fermeture journalisé")
            
            # Fermer la base de données
            if self.database and hasattr(self.database, 'disconnect'):
                self.database.disconnect()
                print("   ✓ Base de données fermée")
            
            print("✓ Nettoyage terminé")
            
        except Exception as e:
            print(f"✗ Erreur lors du nettoyage: {e}")


def parse_arguments() -> argparse.Namespace:
    """
    Parse les arguments de ligne de commande
    
    Returns:
        argparse.Namespace: Arguments parsés
    """
    parser = argparse.ArgumentParser(
        description="Simulation de feu tricolore - Ville de Thiès",
        epilog=f"Version {VERSION}"
    )
    
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Active le mode débogage"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {VERSION}"
    )
    
    parser.add_argument(
        "--reset-db",
        action="store_true",
        help="Réinitialise la base de données"
    )
    
    parser.add_argument(
        "--test",
        action="store_true",
        help="Mode test (pas d'interface graphique)"
    )
    
    return parser.parse_args()


def main() -> int:
    """
    Fonction principale
    
    Returns:
        int: Code de retour
    """
    # Parser les arguments
    args = parse_arguments()
    
    # Gérer la réinitialisation de la base de données
    if args.reset_db:
        print("Réinitialisation de la base de données...")
        db = DatabaseManager()
        db.connect()
        db.reset_database()
        db.disconnect()
        print("✓ Base de données réinitialisée")
        return 0
    
    # Mode test simple
    if args.test:
        print("Mode test - vérification des modules...")
        try:
            # Test simple d'import
            from road_scene import RoadScene
            scene = RoadScene()
            if scene.setup():
                print("✓ RoadScene fonctionne")
                scene.draw_road_network()
                input("Appuyez sur Entrée pour fermer...")
                scene.close()
            return 0
        except Exception as e:
            print(f"✗ Erreur test: {e}")
            return 1
    
    # Créer et exécuter l'application
    app = TrafficSimulationApp(debug=args.debug)
    
    # Exécuter l'application
    return app.run()


if __name__ == "__main__":
    sys.exit(main())