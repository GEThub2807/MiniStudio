from Main import *
# Définition des coordonnées de la plateforme
plateforme_x = 300
plateforme_y = 500
plateforme_largeur = 200
plateforme_hauteur = 20

def colision_platforme():
    # Vérification de la collision entre le joueur et la plateforme
    if position_y + PERSONNAGE_HAUTEUR < plateforme_y:
        # Le joueur traverse la plateforme par le bas
        pass
    elif position_y > plateforme_y + plateforme_hauteur:
        # Le joueur est au-dessus de la plateforme et est bloqué
        position_y = plateforme_y + plateforme_hauteur
    else:
        # Le joueur est en collision avec la plateforme
        pass