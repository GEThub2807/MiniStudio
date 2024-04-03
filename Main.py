import pygame
from pygame.locals import *

# Constantes
LARGEUR = 800
HAUTEUR = 600
GRAVITE = 0.5
VITESSE_X = 5
VITESSE_Y = 10

# Initialisation de Pygame
pygame.init()

# Définir la taille de la fenêtre du jeu
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))

# Charger les images des personnages et du fond
try:
    fond = pygame.image.load("Assets/Fond.jpg").convert()
    personnage = pygame.image.load("Assets/Henry.png").convert()
except pygame.error as e:
    print("Erreur lors du chargement des images :", str(e))
    pygame.quit()
    exit()

# Position initiale du personnage
position_x = 100
position_y = 400

# Variables de mouvement du personnage
vitesse_x = 0
vitesse_y = 0

# Fonction de mouvement du personnage
def deplacer_personnage():
    global position_x, position_y, vitesse_x, vitesse_y

    # Appliquer la gravité au personnage
    vitesse_y += GRAVITE

    # Mettre à jour la position du personnage
    position_x += vitesse_x
    position_y += vitesse_y

    # Limiter la position du personnage à l'écran
    if position_x < 0:
        position_x = 0
    elif position_x > LARGEUR - personnage.get_width():
        position_x = LARGEUR - personnage.get_width()
    if position_y < 0:
        position_y = 0
    elif position_y > HAUTEUR - personnage.get_height():
        position_y = HAUTEUR - personnage.get_height()

# Boucle principale du jeu
running = True
clock = pygame.time.Clock()
while running:
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                vitesse_x = -VITESSE_X
            elif event.key == K_RIGHT:
                vitesse_x = VITESSE_X
            elif event.key == K_SPACE:
                vitesse_y = -VITESSE_Y
        elif event.type == KEYUP:
            if event.key == K_LEFT or event.key == K_RIGHT:
                vitesse_x = 0

    # Déplacer le personnage
    deplacer_personnage()

    # Effacer l'écran avec le fond
    fenetre.blit(fond, (0, 0))

    # Afficher le personnage à sa position actuelle
    fenetre.blit(personnage, (position_x, position_y))

    # Mettre à jour l'affichage
    pygame.display.flip()

    # Limiter la vitesse de rafraîchissement à 60 FPS
    clock.tick(60)

# Quitter Pygame
pygame.quit()