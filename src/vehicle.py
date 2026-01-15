"""
Module de gestion des véhicules - Partie Graphique
Responsable : Mbene Diagne
"""

import turtle
import random
from typing import Tuple, List, Optional
from enum import Enum
from constants import *  # Importez toutes les constantes

class VehicleType(Enum):
    """Types de véhicules"""
    CAR = "car"
    TRUCK = "truck"

class VehicleGraphic:
    """Représente un véhicule (partie graphique)"""
    
    def __init__(self, vehicle_id: int, vehicle_type: VehicleType = VehicleType.CAR):
        """
        Initialise un véhicule graphique
        
        Args:
            vehicle_id: Identifiant unique du véhicule
            vehicle_type: Type de véhicule
        """
        self.id = vehicle_id
        self.type = vehicle_type
        self.position = (0, 0)
        self.direction = "east"
        self.color = self._get_random_color()
        self.width, self.height = self._get_dimensions()
        
        # État graphique
        self.pen = None
        self.visible = False
        self._init_graphics()
        
        print(f"✓ Véhicule #{self.id} créé ({self.type.value})")
    
    def _init_graphics(self) -> None:
        """Initialise le stylo Turtle pour ce véhicule"""
        self.pen = turtle.Turtle()
        self.pen.hideturtle()
        self.pen.speed(0)
        self.pen.penup()
    
    def _get_random_color(self) -> str:
        """Retourne une couleur aléatoire"""
        if self.type == VehicleType.CAR:
            return random.choice(CAR_COLORS)
        else:  # TRUCK
            return random.choice(TRUCK_COLORS)
    
    def _get_dimensions(self) -> Tuple[float, float]:
        """Retourne les dimensions selon le type"""
        # CORRECTION ICI : Utiliser VEHICLE_CONFIG au lieu de CAR_WIDTH, etc.
        if self.type == VehicleType.CAR:
            config = VEHICLE_CONFIG["car"]
            return (config["width"], config["height"])
        else:  # TRUCK
            config = VEHICLE_CONFIG["truck"]
            return (config["width"], config["height"])
    
    def draw(self, position: Tuple[float, float], direction: str) -> None:
        """
        Dessine le véhicule à la position donnée
        
        Args:
            position: Position (x, y) du véhicule
            direction: Direction du véhicule
        """
        self.position = position
        self.direction = direction
        
        # Effacer l'ancien dessin
        self.pen.clear()
        
        # Calculer les points du rectangle selon la direction
        points = self._calculate_shape_points()
        
        # Dessiner le corps du véhicule
        self.pen.penup()
        self.pen.goto(points[0])
        self.pen.pendown()
        
        self.pen.fillcolor(self.color)
        self.pen.begin_fill()
        
        for point in points[1:]:
            self.pen.goto(point)
        
        self.pen.goto(points[0])
        self.pen.end_fill()
        
        # Dessiner les vitres
        self._draw_windows()
        
        self.visible = True
    
    def _calculate_shape_points(self) -> List[Tuple[float, float]]:
        """Calcule les points du véhicule selon sa direction"""
        x, y = self.position
        half_width = self.width / 2
        half_height = self.height / 2
        
        if self.direction in ["east", "west"]:
            # Véhicule horizontal
            if self.direction == "east":
                # Vers l'est (droite)
                points = [
                    (x - half_width, y - half_height),  # Bas gauche
                    (x + half_width, y - half_height),  # Bas droit
                    (x + half_width * 0.7, y + half_height),  # Haut droit
                    (x - half_width * 0.7, y + half_height),  # Haut gauche
                ]
            else:  # west
                # Vers l'ouest (gauche)
                points = [
                    (x + half_width, y - half_height),  # Bas droit
                    (x - half_width, y - half_height),  # Bas gauche
                    (x - half_width * 0.7, y + half_height),  # Haut gauche
                    (x + half_width * 0.7, y + half_height),  # Haut droit
                ]
        else:
            # Véhicule vertical
            if self.direction == "north":
                # Vers le nord (haut)
                points = [
                    (x - half_height, y - half_width),  # Bas gauche
                    (x - half_height, y + half_width),  # Haut gauche
                    (x + half_height, y + half_width * 0.7),  # Haut droit
                    (x + half_height, y - half_width * 0.7),  # Bas droit
                ]
            else:  # south
                # Vers le sud (bas)
                points = [
                    (x - half_height, y + half_width),  # Haut gauche
                    (x - half_height, y - half_width),  # Bas gauche
                    (x + half_height, y - half_width * 0.7),  # Bas droit
                    (x + half_height, y + half_width * 0.7),  # Haut droit
                ]
        
        return points
    
    def _draw_windows(self) -> None:
        """Dessine les vitres du véhicule"""
        x, y = self.position
        half_width = self.width / 2
        half_height = self.height / 2
        
        self.pen.fillcolor("#ADD8E6")  # Bleu clair pour vitres
        self.pen.begin_fill()
        
        if self.direction in ["east", "west"]:
            # Vitres pour véhicule horizontal
            if self.direction == "east":
                self.pen.goto(x - half_width * 0.5, y - half_height * 0.8)
                self.pen.goto(x + half_width * 0.2, y - half_height * 0.8)
                self.pen.goto(x + half_width * 0.2, y + half_height * 0.8)
                self.pen.goto(x - half_width * 0.5, y + half_height * 0.8)
                self.pen.goto(x - half_width * 0.5, y - half_height * 0.8)
            else:  # west
                self.pen.goto(x + half_width * 0.5, y - half_height * 0.8)
                self.pen.goto(x - half_width * 0.2, y - half_height * 0.8)
                self.pen.goto(x - half_width * 0.2, y + half_height * 0.8)
                self.pen.goto(x + half_width * 0.5, y + half_height * 0.8)
                self.pen.goto(x + half_width * 0.5, y - half_height * 0.8)
        else:
            # Vitres pour véhicule vertical
            if self.direction == "north":
                self.pen.goto(x - half_height * 0.8, y - half_width * 0.5)
                self.pen.goto(x - half_height * 0.8, y + half_width * 0.2)
                self.pen.goto(x + half_height * 0.8, y + half_width * 0.2)
                self.pen.goto(x + half_height * 0.8, y - half_width * 0.5)
                self.pen.goto(x - half_height * 0.8, y - half_width * 0.5)
            else:  # south
                self.pen.goto(x - half_height * 0.8, y + half_width * 0.5)
                self.pen.goto(x - half_height * 0.8, y - half_width * 0.2)
                self.pen.goto(x + half_height * 0.8, y - half_width * 0.2)
                self.pen.goto(x + half_height * 0.8, y + half_width * 0.5)
                self.pen.goto(x - half_height * 0.8, y + half_width * 0.5)
        
        self.pen.end_fill()
    
    def erase(self) -> None:
        """Efface le véhicule de l'écran"""
        if self.visible:
            self.pen.clear()
            self.visible = False
    
    def move(self, new_position: Tuple[float, float]) -> None:
        """
        Déplace le véhicule à une nouvelle position
        
        Args:
            new_position: Nouvelle position (x, y)
        """
        if self.visible:
            self.erase()
        self.draw(new_position, self.direction)
    
    def change_direction(self, new_direction: str) -> None:
        """
        Change la direction du véhicule
        
        Args:
            new_direction: Nouvelle direction
        """
        if self.direction != new_direction:
            self.direction = new_direction
            if self.visible:
                self.draw(self.position, new_direction)
    
    def hide(self) -> None:
        """Cache le véhicule"""
        self.pen.hideturtle()
    
    def show(self) -> None:
        """Affiche le véhicule"""
        self.pen.showturtle()


