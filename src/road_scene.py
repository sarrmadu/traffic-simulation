"""
Module de dessin du carrefour routier avec Turtle
Responsable : Mbene Diagne
"""

import turtle
from typing import Tuple
import time

class RoadScene:
    """Gère l'affichage graphique du carrefour"""
    
    def __init__(self):
        self.screen = None
        self.pen = None
        self.initialized = False
        print("✓ RoadScene initialisé")
    
    def setup(self) -> bool:
        """Configure l'environnement Turtle"""
        try:
            # Créer l'écran
            self.screen = turtle.Screen()
            self.screen.setup(width=1000, height=800)
            self.screen.title("Simulation Feu Tricolore")
            self.screen.bgcolor("#87CEEB")  # Bleu ciel
            self.screen.tracer(0)  # Désactiver animation auto
            
            # Créer le stylo
            self.pen = turtle.Turtle()
            self.pen.hideturtle()
            self.pen.speed(0)
            self.pen.penup()
            
            self.initialized = True
            print("✓ Turtle configuré")
            return True
            
        except Exception as e:
            print(f"✗ Erreur configuration Turtle: {e}")
            return False
    
    def draw_road_network(self) -> None:
        """Dessine l'ensemble du réseau routier"""
        if not self.initialized:
            print("Erreur: RoadScene non initialisé")
            return
        
        print("Dessin du réseau routier...")
        
        # Effacer l'écran
        self.pen.clear()
        
        # Dessiner dans l'ordre
        self._draw_grass()
        self._draw_horizontal_road()
        self._draw_vertical_road()
        self._draw_intersection()
        self._draw_road_markings()  # NOUVEAU !
        
        # Mettre à jour l'affichage
        self.screen.update()
        print("✓ Réseau routier dessiné avec marquages")
    
    def _draw_grass(self) -> None:
        """Dessine l'herbe autour des routes"""
        self.pen.penup()
        self.pen.goto(-500, -400)
        self.pen.pendown()
        
        self.pen.fillcolor("#90EE90")  # Vert clair
        self.pen.begin_fill()
        
        for _ in range(2):
            self.pen.forward(1000)
            self.pen.left(90)
            self.pen.forward(800)
            self.pen.left(90)
        
        self.pen.end_fill()
        self.pen.penup()
    
    def _draw_horizontal_road(self) -> None:
        """Dessine la route horizontale"""
        self.pen.penup()
        self.pen.goto(-500, -150)
        self.pen.pendown()
        
        self.pen.fillcolor("#696969")  # Gris foncé
        self.pen.begin_fill()
        
        # Rectangle de la route
        self.pen.goto(500, -150)
        self.pen.goto(500, 150)
        self.pen.goto(-500, 150)
        self.pen.goto(-500, -150)
        
        self.pen.end_fill()
        self.pen.penup()
    
    def _draw_vertical_road(self) -> None:
        """Dessine la route verticale"""
        self.pen.penup()
        self.pen.goto(-150, -400)
        self.pen.pendown()
        
        self.pen.fillcolor("#696969")  # Gris foncé
        self.pen.begin_fill()
        
        # Rectangle de la route
        self.pen.goto(150, -400)
        self.pen.goto(150, 400)
        self.pen.goto(-150, 400)
        self.pen.goto(-150, -400)
        
        self.pen.end_fill()
        self.pen.penup()
    
    def _draw_intersection(self) -> None:
        """Dessine l'intersection centrale"""
        self.pen.penup()
        self.pen.goto(-150, -150)
        self.pen.pendown()
        
        self.pen.fillcolor("#696969")
        self.pen.begin_fill()
        
        # Carré de l'intersection
        for _ in range(4):
            self.pen.forward(300)
            self.pen.left(90)
        
        self.pen.end_fill()
        self.pen.penup()
    
    def update_display(self) -> None:
        """Met à jour l'affichage"""
        if self.screen:
            self.screen.update()
    
    def close(self) -> None:
        """Ferme la fenêtre"""
        if self.screen:
            self.screen.bye()
        print("✓ RoadScene fermé")
    def _draw_road_markings(self) -> None:
        """Dessine les marquages au sol (lignes)"""
        self.pen.color("#FFFFFF")  # Blanc
        self.pen.width(2)
        
        # Ligne centrale horizontale (pointillés)
        self._draw_dashed_line((-500, 0), (500, 0))
        
        # Ligne centrale verticale (pointillés)
        self._draw_dashed_line((0, -400), (0, 400))
        
        # Lignes de séparation de voies
        self._draw_dashed_line((-500, -100), (500, -100))
        self._draw_dashed_line((-500, 100), (500, 100))
        self._draw_dashed_line((-100, -400), (-100, 400))
        self._draw_dashed_line((100, -400), (100, 400))
    
    def _draw_dashed_line(self, start: tuple, end: tuple) -> None:
        """Dessine une ligne en pointillés"""
        x1, y1 = start
        x2, y2 = end
        
        # Calculer la distance et le nombre de segments
        distance = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
        dash_count = int(distance / 20)
        
        # Calculer l'incrément
        dx = (x2 - x1) / dash_count
        dy = (y2 - y1) / dash_count
        
        self.pen.penup()
        self.pen.goto(x1, y1)
        
        for i in range(dash_count):
            if i % 2 == 0:  # Segment visible
                self.pen.pendown()
            else:  # Espace
                self.pen.penup()
            
            self.pen.goto(x1 + dx * (i + 1), y1 + dy * (i + 1))
        
        self.pen.penup()

    def setup_vehicle_manager(self, vehicle_manager_graphic):
        """
        Configure le gestionnaire de véhicules graphiques
        
        Args:
            vehicle_manager_graphic: Instance de VehicleManagerGraphic
        """
        self.vehicle_manager_graphic = vehicle_manager_graphic
        print("✓ Gestionnaire de véhicules connecté à RoadScene")
    
    def update_vehicles(self) -> None:
        """Met à jour l'affichage de tous les véhicules"""
        if hasattr(self, 'vehicle_manager_graphic') and self.vehicle_manager_graphic:
            # Cette méthode sera appelée par la simulation
            # Les véhicules sont déjà dessinés par leur propre Turtle
            pass
    
    def clear_all_vehicles(self) -> None:
        """Efface tous les véhicules de l'écran"""
        if hasattr(self, 'vehicle_manager_graphic') and self.vehicle_manager_graphic:
            self.vehicle_manager_graphic.clear_all_vehicles()


def test_road_scene():
    """Teste le module RoadScene"""
    print("\n=== TEST RoadScene ===")
    scene = RoadScene()
    
    if scene.setup():
        scene.draw_road_network()
        print("✓ Test réussi! Le carrefour est dessiné.")
        print("\nAppuyez sur Entrée dans la fenêtre Turtle pour quitter...")
        
        # Garder la fenêtre ouverte
        scene.screen.mainloop()
        scene.close()
    else:
        print("✗ Test échoué")


if __name__ == "__main__":
    test_road_scene()