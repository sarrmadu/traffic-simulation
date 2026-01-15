"""
Point d'entrée principal de l'application
Responsable : Modou Sarr
"""

import sys
import os
import tkinter as tk

# Ajouter src au path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    """Fonction principale"""
    print("=" * 50)
    print("SIMULATION FEU TRICOLORE - VILLE DE THIÈS")
    print("=" * 50)
    print("\nInitialisation en cours...")
    
    # Créer une fenêtre Tkinter simple
    root = tk.Tk()
    root.title("Simulation Feu Tricolore")
    root.geometry("400x200")
    
    # Ajouter un label
    label = tk.Label(
        root,
        text="Bienvenue dans la simulation\n\n" +
             "L'interface sera développée ici.\n" +
             "Mbene : Graphiques\n" +
             "Ndeye : Logique\n" +
             "Modou : Interface & Données",
        font=("Arial", 12),
        justify="center"
    )
    label.pack(expand=True)
    
    # Bouton quitter
    quit_btn = tk.Button(
        root,
        text="Quitter",
        command=root.quit,
        bg="red",
        fg="white",
        font=("Arial", 10, "bold")
    )
    quit_btn.pack(pady=20)
    
    print("✓ Interface Tkinter créée")
    print("\nInstructions :")
    print("1. Mbene : Implémenter road_scene.py")
    print("2. Ndeye : Implémenter scenario_manager.py")
    print("3. Modou : Compléter l'interface")
    print("\nAppuyez sur le bouton Quitter pour fermer")
    
    # Lancer la boucle Tkinter
    root.mainloop()
    
    print("\n✓ Application fermée")
    return 0

if __name__ == "__main__":
    sys.exit(main())