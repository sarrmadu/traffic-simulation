"""
Module de journalisation des événements
Responsable : Modou Sarr
"""

from database import DatabaseManager
from typing import Optional, Dict, Any
import time

class EventLogger:
    """
    Gère la journalisation de tous les événements de la simulation
    """
    
    def __init__(self, database_manager: Optional[DatabaseManager] = None):
        """
        Initialise le logger
        
        Args:
            database_manager: Instance de DatabaseManager (optionnel)
        """
        self.db = database_manager
        self.enabled = True
        
        if self.db:
            print("✓ EventLogger initialisé avec DatabaseManager")
        else:
            print("⚠ EventLogger initialisé sans base de données")
    
    def log_simulation_event(self, action: str, details: Optional[str] = None) -> None:
        """
        Journalise un événement de simulation
        
        Args:
            action: Action effectuée
            details: Détails supplémentaires
        """
        if not self.enabled:
            return
        
        full_action = action
        if details:
            if isinstance(details, dict):
                import json
                details = json.dumps(details, ensure_ascii=False)
            full_action += f" - {details}"
        
        print(f"[SIMULATION] {full_action}")
        
        if self.db and self.db.connected:
            self.db.insert_event("SIMULATION", full_action)
    
    def log_traffic_light_event(self, 
                               from_state: str, 
                               to_state: str, 
                               manual: bool = False,
                               scenario: Optional[str] = None) -> None:
        """
        Journalise un changement de feu
        
        Args:
            from_state: État précédent
            to_state: Nouvel état
            manual: True si changement manuel
            scenario: Scénario actuel
        """
        if not self.enabled:
            return
        
        action_type = "MANUEL" if manual else "AUTOMATIQUE"
        action = f"{from_state} -> {to_state} ({action_type})"
        
        print(f"[FEU TRICOLORE] {action}")
        
        if self.db and self.db.connected:
            self.db.insert_event("TRAFFIC_LIGHT", action, etat_feu=to_state, scenario=scenario)
    
    def log_vehicle_event(self, 
                         vehicle_id: int, 
                         event: str, 
                         position_x: Optional[float] = None,
                         position_y: Optional[float] = None,
                         vitesse: Optional[float] = None,
                         etat_feu: Optional[str] = None,
                         scenario: Optional[str] = None) -> None:
        """
        Journalise un événement de véhicule
        
        Args:
            vehicle_id: ID du véhicule
            event: Événement (création, suppression, arrêt, etc.)
            position_x: Position X
            position_y: Position Y
            vitesse: Vitesse du véhicule
            etat_feu: État du feu au moment de l'événement
            scenario: Scénario actuel
        """
        if not self.enabled:
            return
        
        print(f"[VEHICULE {vehicle_id}] {event} - Pos: ({position_x}, {position_y}), Vit: {vitesse}")
        
        if self.db and self.db.connected:
            self.db.insert_event(
                "VEHICLE", 
                event, 
                etat_feu=etat_feu,
                scenario=scenario,
                id_voiture=vehicle_id,
                position_x=position_x,
                position_y=position_y,
                vitesse=vitesse
            )
    
    def log_scenario_change(self, old_scenario: str, new_scenario: str) -> None:
        """
        Journalise un changement de scénario
        
        Args:
            old_scenario: Ancien scénario
            new_scenario: Nouveau scénario
        """
        if not self.enabled:
            return
        
        action = f"{old_scenario} -> {new_scenario}"
        
        print(f"[SCENARIO] {action}")
        
        if self.db and self.db.connected:
            self.db.insert_event("SCENARIO", action, scenario=new_scenario)
    
    def log_user_action(self, action: str, details: Optional[str] = None) -> None:
        """
        Journalise une action utilisateur
        
        Args:
            action: Action de l'utilisateur
            details: Détails supplémentaires
        """
        if not self.enabled:
            return
        
        full_action = f"Action utilisateur: {action}"
        if details:
            full_action += f" - {details}"
        
        print(f"[UTILISATEUR] {full_action}")
        
        if self.db and self.db.connected:
            self.db.insert_event("USER_ACTION", full_action)
    
    def get_recent_logs(self, limit: int = 20) -> list:
        """
        Récupère les logs récents depuis la base de données
        
        Args:
            limit: Nombre maximum de logs
            
        Returns:
            Liste des logs récents
        """
        if not self.db or not self.db.connected:
            return []
        
        events = self.db.get_all_events(limit)
        logs = []
        
        for event in events:
            log = {
                "id": event[0],
                "timestamp": event[1],
                "type": event[2],
                "action": event[3],
                "scenario": event[5],
                "vehicle_id": event[6]
            }
            logs.append(log)
        
        return logs
    
    def clear_logs(self) -> bool:
        """
        Efface tous les logs
        
        Returns:
            True si réussi
        """
        if not self.db or not self.db.connected:
            return False
        
        try:
            self.db.reset_database()
            print("✓ Tous les logs effacés")
            return True
        except Exception as e:
            print(f"✗ Erreur effacement logs: {e}")
            return False


def test_logger():
    """Teste le module EventLogger"""
    print("\n=== TEST EventLogger ===")
    
    # Créer une base de données test
    db = DatabaseManager("test_logger.db")
    db.connect()
    
    logger = EventLogger(db)
    
    print("\n1. Test journalisation événements:")
    logger.log_simulation_event("DÉMARRAGE", "Test de simulation")
    logger.log_traffic_light_event("ROUGE", "VERT", manual=False, scenario="normal")
    logger.log_vehicle_event(1, "CRÉATION", 100.5, 50.2, 2.3, "VERT", "normal")
    logger.log_scenario_change("normal", "rush_hour")
    logger.log_user_action("Bouton Démarrer cliqué")
    
    print("\n2. Test récupération logs:")
    logs = logger.get_recent_logs(5)
    print(f"  {len(logs)} logs récupérés")
    
    for log in logs:
        print(f"  - [{log['timestamp']}] {log['type']}: {log['action']}")
    
    print("\n3. Test désactivation logger:")
    logger.enabled = False
    logger.log_simulation_event("TEST_DÉSACTIVÉ", "Ne devrait pas s'afficher")
    logger.enabled = True
    
    db.disconnect()
    print("\n✓ Tests EventLogger terminés")


if __name__ == "__main__":
    test_logger()