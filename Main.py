import pygame
from pygame.locals import *

# Constantes
LARGEUR = 1000  # Largeur de la fenêtre du jeu
HAUTEUR = 500  # Hauteur de la fenêtre du jeu
GRAVITE = 0.5
VITESSE_X = 5
VITESSE_Y = 10
VITESSE_COURSE = 10  # Vitesse de déplacement en mode course
PERSONNAGE_LARGEUR = 50  # Largeur du personnage
PERSONNAGE_HAUTEUR = 50  # Hauteur du personnage
PNJ_LARGEUR = 70  # Largeur du personnage
PNJ_HAUTEUR = 130 # Hauteur du personnage

# Constantes Platforme
plateforme_y = 8  # Position Y de la plateforme (Modifiable)
plateforme_hauteur = 1 # Hauteur de la plateforme (Modifiable)
platforme_largeur = 20 # Largeur de la plateforme (Modifiable)
rectangle = pygame.Rect(0, plateforme_y, platforme_largeur, plateforme_hauteur)
# Points de départ et d'arrivée du PNJ
PNJ_DEPART_X = 500
PNJ_DEPART_Y = 400
PNJ_ARRIVEE_X = 600
PNJ_ARRIVEE_Y = 400

# Initialisation de Pygame
pygame.init()

# Définir la taille de la fenêtre du jeu
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))

# Charger l'image du fond + joueur + PNJ
try:
    fond = pygame.image.load("Assets/Fond.jpg").convert()
    fond = pygame.transform.scale(fond, (LARGEUR, HAUTEUR))
    personnage = pygame.image.load("Assets/Cube.png").convert_alpha()
    personnage = pygame.transform.scale(personnage, (PERSONNAGE_LARGEUR, PERSONNAGE_HAUTEUR))
    pnj = pygame.image.load("Assets/PNJ.png").convert_alpha()
    pnj = pygame.transform.scale(pnj, (PNJ_LARGEUR, PNJ_HAUTEUR))
except pygame.error as e:
    print("Erreur lors du chargement de l'image du fond :", str(e))
    pygame.quit()
    exit()

# Position initiale du personnage
position_x = 100
position_y = 400

# Position initiale du PNJ
pnj_x = PNJ_DEPART_X
pnj_y = PNJ_DEPART_Y

# Variables de mouvement du personnage
vitesse_x = 0
vitesse_y = 0
nombre_sauts = 0
is_running = False  # Variable pour vérifier si la touche Shift est enfoncée

# Variable de direction du PNJ
direction_pnj = 1  # 1 pour droite, -1 pour gauche

# Fonction de mouvement du personnage
def deplacer_personnage():
    global position_x, position_y, vitesse_x, vitesse_y, nombre_sauts

    # Appliquer la gravité au personnage
    vitesse_y += GRAVITE

    # Mettre à jour la position du personnage
    position_x += vitesse_x
    position_y += vitesse_y

    # Limiter la position du personnage à l'écran
    position_x = max(0, min(position_x, LARGEUR - PERSONNAGE_LARGEUR))
    position_y = max(0, min(position_y, HAUTEUR - PERSONNAGE_HAUTEUR))

    # Réinitialiser le nombre de sauts si le personnage touche le sol
    if position_y >= HAUTEUR - PERSONNAGE_HAUTEUR:
        nombre_sauts = 0

