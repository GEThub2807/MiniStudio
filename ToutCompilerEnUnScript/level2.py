import pygame
from pygame.locals import *

def run_game():
    # Constantes
    LARGEUR = 1920  # Largeur de la fenêtre du jeu
    HAUTEUR = 1080  # Hauteur de la fenêtre du jeu
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

    # Créer une classe pour le joueur
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
        fond = pygame.transform.scale(fond, (LARGEUR, HAUTEUR))

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
        nonlocal position_x, position_y, vitesse_x, vitesse_y, nombre_sauts

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
