"""
Scénarios de circulation - Documentation
========================================

Ce document décrit les 4 scénarios de circulation implémentés dans la simulation.

## 1. Vue d'ensemble

La simulation supporte 4 scénarios distincts qui modifient :
- Les durées des feux tricolores
- Le comportement des véhicules
- La fréquence d'apparition des véhicules
- La vitesse des véhicules

## 2. Scénario 1 : Circulation normale

### 2.1 Description
Comportement standard pour une journée typique.

### 2.2 Paramètres du feu
```python
{
    "GREEN": 10,    # 10 secondes
    "ORANGE": 3,    # 3 secondes
    "RED": 8        # 8 secondes
}