# Fonction de collision entre le personnage et le PNJ
def collision_pnj():
    global position_x, position_y, vitesse_x, vitesse_y
    
    # Vérifier la collision uniquement si le personnage se déplace vers le PNJ
    if vitesse_x > 0:
        if position_x + PERSONNAGE_LARGEUR > pnj_x and position_x < pnj_x + PNJ_LARGEUR:
            if position_y + PERSONNAGE_HAUTEUR > pnj_y and position_y < pnj_y + PNJ_HAUTEUR:
                position_x = pnj_x - PERSONNAGE_LARGEUR
                vitesse_x = 0  # Arrêter le mouvement horizontal
    elif vitesse_x < 0:
        if position_x < pnj_x + PNJ_LARGEUR and position_x + PERSONNAGE_LARGEUR > pnj_x:
            if position_y + PERSONNAGE_HAUTEUR > pnj_y and position_y < pnj_y + PNJ_HAUTEUR:
                position_x = pnj_x + PNJ_LARGEUR
                vitesse_x = 0  # Arrêter le mouvement horizontal
            
    # Même chose pour le mouvement vertical
    if vitesse_y > 0:
        if position_x + PERSONNAGE_LARGEUR > pnj_x and position_x < pnj_x + PNJ_LARGEUR:
            if position_y + PERSONNAGE_HAUTEUR > pnj_y and position_y < pnj_y + PNJ_HAUTEUR:
                position_y = pnj_y - PERSONNAGE_HAUTEUR
                vitesse_y = 0  # Arrêter le mouvement vertical
    elif vitesse_y < 0:
        if position_x + PERSONNAGE_LARGEUR > pnj_x and position_x < pnj_x + PNJ_LARGEUR:
            if position_y < pnj_y + PNJ_HAUTEUR and position_y + PERSONNAGE_HAUTEUR > pnj_y:
                position_y = pnj_y + PNJ_HAUTEUR
                vitesse_y = 0  # Arrêter le mouvement vertical

def collision_plateforme():
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

def collision_rectangle():
    global position_y, vitesse_y, nombre_sauts

    if position_x + PERSONNAGE_LARGEUR > rectangle.left and position_x < rectangle.right:
        if position_y + PERSONNAGE_HAUTEUR > rectangle.top and position_y < rectangle.bottom:
            position_y = rectangle.top - PERSONNAGE_HAUTEUR
            vitesse_y = 0
            nombre_sauts = 0
            
# Boucle principale du jeu
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                vitesse_x = -VITESSE_X
            elif event.key == K_RIGHT:
                vitesse_x = VITESSE_X
            elif event.key == K_SPACE and nombre_sauts < 2:
                vitesse_y = -VITESSE_Y
                nombre_sauts += 1
            elif event.key == K_LSHIFT or event.key == K_RSHIFT:
                if not is_running:
                    VITESSE_X = VITESSE_COURSE
                    is_running = True
            elif event.key == K_ESCAPE:
                running = False
        elif event.type == KEYUP:
            if event.key == K_LEFT and vitesse_x < 0:
                vitesse_x = 0
            elif event.key == K_RIGHT and vitesse_x > 0:
                vitesse_x = 0
            elif event.key == K_LSHIFT or event.key == K_RSHIFT:
                if is_running:
                    VITESSE_X = 5
                    is_running = False

    # Déplacer le personnage
    deplacer_personnage()

    # Déplacer le PNJ avec gestion de collision
    pnj_x += direction_pnj * 1

    if pnj_x <= 0 or pnj_x >= LARGEUR - PNJ_LARGEUR:
        direction_pnj *= -1

    # Vérifier la collision entre le personnage et le PNJ
    collision_pnj()

    # Dans la boucle principale, vérifiez la collision avec le rectangle
    collision_rectangle()

    # Afficher le fond à l'arrière-plan
    fenetre.blit(fond, (0, 0))

    # Afficher le personnage à sa position actuelle
    fenetre.blit(personnage, (position_x, position_y))

    # Afficher le PNJ à sa position actuelle
    fenetre.blit(pnj, (pnj_x, pnj_y))

    # Afficher l'image du rectangle à la position plateforme_y
    rectangle_image = pygame.Surface((platforme_largeur, plateforme_hauteur))
    rectangle_image = pygame.image.load("Assets/Rectangle.png").convert_alpha()
    fenetre.blit(rectangle_image, (0, plateforme_y))

    # Mettre à jour l'affichage
    pygame.display.flip()

    # Limiter la vitesse de rafraîchissement à 60 FPS
    clock.tick(60)

# Quitter Pygame
pygame.quit()