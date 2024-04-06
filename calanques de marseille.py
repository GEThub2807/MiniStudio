import pygame
from pygame.locals import *
from random import randint

# Constantes
LARGEUR = 1600  # Largeur de la fenêtre du jeu
HAUTEUR = 900  # Hauteur de la fenêtre du jeu
GRAVITE = 0.5
VITESSE_X = 5
VITESSE_Y = 10
VITESSE_COURSE = 10  # Vitesse de déplacement en mode course
PERSONNAGE_LARGEUR = 50  # Largeur du personnage
PERSONNAGE_HAUTEUR = 50  # Hauteur du personnage
NPC_VITESSE = 5 #vitesse des pnjs

# Initialisation de Pygame
pygame.init()

# Définir la taille de la fenêtre du jeu
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))

# Charger les images des personnages et du fond
try:
    fond = pygame.image.load("Assets/obese.jpg").convert()
    lengthFond : list[int] = fond.get_size()

    personnage = pygame.image.load("Assets/perso.png").convert_alpha()
    personnage = pygame.transform.scale(personnage, (PERSONNAGE_LARGEUR, PERSONNAGE_HAUTEUR))

    
    npc = pygame.image.load("Assets/npc.jpg").convert_alpha()
    lengthNpc = npc.get_size()
    npc = pygame.transform.scale(npc, (lengthNpc[0], lengthNpc[1]))

except pygame.error as e:
    print("Erreur lors du chargement des images :", str(e))
    pygame.quit()
    exit()

# Position initiale du personnage
position_x = 0
position_y = lengthFond[1] - 501

# Variables de mouvement du personnage
vitesse_x = 0
vitesse_y = 0
nombre_sauts = 2
is_running = False  # Variable pour vérifier si la touche Shift est enfoncée

# Position initiale de la caméra
camera_x = 0
camera_y = 0

# Taille de la zone de la caméra
CAMERA_LARGEUR = LARGEUR // 2
CAMERA_HAUTEUR = HAUTEUR // 2

# Position initiale des pnjs
npc_pos_x = (randint(0, lengthFond[0]))
npc_pos_y = (lengthFond[1] - 300)

# Fonction de mouvement du personnage
def deplacer_personnage():
    global position_x, position_y, vitesse_x, vitesse_y, nombre_sauts

    # Appliquer la gravité au personnage
    vitesse_y += GRAVITE

    # Mettre à jour la position du personnage
    position_x += vitesse_x
    position_y += vitesse_y

    # Limiter la position du personnage à l'écran
    position_x = max(0, min(position_x, lengthFond[0] - PERSONNAGE_LARGEUR))
    position_y = max(0, min(position_y, lengthFond[1] - PERSONNAGE_HAUTEUR - 300))

    # Réinitialiser le nombre de sauts si le personnage est au sol
    if position_y >= lengthFond[1] - PERSONNAGE_HAUTEUR - 300:
        nombre_sauts = 0



# Fonction pour déplacer la caméra
def deplacer_camera():
    global camera_x, camera_y

    delta_x = position_x - (camera_x + CAMERA_LARGEUR // 2)
    delta_y = position_y - (camera_y + CAMERA_HAUTEUR // 2)

    if camera_x <= 0 and delta_x < 0:
        delta_x = 0

    if camera_x + LARGEUR >= lengthFond[0] and delta_x > 0:
        delta_x = 0

    if camera_y <= 0 and delta_y < 0:
        delta_y = 0

    if camera_y + HAUTEUR >= lengthFond[1] and delta_y > 0:
        delta_y = 0

    camera_x += delta_x * 0.1
    camera_y += delta_y * 0.1

""" def npc_move():
    global npc_pos_x, npc_pos_y, NPC_VITESSE

    # Vérifier si le PNJ est hors de l'écran à gauche ou à droite
    if npc_pos_x >= LARGEUR or npc_pos_x <= 0 - lengthNpc[0]:
        NPC_VITESSE *= -1  # Inverser la direction du déplacement

    # Mettre à jour la position horizontale du PNJ
    npc_pos_x += NPC_VITESSE

    # Aligner la position verticale du PNJ sur celle du personnage
    npc_pos_y = position_y

    # Limiter la position du PNJ à l'écran
    npc_pos_y = max(0, min(npc_pos_y, HAUTEUR - lengthNpc[1] - 500)) """

def npc_move():
    global npc_pos_x, npc_pos_y, NPC_VITESSE

    # Vérifier si le PNJ est hors de l'écran à gauche ou à droite
    if npc_pos_x >= LARGEUR :
        npc_pos_x = 0 - lengthNpc[0]

    if npc_pos_x <= 0 :
        npc_pos_x = LARGEUR + lengthNpc[0]

    # Mettre à jour la position horizontale du PNJ
    npc_pos_x += NPC_VITESSE

    # Aligner la position verticale du PNJ sur celle du personnage
    npc_pos_y = position_y

    # Limiter la position du PNJ à l'écran
    npc_pos_y = max(0, min(npc_pos_y, HAUTEUR - lengthNpc[1] - 500))


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
            elif event.key == K_SPACE and nombre_sauts < 2:
                vitesse_y = -VITESSE_Y
                nombre_sauts += 1
            elif event.key == K_LSHIFT or event.key == K_RSHIFT:
                if not is_running:
                    VITESSE_X = VITESSE_COURSE
                    is_running = True  # La touche Shift est enfoncée
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
                    is_running = False  # La touche Shift est relâchée

    # Déplacer le personnage
    deplacer_personnage()

    # Déplacer la caméra
    deplacer_camera()

    # Déplacer les pnjs
    npc_move()

    fenetre.fill((0,0,0))

    # Afficher le fond à l'arrière-plan
    fenetre.blit(fond, (0 - camera_x, 0 - camera_y))

    # Afficher le personnage à sa position actuelle (par rapport à la caméra)
    fenetre.blit(personnage, (position_x - camera_x, position_y - camera_y))

    # Afficher le pnj à sa position actuelle 
    fenetre.blit(npc, (npc_pos_x, npc_pos_y))    

    # Mettre à jour l'affichage
    pygame.display.flip()

    # Limiter la vitesse de rafraîchissement à 60 FPS
    clock.tick(60)

# Quitter Pygame
pygame.quit()