class VehicleManagerGraphic:
    """Gère tous les véhicules graphiques"""
    
    def __init__(self, screen=None):
        """
        Initialise le gestionnaire graphique
        
        Args:
            screen: Écran Turtle (optionnel)
        """
        self.vehicles = {}  # vehicle_id -> VehicleGraphic
        self.next_id = 1
        self.screen = screen
        self.behavior_manager = None  # Ajouter cette ligne

    
    def create_vehicle(self, vehicle_type: VehicleType = VehicleType.CAR) -> int:
        """
        Crée un nouveau véhicule graphique
        
        Returns:
            ID du véhicule créé
        """
        vehicle_id = self.next_id
        self.next_id += 1
        
        vehicle = VehicleGraphic(vehicle_id, vehicle_type)
        self.vehicles[vehicle_id] = vehicle
        
        return vehicle_id
    
    def draw_vehicle(self, vehicle_id: int, position: Tuple[float, float], direction: str) -> None:
        """Dessine un véhicule spécifique"""
        if vehicle_id in self.vehicles:
            self.vehicles[vehicle_id].draw(position, direction)
            self._update_screen()
    
    def move_vehicle(self, vehicle_id: int, new_position: Tuple[float, float]) -> None:
        """Déplace un véhicule"""
        if vehicle_id in self.vehicles:
            self.vehicles[vehicle_id].move(new_position)
            self._update_screen()
    
    def change_vehicle_direction(self, vehicle_id: int, new_direction: str) -> None:
        """Change la direction d'un véhicule"""
        if vehicle_id in self.vehicles:
            self.vehicles[vehicle_id].change_direction(new_direction)
            self._update_screen()
    
    def remove_vehicle(self, vehicle_id: int) -> None:
        """Supprime un véhicule"""
        if vehicle_id in self.vehicles:
            self.vehicles[vehicle_id].erase()
            del self.vehicles[vehicle_id]
            self._update_screen()
    
    def clear_all_vehicles(self) -> None:
        """Supprime tous les véhicules"""
        for vehicle_id in list(self.vehicles.keys()):
            self.remove_vehicle(vehicle_id)
    
    def get_vehicle_count(self) -> int:
        """Retourne le nombre de véhicules actifs"""
        return len(self.vehicles)
    
    def get_vehicle(self, vehicle_id: int) -> Optional[VehicleGraphic]:
        """Retourne un véhicule spécifique"""
        return self.vehicles.get(vehicle_id)
    
    def _update_screen(self):
        """Met à jour l'écran si disponible"""
        if self.screen:
            self.screen.update()
    
    def setup(self, screen) -> bool:
        """
        Configure le gestionnaire avec un écran
        
        Args:
            screen: Écran Turtle
            
        Returns:
            bool: True si succès
        """
        try:
            self.screen = screen
            return True
        except Exception as e:
            print(f"✗ Erreur configuration VehicleManagerGraphic: {e}")
            return False


