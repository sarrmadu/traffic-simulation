"""
Module d'interface graphique utilisateur
Responsable : Modou Sarr
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Callable

class ControlInterface:
    """Interface de contrôle de la simulation"""
    
    def __init__(self, simulation_callback=None):
        """
        Initialise l'interface
        
        Args:
            simulation_callback: Fonction appelée pour contrôler la simulation
        """
        self.simulation_callback = simulation_callback
        self.root = None
        self.initialized = False
        
        # Variables d'état
        self.simulation_running = False
        self.simulation_paused = False
        self.current_scenario = "Circulation Normale"
        
        print("✓ ControlInterface initialisé")
    
    def setup(self) -> bool:
        """Configure l'interface"""
        try:
            # Créer la fenêtre principale
            self.root = tk.Tk()
            self.root.title("Contrôle Simulation - Ville de Thiès")
            self.root.geometry("400x500")
            self.root.resizable(False, False)
            
            # Configurer le style
            self._configure_style()
            
            # Créer les composants
            self._create_widgets()
            
            self.initialized = True
            print("✓ Interface configurée")
            return True
            
        except Exception as e:
            print(f"✗ Erreur configuration interface: {e}")
            return False
    
    def _configure_style(self) -> None:
        """Configure le style de l'interface"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Couleurs personnalisées
        self.colors = {
            'bg': '#F0F0F0',
            'fg': '#333333',
            'button_start': '#4CAF50',
            'button_pause': '#FF9800',
            'button_stop': '#F44336',
            'button_reset': '#2196F3',
            'frame_bg': '#E0E0E0'
        }
        
        self.root.configure(bg=self.colors['bg'])
    
    def _create_widgets(self) -> None:
        """Crée tous les widgets de l'interface"""
        
        # Titre
        title_frame = tk.Frame(self.root, bg=self.colors['bg'])
        title_frame.pack(pady=10)
        
        title = tk.Label(
            title_frame,
            text="🚦 CONTRÔLE SIMULATION",
            font=("Arial", 16, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['fg']
        )
        title.pack()
        
        # Boutons de simulation
        self._create_simulation_buttons()
        
        # Séparateur
        ttk.Separator(self.root, orient='horizontal').pack(fill='x', padx=20, pady=10)
        
        # Sélecteur de scénario
        self._create_scenario_selector()
        
        # Séparateur
        ttk.Separator(self.root, orient='horizontal').pack(fill='x', padx=20, pady=10)
        
        # Contrôles manuels (mode manuel)
        self._create_manual_controls()
        
        # Séparateur
        ttk.Separator(self.root, orient='horizontal').pack(fill='x', padx=20, pady=10)
        
        # Indicateurs d'état
        self._create_status_panel()
        
        # Bouton quitter
        self._create_quit_button()
    
    def _create_simulation_buttons(self) -> None:
        """Crée les boutons de contrôle de simulation"""
        frame = tk.Frame(self.root, bg=self.colors['frame_bg'], padx=10, pady=10)
        frame.pack(pady=5)
        
        # Bouton Démarrer
        self.btn_start = tk.Button(
            frame,
            text="▶ DÉMARRER",
            font=("Arial", 10, "bold"),
            bg=self.colors['button_start'],
            fg="white",
            width=12,
            height=2,
            command=self._on_start_clicked
        )
        self.btn_start.pack(side=tk.LEFT, padx=5)
        
        # Bouton Pause
        self.btn_pause = tk.Button(
            frame,
            text="⏸ PAUSE",
            font=("Arial", 10, "bold"),
            bg=self.colors['button_pause'],
            fg="white",
            width=12,
            height=2,
            command=self._on_pause_clicked,
            state=tk.DISABLED
        )
        self.btn_pause.pack(side=tk.LEFT, padx=5)
        
        # Bouton Arrêter
        self.btn_stop = tk.Button(
            frame,
            text="⏹ ARRÊTER",
            font=("Arial", 10, "bold"),
            bg=self.colors['button_stop'],
            fg="white",
            width=12,
            height=2,
            command=self._on_stop_clicked,
            state=tk.DISABLED
        )
        self.btn_stop.pack(side=tk.LEFT, padx=5)
        
        # Bouton Réinitialiser
        self.btn_reset = tk.Button(
            frame,
            text="↻ RÉINITIALISER",
            font=("Arial", 10, "bold"),
            bg=self.colors['button_reset'],
            fg="white",
            width=12,
            height=2,
            command=self._on_reset_clicked
        )
        self.btn_reset.pack(side=tk.LEFT, padx=5)
    
    def _create_scenario_selector(self) -> None:
        """Crée le sélecteur de scénario"""
        frame = tk.LabelFrame(
            self.root,
            text="📋 SCÉNARIO DE CIRCULATION",
            bg=self.colors['frame_bg'],
            padx=10,
            pady=10
        )
        frame.pack(padx=20, pady=5, fill='x')
        
        # Variable pour les boutons radio
        self.scenario_var = tk.StringVar(value=self.current_scenario)
        
        # Liste des scénarios
        scenarios = [
            ("Circulation Normale", "normal"),
            ("Heure de Pointe", "rush_hour"),
            ("Mode Nuit", "night"),
            ("Mode Manuel", "manual")
        ]
        
        for text, value in scenarios:
            rb = tk.Radiobutton(
                frame,
                text=text,
                variable=self.scenario_var,
                value=value,
                bg=self.colors['frame_bg'],
                command=self._on_scenario_changed
            )
            rb.pack(anchor='w', pady=2)
    
    def _create_manual_controls(self) -> None:
        """Crée les contrôles manuels (mode manuel)"""
        frame = tk.LabelFrame(
            self.root,
            text="🎮 CONTRÔLE MANUEL (Mode Manuel uniquement)",
            bg=self.colors['frame_bg'],
            padx=10,
            pady=10
        )
        frame.pack(padx=20, pady=5, fill='x')
        
        # Désactivés par défaut (activés seulement en mode manuel)
        self.btn_red = tk.Button(
            frame,
            text="🔴 FEU ROUGE",
            bg="#FF4444",
            fg="white",
            width=15,
            command=self._on_red_clicked,
            state=tk.DISABLED
        )
        self.btn_red.pack(side=tk.LEFT, padx=5)
        
        self.btn_orange = tk.Button(
            frame,
            text="🟠 FEU ORANGE",
            bg="#FF8800",
            fg="black",
            width=15,
            command=self._on_orange_clicked,
            state=tk.DISABLED
        )
        self.btn_orange.pack(side=tk.LEFT, padx=5)
        
        self.btn_green = tk.Button(
            frame,
            text="🟢 FEU VERT",
            bg="#44FF44",
            fg="black",
            width=15,
            command=self._on_green_clicked,
            state=tk.DISABLED
        )
        self.btn_green.pack(side=tk.LEFT, padx=5)
    
    def _create_status_panel(self) -> None:
        """Crée le panneau d'état"""
        frame = tk.LabelFrame(
            self.root,
            text="📊 ÉTAT ACTUEL",
            bg=self.colors['frame_bg'],
            padx=10,
            pady=10
        )
        frame.pack(padx=20, pady=5, fill='x')
        
        # État simulation
        self.lbl_status = tk.Label(
            frame,
            text="Simulation: ARRÊTÉE",
            font=("Arial", 10),
            bg=self.colors['frame_bg'],
            fg="#F44336"  # Rouge
        )
        self.lbl_status.pack(anchor='w', pady=2)
        
        # Scénario actuel
        self.lbl_scenario = tk.Label(
            frame,
            text=f"Scénario: {self.current_scenario}",
            font=("Arial", 10),
            bg=self.colors['frame_bg']
        )
        self.lbl_scenario.pack(anchor='w', pady=2)
        
        # Véhicules (à mettre à jour plus tard)
        self.lbl_vehicles = tk.Label(
            frame,
            text="Véhicules actifs: 0",
            font=("Arial", 10),
            bg=self.colors['frame_bg']
        )
        self.lbl_vehicles.pack(anchor='w', pady=2)
        
        # Feu tricolore (à mettre à jour plus tard)
        self.lbl_traffic_light = tk.Label(
            frame,
            text="Feu: --",
            font=("Arial", 10),
            bg=self.colors['frame_bg']
        )
        self.lbl_traffic_light.pack(anchor='w', pady=2)
    
    def _create_quit_button(self) -> None:
        """Crée le bouton quitter"""
        frame = tk.Frame(self.root, bg=self.colors['bg'])
        frame.pack(pady=20)
        
        btn_quit = tk.Button(
            frame,
            text="🚪 QUITTER L'APPLICATION",
            font=("Arial", 10, "bold"),
            bg="#666666",
            fg="white",
            width=20,
            height=2,
            command=self.close
        )
        btn_quit.pack()
    
    # === GESTION DES ÉVÉNEMENTS ===
    
    def _on_start_clicked(self) -> None:
        """Gère le clic sur Démarrer"""
        print("Bouton Démarrer cliqué")
        self.simulation_running = True
        self.simulation_paused = False
        
        # Mettre à jour l'interface
        self.lbl_status.config(text="Simulation: EN COURS", fg="#4CAF50")
        self.btn_start.config(state=tk.DISABLED)
        self.btn_pause.config(state=tk.NORMAL)
        self.btn_stop.config(state=tk.NORMAL)
        
        # Appeler le callback si défini
        if self.simulation_callback:
            self.simulation_callback('start')
    
    def _on_pause_clicked(self) -> None:
        """Gère le clic sur Pause"""
        if self.simulation_paused:
            print("Bouton Reprise cliqué")
            self.simulation_paused = False
            self.lbl_status.config(text="Simulation: EN COURS", fg="#4CAF50")
            self.btn_pause.config(text="⏸ PAUSE")
        else:
            print("Bouton Pause cliqué")
            self.simulation_paused = True
            self.lbl_status.config(text="Simulation: EN PAUSE", fg="#FF9800")
            self.btn_pause.config(text="▶ REPRENDRE")
        
        # Appeler le callback si défini
        if self.simulation_callback:
            self.simulation_callback('pause')
    
    def _on_stop_clicked(self) -> None:
        """Gère le clic sur Arrêter"""
        print("Bouton Arrêter cliqué")
        self.simulation_running = False
        self.simulation_paused = False
        
        # Mettre à jour l'interface
        self.lbl_status.config(text="Simulation: ARRÊTÉE", fg="#F44336")
        self.btn_start.config(state=tk.NORMAL)
        self.btn_pause.config(state=tk.DISABLED, text="⏸ PAUSE")
        self.btn_stop.config(state=tk.DISABLED)
        
        # Appeler le callback si défini
        if self.simulation_callback:
            self.simulation_callback('stop')
    
    def _on_reset_clicked(self) -> None:
        """Gère le clic sur Réinitialiser"""
        print("Bouton Réinitialiser cliqué")
        messagebox.showinfo("Réinitialisation", "La simulation sera réinitialisée.")
        
        # Appeler le callback si défini
        if self.simulation_callback:
            self.simulation_callback('reset')
    
    def _on_scenario_changed(self) -> None:
        """Gère le changement de scénario"""
        scenario = self.scenario_var.get()
        print(f"Scénario changé: {scenario}")
        
        # Mettre à jour l'affichage
        scenario_names = {
            "normal": "Circulation Normale",
            "rush_hour": "Heure de Pointe",
            "night": "Mode Nuit",
            "manual": "Mode Manuel"
        }
        self.current_scenario = scenario_names.get(scenario, "Inconnu")
        self.lbl_scenario.config(text=f"Scénario: {self.current_scenario}")
        
        # Activer/désactiver contrôles manuels
        if scenario == "manual":
            self.btn_red.config(state=tk.NORMAL)
            self.btn_orange.config(state=tk.NORMAL)
            self.btn_green.config(state=tk.NORMAL)
        else:
            self.btn_red.config(state=tk.DISABLED)
            self.btn_orange.config(state=tk.DISABLED)
            self.btn_green.config(state=tk.DISABLED)
        
        # Appeler le callback si défini
        if self.simulation_callback:
            self.simulation_callback(f'scenario:{scenario}')
    
    def _on_red_clicked(self) -> None:
        """Gère le clic sur Feu Rouge"""
        print("Feu Rouge manuel")
        if self.simulation_callback:
            self.simulation_callback('light:red')
    
    def _on_orange_clicked(self) -> None:
        """Gère le clic sur Feu Orange"""
        print("Feu Orange manuel")
        if self.simulation_callback:
            self.simulation_callback('light:orange')
    
    def _on_green_clicked(self) -> None:
        """Gère le clic sur Feu Vert"""
        print("Feu Vert manuel")
        if self.simulation_callback:
            self.simulation_callback('light:green')
    
    def update_vehicle_count(self, count: int) -> None:
        """Met à jour le compteur de véhicules"""
        self.lbl_vehicles.config(text=f"Véhicules actifs: {count}")
    
    def update_traffic_light(self, state: str) -> None:
        """Met à jour l'état du feu"""
        self.lbl_traffic_light.config(text=f"Feu: {state}")
    
    def run(self) -> None:
        """Lance l'interface"""
        if not self.initialized:
            print("Erreur: Interface non initialisée")
            return
        
        print("\nLancement de l'interface...")
        print("Instructions:")
        print("1. Cliquez sur ▶ DÉMARRER pour lancer la simulation")
        print("2. Utilisez les boutons pour contrôler")
        print("3. Changez de scénario avec les boutons radio")
        print("4. En mode Manuel, utilisez les boutons de feu")
        print("5. Cliquez sur 🚪 QUITTER pour fermer")
        
        self.root.mainloop()
    
    def close(self) -> None:
        """Ferme l'interface"""
        if self.root:
            self.root.quit()
            self.root.destroy()
        print("✓ Interface fermée")


def test_gui():
    """Teste l'interface graphique"""
    print("\n=== TEST ControlInterface ===")
    
    def simulation_callback(action):
        """Fonction de test pour les callbacks"""
        print(f"Callback reçu: {action}")
    
    interface = ControlInterface(simulation_callback=simulation_callback)
    
    if interface.setup():
        print("✓ Interface configurée avec succès")
        print("✓ Test: L'interface va s'ouvrir...")
        interface.run()
    else:
        print("✗ Erreur de configuration")


if __name__ == "__main__":
    test_gui()