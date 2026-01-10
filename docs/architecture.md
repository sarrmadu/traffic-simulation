
## architecture.md**

```python
"""
Architecture du système - Simulation Feu Tricolore
==================================================

Ce document décrit l'architecture logicielle du système de simulation de feu tricolore.

## 1. Vue d'ensemble

L'application est structurée en plusieurs modules Python qui communiquent entre eux :

voire image architecture.png

## 2. Détails des modules

### 2.1 main.py
Point d'entrée de l'application. Responsable de :
- Initialisation de tous les composants
- Gestion du cycle de vie de l'application
- Coordination entre les modules

### 2.2 simulation.py
Moteur principal de simulation. Responsable de :
- Boucle principale de simulation
- Synchronisation des composants
- Gestion du temps virtuel
- Coordination entre feux et véhicules

### 2.3 gui.py
Interface utilisateur. Responsable de :
- Fenêtre principale Tkinter
- Boutons de contrôle (Play/Pause/Stop/Réinitialiser)
- Sélecteur de scénarios
- Affichage des indicateurs d'état

### 2.4 road_scene.py
Gestion graphique du carrefour. Responsable de :
- Dessin des routes et intersections
- Marquages au sol
- Environnement (trottoirs, herbe)
- Mise à jour de l'affichage

### 2.5 traffic_light.py
Logique des feux tricolores. Responsable de :
- États du feu (ROUGE/ORANGE/VERT)
- Cycles automatiques
- Contrôle manuel
- Durées configurables par scénario

### 2.6 vehicle.py
Gestion des véhicules. Responsable de :
- Création et suppression des véhicules
- Mouvement et animation
- Réaction aux feux
- Comportement selon le scénario

### 2.7 scenario_manager.py
Gestion des scénarios. Responsable de :
- 4 scénarios de circulation
- Paramètres par scénario
- Transition entre scénarios
- Adaptation du comportement du système

### 2.8 database.py
Gestion des données. Responsable de :
- Connexion SQLite
- Schéma de base de données
- CRUD des événements
- Requêtes d'analyse

### 2.9 logger.py
Journalisation. Responsable de :
- Enregistrement des événements
- Catégorisation des logs
- Persistance dans la base de données
- Formatage des messages

## 3. Flux de données

### 3.1 Initialisation
1. main.py crée les instances des modules
2. Initialisation de la base de données
3. Configuration des scénarios
4. Création de l'interface graphique

### 3.2 Boucle de simulation
1. simulation.py met à jour l'état du système
2. traffic_light.py met à jour les feux
3. vehicle.py met à jour les véhicules
4. road_scene.py redessine la scène
5. gui.py met à jour l'interface
6. logger.py enregistre les événements

### 3.3 Interaction utilisateur
1. L'utilisateur clique sur un bouton
2. gui.py envoie l'événement à simulation.py
3. simulation.py met à jour l'état correspondant
4. Les autres modules sont notifiés du changement
5. L'interface est mise à jour

## 4. Modèle de classes

### 4.1 Simulation
Classe principale qui orchestre tous les composants.

### 4.2 TrafficLight
Représente un feu tricolore avec ses états et transitions.

### 4.3 Vehicle
Représente un véhicule avec son comportement et son affichage.

### 4.4 Scenario
Classe abstraite pour les différents scénarios.

### 4.5 RoadNetwork
Représente le réseau routier du carrefour.

### 4.6 DatabaseManager
Gère la connexion et les opérations SQLite.

### 4.7 EventLogger
Gère la journalisation des événements.

## 5. Communications inter-modules

### 5.1 Pattern Observer
Les modules s'abonnent aux événements qui les concernent.

### 5.2 Événements principaux
- SIMULATION_STARTED
- SIMULATION_PAUSED
- SIMULATION_STOPPED
- TRAFFIC_LIGHT_CHANGED
- VEHICLE_CREATED
- VEHICLE_REMOVED
- SCENARIO_CHANGED

### 5.3 Synchronisation
Tous les modules utilisent le même horodatage de simulation.

## 6. Considérations de performance

### 6.1 Animation
- Utilisation de Turtle avec tracer(0) pour performance
- Mise à jour différentielle (seulement ce qui change)
- Limitation du nombre de véhicules simultanés

### 6.2 Base de données
- Transactions groupées pour performance
- Index sur les colonnes fréquemment interrogées
- Archivage des vieux événements

### 6.3 Mémoire
- Pool d'objets véhicules réutilisables
- Nettoyage régulier des ressources
- Limitation de la profondeur d'historique

## 7. Extensibilité

### 7.1 Nouveaux scénarios
Ajouter une nouvelle classe héritant de Scenario.

### 7.2 Nouveaux types de véhicules
Ajouter une nouvelle classe héritant de Vehicle.

### 7.3 Nouveaux indicateurs
Ajouter de nouveaux widgets dans gui.py.

### 7.4 Export de données
Ajouter des méthodes dans database.py.

## 8. Limitations connues

### 8.1 Limitations techniques
- Nombre maximum de véhicules : 50
- Résolution fixe : 1000x800
- Base de données : SQLite uniquement

### 8.2 Limitations fonctionnelles
- Pas de détection de collisions
- Pas de piétons
- Pas de conditions météo

## 9. Dépendances

### 9.1 Requises (standard library)
- tkinter
- turtle
- sqlite3
- threading
- time
- random

### 9.2 Optionnelles
- pytest (pour les tests)
- black (pour le formatage)
- flake8 (pour le linting)

## 10. Schéma de base de données

Voir database.py pour le schéma complet.
"""