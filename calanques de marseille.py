
import pygame as py
from pygame.locals import *

# Constantes
LARGEUR = 1920  # Largeur de la fenêtre du jeu
HAUTEUR = 1080  # Hauteur de la fenêtre du jeu
GRAVITE = 0.5
VITESSE_X = 5
VITESSE_Y = 10
VITESSE_COURSE = 10  # Vitesse de déplacement en mode course
PERSONNAGE_LARGEUR = 50  # Largeur du personnage
PERSONNAGE_HAUTEUR = 50  # Hauteur du personnage

# Charge le fichier audio
'son = py.mixer.Sound("chemin/vers/ton/fichier/audio.wav")'

# Initialisation de py
py.init()

# Définir la taille de la fenêtre du jeu
fenetre = py.display.set_mode((LARGEUR, HAUTEUR))

# Charger les images des personnages et du fond
try:
    fond = py.image.load("Assets/obese.jpg").convert()
    personnage = py.image.load("Assets/perso.png").convert()
    personnage = py.transform.scale(personnage, (PERSONNAGE_LARGEUR, PERSONNAGE_HAUTEUR))
except py.error as e:
    print("Erreur lors du chargement des images :", str(e))
    py.quit()
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

def cameraGroup():
    display_surface = py.display.get_surface()
    
    #camera offset
    offset = py.math.Vector2()
    half_w = display_surface.get_size() [0] // 2
    half_h = display_surface.get_size() [1] // 2

    #box setup
    camera_borders = {
        'left' : 200,
        'right' : 200,
        'top' : 200,
        'bottom' : 200
    }
    l = camera_borders['left']
    t = camera_borders['top']
    w = display_surface.get_size() [0] - (camera_borders['left'] + camera_borders['right'])
    h = display_surface.get_size() [1] - (camera_borders['right'] + camera_borders['bottom'])
    camera = py.Rect(l, t, w, h)

    #ground
    ground_surf = py.image.load('Assets/obese.jpg').convert_alpha()
    ground_rect = ground_surf.get_rect(topleft = (0, 0))

# Position de la bordure de la caméra à partir de laquelle la caméra commencera à se déplacer
BORDER_MARGIN = 50

# Boucle principale du jeu
running = True
clock = py.time.Clock()
while running:
    # Gestion des événements
    for event in py.event.get():
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

    # Effacer l'écran
    fenetre.fill((0, 0, 0))

    # Vérifier si le personnage approche des bords de la caméra
    if position_x < camera_x + BORDER_MARGIN:
        camera_x -= VITESSE_X  # Déplacer la caméra vers la gauche
    elif position_x > camera_x + camera_largeur - BORDER_MARGIN:
        camera_x += VITESSE_X  # Déplacer la caméra vers la droite
    if position_y < camera_y + BORDER_MARGIN:
        camera_y -= VITESSE_Y  # Déplacer la caméra vers le haut
    elif position_y > camera_y + camera_hauteur - BORDER_MARGIN:
        camera_y += VITESSE_Y  # Déplacer la caméra vers le bas

    # Limiter la position de la caméra pour rester dans les limites du monde du jeu
    camera_x = max(0, min(camera_x, LARGEUR - camera_largeur))
    camera_y = max(0, min(camera_y, HAUTEUR - camera_hauteur))

    # Afficher le fond à l'arrière-plan avec la caméra
    fenetre.blit(fond, (0 - camera_x, 0 - camera_y))

    # Afficher le personnage dans la caméra
    fenetre.blit(personnage, (position_x - camera_x, position_y - camera_y))

    # Mettre à jour l'affichage
    py.display.flip()

    # Limiter la vitesse de rafraîchissement à 60 FPS
    clock.tick(60)

# Joue le son
'son.play()'

# Attends que le son se termine
'py.time.delay(son.get_length() * 1000)  # Convertit la durée du son en millisecondes'

# Arrête le son
'son.stop()'

# Quitter py
py.quit()