def test_vehicle_graphics():
    """Teste les graphiques des véhicules"""
    print("\n=== TEST Vehicle Graphics ===")
    
    try:
        # Créer un écran Turtle
        screen = turtle.Screen()
        screen.setup(SCREEN_WIDTH, SCREEN_HEIGHT)  # Utiliser les constantes
        screen.title("Test Véhicules Graphiques - Ville de Thiès")
        screen.bgcolor(BACKGROUND_COLOR)  # Utiliser la constante
        screen.tracer(0)  # Désactive l'animation automatique
        
        manager = VehicleManagerGraphic(screen)
        
        print("\n1. Test création véhicules:")
        
        # Créer quelques véhicules
        car1_id = manager.create_vehicle(VehicleType.CAR)
        car2_id = manager.create_vehicle(VehicleType.CAR)
        truck_id = manager.create_vehicle(VehicleType.TRUCK)
        
        print(f"  ✓ {manager.get_vehicle_count()} véhicules créés")
        
        print("\n2. Test dessin véhicules:")
        
        # Dessiner les véhicules à différentes positions
        manager.draw_vehicle(car1_id, (-200, 0), "east")
        manager.draw_vehicle(car2_id, (200, 0), "west")
        manager.draw_vehicle(truck_id, (0, 100), "north")
        
        screen.update()
        print("  ✓ Véhicules dessinés")
        
        print("\n3. Test déplacement véhicules:")
        
        # Déplacer un véhicule
        print("  Déplacement véhicule #1 vers l'est...")
        for i in range(5):
            new_x = -200 + i * 40
            manager.move_vehicle(car1_id, (new_x, 0))
            turtle.time.sleep(0.3)  # Pause pour voir l'animation
        
        print("\n4. Test changement direction:")
        manager.change_vehicle_direction(car2_id, "north")
        turtle.time.sleep(1)
        
        print("\n5. Test suppression véhicules:")
        manager.remove_vehicle(car2_id)
        print(f"  ✓ Véhicule #{car2_id} supprimé")
        print(f"  Véhicules restants: {manager.get_vehicle_count()}")
        
        screen.update()
        
        print("\n✓ Tests Vehicle Graphics terminés")
        print("\n=== INSTRUCTIONS ===")
        print("1. La fenêtre Turtle doit rester ouverte")
        print("2. Cliquez sur la fenêtre pour la fermer")
        print("3. Ou appuyez sur 'q' dans la fenêtre")
        
        # Configurer la fermeture propre
        def close_window():
            print("\nFermeture de la fenêtre de test...")
            manager.clear_all_vehicles()
            screen.bye()
        
        # Configurer les événements clavier
        screen.onkey(close_window, "q")
        screen.onkey(close_window, "Q")
        screen.listen()
        
        # Garder la fenêtre ouverte
        screen.mainloop()
        
        print("\nTest terminé avec succès!")
        
    except Exception as e:
        print(f"\n✗ Erreur pendant le test: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        print("\n=== FIN TEST ===")


if __name__ == "__main__":
    test_vehicle_graphics()