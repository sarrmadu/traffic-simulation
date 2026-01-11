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
        
        # Dessiner l'herbe (fond vert)
        self._draw_grass()
        
        # Dessiner les routes
        self._draw_horizontal_road()
        self._draw_vertical_road()
        
        # Dessiner l'intersection
        self._draw_intersection()
        
        # Mettre à jour l'affichage
        self.screen.update()
        print("✓ Réseau routier dessiné")
    
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