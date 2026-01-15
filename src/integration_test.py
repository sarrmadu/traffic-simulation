"""
Test d'intégration complet
Responsable : Mbene Diagne
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from road_scene import RoadScene
from traffic_light import TrafficLightManager
from vehicle import VehicleManagerGraphic, VehicleType
import turtle
import time

def test_integration_complete():
    """Test d'intégration complet des graphiques"""
    print("\n=== TEST INTÉGRATION COMPLÈTE ===")
    
    # 1. Initialiser la scène
    print("1. Initialisation RoadScene...")
    scene = RoadScene()
    if not scene.setup():
        print("✗ Échec initialisation RoadScene")
        return
    
    scene.draw_road_network()
    print("✓ Carrefour dessiné")
    
    # 2. Initialiser les feux
    print("\n2. Initialisation TrafficLightManager...")
    traffic_manager = TrafficLightManager()
    
    # Dessiner les feux
    for direction, light in traffic_manager.lights.items():
        light.draw()
    
    scene.update_display()
    print("✓ Feux tricolores dessinés")
    
    # 3. Initialiser les véhicules
    print("\n3. Initialisation VehicleManagerGraphic...")
    vehicle_manager = VehicleManagerGraphic()
    scene.setup_vehicle_manager(vehicle_manager)
    
    # Créer quelques véhicules
    print("\n4. Création et animation des véhicules...")
    
    # Créer des véhicules à différentes positions
    vehicle_ids = []
    
    # Voiture venant de l'ouest (droite)
    car1_id = vehicle_manager.create_vehicle(VehicleType.CAR)
    vehicle_manager.draw_vehicle(car1_id, (-300, -50), "east")
    vehicle_ids.append(car1_id)
    
    # Camion venant de l'est (gauche)
    truck_id = vehicle_manager.create_vehicle(VehicleType.TRUCK)
    vehicle_manager.draw_vehicle(truck_id, (300, 50), "west")
    vehicle_ids.append(truck_id)
    
    # Voiture venant du sud (bas)
    car2_id = vehicle_manager.create_vehicle(VehicleType.CAR)
    vehicle_manager.draw_vehicle(car2_id, (-50, -250), "north")
    vehicle_ids.append(car2_id)
    
    scene.update_display()
    print(f"✓ {len(vehicle_ids)} véhicules créés")
    
    # 5. Animation des véhicules
    print("\n5. Démonstration animation...")
    print("   Les véhicules vont avancer pendant 5 secondes")
    
    start_time = time.time()
    while time.time() - start_time < 5:
        # Déplacer la voiture venant de l'ouest
        for i, vid in enumerate(vehicle_ids):
            if vid == car1_id:
                # Avancer vers l'est
                current_pos = vehicle_manager.vehicles[vid].position
                new_pos = (current_pos[0] + 2, current_pos[1])
                vehicle_manager.move_vehicle(vid, new_pos)
            
            elif vid == truck_id:
                # Avancer vers l'ouest
                current_pos = vehicle_manager.vehicles[vid].position
                new_pos = (current_pos[0] - 1.5, current_pos[1])
                vehicle_manager.move_vehicle(vid, new_pos)
            
            elif vid == car2_id:
                # Avancer vers le nord
                current_pos = vehicle_manager.vehicles[vid].position
                new_pos = (current_pos[0], current_pos[1] + 2)
                vehicle_manager.move_vehicle(vid, new_pos)
        
        # Mettre à jour l'affichage
        scene.update_display()
        time.sleep(0.05)
    
    # 6. Changement des feux
    print("\n6. Démonstration changement feux...")
    
    print("   Feu ROUGE pendant 2 secondes...")
    traffic_manager.change_all_states("RED", manual=True)
    scene.update_display()
    time.sleep(2)
    
    print("   Feu VERT pendant 2 secondes...")
    traffic_manager.change_all_states("GREEN", manual=True)
    scene.update_display()
    time.sleep(2)
    
    print("   Feu ORANGE pendant 1 seconde...")
    traffic_manager.change_all_states("ORANGE", manual=True)
    scene.update_display()
    time.sleep(1)
    
    print("\n✓ Test d'intégration terminé avec succès!")
    print("\nAppuyez sur Entrée dans la fenêtre Turtle pour quitter...")
    
    # Garder la fenêtre ouverte
    scene.screen.mainloop()
    scene.close()

if __name__ == "__main__":
    test_integration_complete()