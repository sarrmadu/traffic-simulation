"""
Module de gestion des feux tricolores - Suite
Responsable : Mbene Diagne
"""

import time
from enum import Enum
from typing import Tuple, Optional
import turtle

class TrafficLightState(Enum):
    """États du feu tricolore"""
    RED = "ROUGE"
    ORANGE = "ORANGE"
    GREEN = "VERT"
    ORANGE_BLINKING = "ORANGE_CLIGNOTANT"

class TrafficLight:
    """Représente un feu tricolore avec graphisme"""
    
    def __init__(self, position: Tuple[float, float], direction: str = "north"):
        """
        Initialise un feu tricolore
        
        Args:
            position: Position (x, y) du feu
            direction: Direction du feu (north, south, east, west)
        """
        self.position = position
        self.direction = direction
        self.state = TrafficLightState.RED
        self.last_change_time = time.time()
        self.is_blinking = False
        self.blink_on = True
        self.last_blink_time = time.time()
        
        # Graphisme
        self.light_radius = 15
        self.light_spacing = 40
        self.pen = None
        self._init_graphics()
        
        print(f"✓ Feu {direction} créé à {position}")
    
    def _init_graphics(self) -> None:
        """Initialise le stylo Turtle pour ce feu"""
        self.pen = turtle.Turtle()
        self.pen.hideturtle()
        self.pen.speed(0)
        self.pen.penup()
    
    def draw(self) -> None:
        """Dessine le feu avec son état actuel"""
        x, y = self.position
        
        # Effacer l'ancien dessin
        self.pen.clear()
        
        # Dessiner le support
        self.pen.goto(x - 25, y - 100)
        self.pen.pendown()
        self.pen.fillcolor("#404040")
        self.pen.begin_fill()
        
        for _ in range(2):
            self.pen.forward(50)
            self.pen.left(90)
            self.pen.forward(150)
            self.pen.left(90)
        
        self.pen.end_fill()
        self.pen.penup()
        
        # Déterminer les couleurs selon l'état
        if self.is_blinking:
            red_color = "#404040"    # Éteint
            orange_color = "#FFA500" if self.blink_on else "#404040"
            green_color = "#404040"  # Éteint
        else:
            red_color = "#FF0000" if self.state == TrafficLightState.RED else "#404040"
            orange_color = "#FFA500" if self.state == TrafficLightState.ORANGE else "#404040"
            green_color = "#00FF00" if self.state == TrafficLightState.GREEN else "#404040"
        
        # Dessiner les trois feux
        lights = [
            (x, y + 40, red_color),      # Rouge en haut
            (x, y, orange_color),        # Orange au milieu
            (x, y - 40, green_color)     # Vert en bas
        ]
        
        for light_x, light_y, color in lights:
            self._draw_light(light_x, light_y, color)
    
    def _draw_light(self, x: float, y: float, color: str) -> None:
        """Dessine une lumière individuelle"""
        self.pen.goto(x, y - self.light_radius)
        self.pen.pendown()
        
        self.pen.fillcolor(color)
        self.pen.begin_fill()
        self.pen.circle(self.light_radius)
        self.pen.end_fill()
        self.pen.penup()
    
    def update(self, scenario_durations: dict) -> bool:
        """
        Met à jour l'état du feu selon le scénario
        
        Args:
            scenario_durations: Durées du scénario actuel
        
        Returns:
            True si l'état a changé, False sinon
        """
        current_time = time.time()
        
        if self.is_blinking:
            # Mode clignotant (nuit)
            if current_time - self.last_blink_time >= scenario_durations.get("blink_interval", 1.0):
                self.blink_on = not self.blink_on
                self.last_blink_time = current_time
                self.draw()
                return True
        else:
            # Cycle normal
            elapsed = current_time - self.last_change_time
            
            if self.state == TrafficLightState.GREEN:
                if elapsed >= scenario_durations.get("green", 10):
                    self.change_state(TrafficLightState.ORANGE)
                    return True
            
            elif self.state == TrafficLightState.ORANGE:
                if elapsed >= scenario_durations.get("orange", 3):
                    self.change_state(TrafficLightState.RED)
                    return True
            
            elif self.state == TrafficLightState.RED:
                if elapsed >= scenario_durations.get("red", 8):
                    self.change_state(TrafficLightState.GREEN)
                    return True
        
        return False
    
    def change_state(self, new_state: TrafficLightState, manual: bool = False) -> str:
        """
        Change l'état du feu
        
        Args:
            new_state: Nouvel état
            manual: True si changement manuel
        
        Returns:
            Ancien état
        """
        old_state = self.state.value
        self.state = new_state
        self.last_change_time = time.time()
        
        # Gérer le clignotement
        self.is_blinking = (new_state == TrafficLightState.ORANGE_BLINKING)
        
        # Redessiner
        self.draw()
        
        action = "manuel" if manual else "automatique"
        print(f"Feu {self.direction}: {old_state} → {new_state.value} ({action})")
        
        return old_state
    
    def set_blinking_mode(self, enable: bool) -> None:
        """Active/désactive le mode clignotant"""
        self.is_blinking = enable
        if enable:
            self.state = TrafficLightState.ORANGE_BLINKING
        self.draw()
    
    def get_current_state(self) -> str:
        """Retourne l'état actuel"""
        if self.is_blinking:
            return "ORANGE_CLIGNOTANT"
        return self.state.value
    
    def get_color(self) -> str:
        """Retourne la couleur actuelle principale"""
        if self.is_blinking:
            return "orange" if self.blink_on else "gray"
        
        colors = {
            TrafficLightState.RED: "red",
            TrafficLightState.ORANGE: "orange",
            TrafficLightState.GREEN: "green"
        }
        return colors.get(self.state, "gray")


