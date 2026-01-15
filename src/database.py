"""
Module de gestion de la base de données SQLite
Responsable : Modou Sarr
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Tuple, Dict, Any, Optional
import os

class DatabaseManager:
    """
    Gère la connexion et les opérations sur la base de données
    """
    
    def __init__(self, db_name: str = "traffic_simulation.db"):
        """
        Initialise le gestionnaire de base de données
        
        Args:
            db_name: Nom du fichier de base de données
        """
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.connected = False
        
        print(f"✓ DatabaseManager initialisé (base: {db_name})")
    
    def connect(self) -> bool:
        """
        Établit la connexion à la base de données
        
        Returns:
            bool: True si connexion réussie
        """
        try:
            # Créer le dossier database s'il n'existe pas
            os.makedirs("database", exist_ok=True)
            
            # Connexion à la base de données
            db_path = os.path.join("database", self.db_name)
            self.conn = sqlite3.connect(db_path)
            self.cursor = self.conn.cursor()
            self.connected = True
            
            # Créer les tables si nécessaire
            self._create_tables()
            
            print(f"✓ Base de données connectée: {db_path}")
            return True
            
        except sqlite3.Error as e:
            print(f"✗ Erreur connexion base de données: {e}")
            return False
    
    def _create_tables(self) -> None:
        """Crée les tables nécessaires si elles n'existent pas"""
        # Table des événements de simulation
        events_table = """
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            type_action TEXT NOT NULL,
            action TEXT,
            etat_feu TEXT,
            scenario TEXT,
            id_voiture INTEGER,
            position_x REAL,
            position_y REAL,
            vitesse REAL
        )
        """
        
        # Table des statistiques (agrégées)
        stats_table = """
        CREATE TABLE IF NOT EXISTS statistics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE DEFAULT CURRENT_DATE,
            scenario TEXT,
            total_events INTEGER DEFAULT 0,
            simulation_time REAL DEFAULT 0,
            vehicles_spawned INTEGER DEFAULT 0,
            vehicles_removed INTEGER DEFAULT 0
        )
        """
        
        try:
            self.cursor.execute(events_table)
            self.cursor.execute(stats_table)
            self.conn.commit()
            print("✓ Tables créées ou déjà existantes")
            
        except sqlite3.Error as e:
            print(f"✗ Erreur création tables: {e}")
    
    def disconnect(self) -> None:
        """Ferme la connexion à la base de données"""
        if self.conn:
            self.conn.close()
            self.connected = False
            print("✓ Connexion base de données fermée")
    
    def insert_event(self, 
                    type_action: str, 
                    action: str, 
                    etat_feu: Optional[str] = None,
                    scenario: Optional[str] = None,
                    id_voiture: Optional[int] = None,
                    position_x: Optional[float] = None,
                    position_y: Optional[float] = None,
                    vitesse: Optional[float] = None) -> int:
        """
        Insère un événement dans la base de données
        
        Returns:
            int: ID de l'événement inséré, -1 en cas d'erreur
        """
        if not self.connected:
            print("⚠ Base de données non connectée")
            return -1
        
        query = """
        INSERT INTO events 
        (type_action, action, etat_feu, scenario, id_voiture, position_x, position_y, vitesse)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        try:
            self.cursor.execute(query, (
                type_action, action, etat_feu, scenario, 
                id_voiture, position_x, position_y, vitesse
            ))
            self.conn.commit()
            
            event_id = self.cursor.lastrowid
            print(f"✓ Événement #{event_id} inséré: {type_action} - {action}")
            return event_id
            
        except sqlite3.Error as e:
            print(f"✗ Erreur insertion événement: {e}")
            return -1
    
    def get_all_events(self, limit: int = 100) -> List[Tuple]:
        """
        Récupère tous les événements
        
        Args:
            limit: Nombre maximum d'événements à retourner
        
        Returns:
            Liste des événements
        """
        if not self.connected:
            return []
        
        query = "SELECT * FROM events ORDER BY timestamp DESC LIMIT ?"
        
        try:
            self.cursor.execute(query, (limit,))
            return self.cursor.fetchall()
            
        except sqlite3.Error as e:
            print(f"✗ Erreur récupération événements: {e}")
            return []
    
    def get_events_by_type(self, event_type: str, limit: int = 50) -> List[Tuple]:
        """
        Récupère les événements par type
        
        Args:
            event_type: Type d'événement
            limit: Nombre maximum
        
        Returns:
            Liste des événements
        """
        if not self.connected:
            return []
        
        query = "SELECT * FROM events WHERE type_action = ? ORDER BY timestamp DESC LIMIT ?"
        
        try:
            self.cursor.execute(query, (event_type, limit))
            return self.cursor.fetchall()
            
        except sqlite3.Error as e:
            print(f"✗ Erreur récupération par type: {e}")
            return []
    
    def get_events_by_scenario(self, scenario: str, limit: int = 50) -> List[Tuple]:
        """
        Récupère les événements par scénario
        """
        if not self.connected:
            return []
        
        query = "SELECT * FROM events WHERE scenario = ? ORDER BY timestamp DESC LIMIT ?"
        
        try:
            self.cursor.execute(query, (scenario, limit))
            return self.cursor.fetchall()
            
        except sqlite3.Error as e:
            print(f"✗ Erreur récupération par scénario: {e}")
            return []
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Calcule des statistiques sur les données
        
        Returns:
            Dictionnaire de statistiques
        """
        if not self.connected:
            return {}
        
        stats = {}
        
        try:
            # Nombre total d'événements
            self.cursor.execute("SELECT COUNT(*) FROM events")
            stats["total_events"] = self.cursor.fetchone()[0]
            
            # Événements par type
            self.cursor.execute("""
                SELECT type_action, COUNT(*) 
                FROM events 
                GROUP BY type_action
            """)
            stats["events_by_type"] = dict(self.cursor.fetchall())
            
            # Dernier événement
            self.cursor.execute("""
                SELECT timestamp, type_action, action 
                FROM events 
                ORDER BY timestamp DESC 
                LIMIT 1
            """)
            last_event = self.cursor.fetchone()
            stats["last_event"] = last_event
            
            # Nombre d'événements aujourd'hui
            self.cursor.execute("""
                SELECT COUNT(*) 
                FROM events 
                WHERE DATE(timestamp) = DATE('now')
            """)
            stats["events_today"] = self.cursor.fetchone()[0]
            
            return stats
            
        except sqlite3.Error as e:
            print(f"✗ Erreur calcul statistiques: {e}")
            return {}
    
    def clear_old_events(self, days_old: int = 30) -> int:
        """
        Supprime les événements trop anciens
        
        Args:
            days_old: Âge en jours
        
        Returns:
            Nombre d'événements supprimés
        """
        if not self.connected:
            return 0
        
        query = "DELETE FROM events WHERE DATE(timestamp) < DATE('now', ?)"
        
        try:
            self.cursor.execute(query, (f'-{days_old} days',))
            deleted = self.cursor.rowcount
            self.conn.commit()
            
            print(f"✓ {deleted} événements anciens supprimés")
            return deleted
            
        except sqlite3.Error as e:
            print(f"✗ Erreur suppression événements: {e}")
            return 0
    
    def reset_database(self) -> bool:
        """Réinitialise complètement la base de données"""
        try:
            self.cursor.execute("DROP TABLE IF EXISTS events")
            self.cursor.execute("DROP TABLE IF EXISTS statistics")
            self.conn.commit()
            
            # Recréer les tables
            self._create_tables()
            
            print("✓ Base de données réinitialisée")
            return True
            
        except sqlite3.Error as e:
            print(f"✗ Erreur réinitialisation: {e}")
            return False


