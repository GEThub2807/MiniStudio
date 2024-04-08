import pygame
from pygame.locals import *
from random import randint
import time

# Constantes
LARGEUR = 1600  # Largeur de la fenêtre du jeu
HAUTEUR = 900  # Hauteur de la fenêtre du jeu
GRAVITE = 0.5
VITESSE_X = 5
VITESSE_Y = 10
VITESSE_COURSE = 10  # Vitesse de déplacement en mode course
PERSONNAGE_LARGEUR = 50  # Largeur du personnage
PERSONNAGE_HAUTEUR = 50  # Hauteur du personnage
""" NPC_VITESSE = randint(-5, -3) if randint(0, 1) else randint(3, 5) """
NPC_VITESSE = -5

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

    
    pnj1 = pygame.image.load("Assets/pnj1.png").convert_alpha()
    pnj2 = pygame.image.load("Assets/pnj2.png").convert_alpha()
    pnj3 = pygame.image.load("Assets/pnj3.png").convert_alpha()
    
    # Liste de tous les pnjs
    npc = [pnj1, pnj2, pnj3]

    pnj_choice = randint(0, len(npc) - 1)
    lengthNpc = npc[pnj_choice].get_size()

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

import random

class NPC:
    def __init__(self, images, initial_x, spawn_y, velocity):
        self.images = images
        self.image_index = 0
        self.image = images[self.image_index]
        self.pos_x = initial_x
        self.spawn_y = spawn_y
        self.pos_y = spawn_y
        self.velocity = velocity
        self.size = self.image.get_size()

    def move(self):
        self.pos_x += self.velocity

        # Vérifier si le PNJ est hors de l'écran à gauche ou à droite
        if self.pos_x >= LARGEUR and self.velocity > 0:
            self.pos_x = 0 - self.size[0]
            self.change_image()
        elif self.pos_x <= 0 - self.size[0] and self.velocity < 0:
            self.pos_x = LARGEUR
            self.change_image()

    def change_image(self):
        # Changer l'image du PNJ de manière aléatoire
        self.image_index = random.randint(0, len(self.images) - 1)
        self.image = self.images[self.image_index]

    def draw(self, screen, camera_x, camera_y):
        screen.blit(self.image, (self.pos_x - camera_x, self.pos_y - camera_y))

# Créer une instance de la classe NPC
npc_images = [pnj1, pnj2, pnj3]
npc = NPC(npc_images, randint(0, lengthFond[0]), lengthFond[1] - 700, NPC_VITESSE)
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
    npc.move()

    fenetre.fill((0,0,0))

    # Afficher le fond à l'arrière-plan
    fenetre.blit(fond, (0 - camera_x, 0 - camera_y))

    # Afficher le personnage à sa position actuelle (par rapport à la caméra)
    fenetre.blit(personnage, (position_x - camera_x, position_y - camera_y))

    # Afficher le pnj à sa position actuelle
    npc.draw(fenetre, camera_x, camera_y)

    # Mettre à jour l'affichage
    pygame.display.flip()

    # Limiter la vitesse de rafraîchissement à 60 FPS
    clock.tick(60)

# Quitter Pygame
pygame.quit()

import pygame
from pygame.locals import *

# Constantes
LARGEUR = 1400  # Largeur de la fenêtre du jeu
HAUTEUR = 800  # Hauteur de la fenêtre du jeu
GRAVITE = 0.5
VITESSE_X = 5
VITESSE_Y = 10
VITESSE_COURSE = 10  # Vitesse de déplacement en mode course
PERSONNAGE_LARGEUR = 50  # Largeur du personnage
PERSONNAGE_HAUTEUR = 50  # Hauteur du personnage

# Initialisation de Pygame
pygame.init()

# Définir la taille de la fenêtre du jeu
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))


# Creer une classe pour le joueur
class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.health = 100
        self.max_health = 100
        self.image = pygame.image.load('Assets/rat.png')
        self.rect = self.image.get_rect()





# Charger les images des personnages et du fond
try:
    fond = pygame.image.load("Assets/Fond_Game.jpg").convert()

    fond = pygame.transform.scale(fond,(LARGEUR,HAUTEUR))

    personnage = Player()
    personnage.image = pygame.transform.scale(personnage.image, (PERSONNAGE_LARGEUR, PERSONNAGE_HAUTEUR))

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
nombre_sauts = 0
is_running = False  # Variable pour vérifier si la touche Shift est enfoncée


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

    # Afficher le fond à l'arrière-plan
    fenetre.blit(fond, (0, 0))

    # Afficher le personnage à sa position actuelle
    fenetre.blit(personnage.image, (position_x, position_y))

    # Mettre à jour l'affichage
    pygame.display.flip()

    # Limiter la vitesse de rafraîchissement à (x) FPS
    clock.tick(60)

# Quitter Pygame
pygame.quit()
