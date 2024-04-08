import pygame

plateforme_y = 100
position_y = 100
vitesse_y = 0
plateforme_hauteur = 20
PERSONNAGE_HAUTEUR = 50

class Platforme:
    def __init__(self) -> None:
        pass

    def colision_platforme(self):
        global position_y, vitesse_y, nombre_sauts

        # Vérification de la collision entre le joueur et la plateforme
        if position_y + PERSONNAGE_HAUTEUR < plateforme_y:
            # Le joueur est au-dessus de la plateforme
            pass
        elif position_y + PERSONNAGE_HAUTEUR - vitesse_y <= plateforme_y:
            # Le joueur traverse la plateforme par le bas
            # Ajuster la position et réinitialiser les sauts
            position_y = plateforme_y - PERSONNAGE_HAUTEUR
            vitesse_y = 0
            nombre_sauts = 0
        else:
            # Le joueur est en collision avec la plateforme depuis le haut
            # Ajuster la position pour empêcher le passage à travers la plateforme
            position_y = plateforme_y + plateforme_hauteur
            vitesse_y = 0
            nombre_sauts = 0