class TrafficLightManager:
    """Gère tous les feux du carrefour"""
    
    def __init__(self):
        self.lights = {}
        self._initialize_lights()
    
    def _initialize_lights(self) -> None:
        """Initialise les 4 feux du carrefour"""
        positions = {
            "north": (0, 200),
            "south": (0, -200),
            "east": (200, 0),
            "west": (-200, 0)
        }
        
        for direction, position in positions.items():
            self.lights[direction] = TrafficLight(position, direction)
        
        print("✓ 4 feux tricolores initialisés")
    
    def update_all(self, scenario_durations: dict) -> None:
        """Met à jour tous les feux"""
        for light in self.lights.values():
            light.update(scenario_durations)
    
    def change_all_states(self, state: TrafficLightState, manual: bool = False) -> None:
        """Change l'état de tous les feux"""
        for light in self.lights.values():
            light.change_state(state, manual)
    
    def set_all_blinking(self, enable: bool) -> None:
        """Active/désactive le clignotement pour tous les feux"""
        for light in self.lights.values():
            light.set_blinking_mode(enable)
    
    def get_light(self, direction: str) -> Optional[TrafficLight]:
        """Retourne un feu spécifique"""
        return self.lights.get(direction)
    
    def get_current_states(self) -> dict:
        """Retourne l'état de tous les feux"""
        return {direction: light.get_current_state() 
                for direction, light in self.lights.items()}


def test_traffic_light():
    """Teste le module TrafficLight"""
    print("\n=== TEST TrafficLight ===")
    
    # Créer un écran Turtle
    screen = turtle.Screen()
    screen.setup(800, 600)
    screen.title("Test Feux Tricolores")
    screen.bgcolor("#87CEEB")
    screen.tracer(0)
    
    # Créer un gestionnaire de feux
    manager = TrafficLightManager()
    
    # Tester le changement d'état
    print("\nTest changement manuel:")
    manager.change_all_states(TrafficLightState.RED, manual=True)
    time.sleep(1)
    
    manager.change_all_states(TrafficLightState.GREEN, manual=True)
    time.sleep(1)
    
    manager.change_all_states(TrafficLightState.ORANGE, manual=True)
    time.sleep(1)
    
    print("\nTest mode clignotant:")
    manager.set_all_blinking(True)
    time.sleep(3)
    
    manager.set_all_blinking(False)
    
    print("\n✓ Tests TrafficLight terminés")
    print("Fermez la fenêtre Turtle pour continuer...")
    
    screen.mainloop()


if __name__ == "__main__":
    test_traffic_light()