def test_database():
    """Teste le module DatabaseManager"""
    print("\n=== TEST DatabaseManager ===")
    
    db = DatabaseManager("test_simulation.db")
    
    if db.connect():
        print("\n1. Test insertion événements:")
        
        # Insérer différents types d'événements
        db.insert_event("SIMULATION", "Démarrage", scenario="normal")
        db.insert_event("TRAFFIC_LIGHT", "ROUGE -> VERT", etat_feu="VERT", scenario="normal")
        db.insert_event("VEHICLE", "Création", id_voiture=1, position_x=100.5, position_y=50.2, vitesse=2.3)
        db.insert_event("SCENARIO", "normal -> rush_hour", scenario="rush_hour")
        
        print("\n2. Test récupération événements:")
        events = db.get_all_events(10)
        print(f"  {len(events)} événements récupérés")
        
        for event in events[:3]:  # Afficher les 3 premiers
            print(f"  - {event[2]}: {event[3]}")
        
        print("\n3. Test statistiques:")
        stats = db.get_statistics()
        print(f"  Total événements: {stats.get('total_events', 0)}")
        print(f"  Événements par type: {stats.get('events_by_type', {})}")
        
        print("\n4. Test réinitialisation:")
        db.reset_database()
        
        db.disconnect()
        print("\n✓ Tests DatabaseManager terminés")
    else:
        print("✗ Échec connexion base de données")


if __name__ == "__main__":
    test_database()