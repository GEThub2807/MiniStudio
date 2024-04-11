import pygame
from pygame.locals import *

# Constantes
LARGEUR = 1920  # Largeur de la fenêtre du jeu
HAUTEUR = 1080  # Hauteur de la fenêtre du jeu
GRAVITE = 0.5
VITESSE_X = 5
VITESSE_Y = 10
VITESSE_COURSE = 10  # Vitesse de déplacement en mode course
PERSONNAGE_LARGEUR = 100  # Largeur du personnage
PERSONNAGE_HAUTEUR = 70  # Hauteur du personnage
PNJ_LARGEUR = 70  # Largeur du personnage
PNJ_HAUTEUR = 130 # Hauteur du personnage
PLATEFORME_LARGEUR = 145  # Largeur de la plateforme
PLATEFORME_HAUTEUR = 20  # Hauteur de la plateforme

# Points de départ et d'arrivée du PNJ
PNJ_DEPART_X = 500
PNJ_DEPART_Y = HAUTEUR - PNJ_HAUTEUR
PNJ_ARRIVEE_X = 600
PNJ_ARRIVEE_Y = HAUTEUR - PNJ_HAUTEUR

COLOR = (255, 0, 0)

# Initialisation de Pygame
pygame.init()

# Définir la taille de la fenêtre du jeu
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))

# Position de la plateforme
x = 35 # x pixels du bord gauche de l'écran
y = HAUTEUR - PLATEFORME_HAUTEUR - 75  # x pixels du bas de l'écran

class PlateformeBalcon(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((PLATEFORME_LARGEUR, PLATEFORME_HAUTEUR))
        self.image.fill (COLOR) # Remplir la surface avec la couleur définie
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def GetCollision(self, rect: pygame.rect.Rect) -> tuple[int, int]:
        #0 => None
        #1 => Left
        #2 => Right
        #3 => Top
        #4 => Bottom 

        if rect.right < self.rect.left:
            return 0, 0
        
        if rect.left > self.rect.right:
            return 0, 0
        
        if rect.top > self.rect.bottom:
            return 0, 0
        
        if rect.bottom < self.rect.top:
            return 0, 0

        distances: list[int] = []
        distances.append(abs(rect.right - self.rect.left))
        distances.append(abs(rect.left - self.rect.right))
        distances.append(abs(rect.bottom - self.rect.top))
        distances.append(abs(rect.top - self.rect.bottom))

        minDistance = 2000
        side: int = 0
        for i in range(0, len(distances)):
            if minDistance > distances[i]:
                minDistance = distances[i]
                side = i + 1
        
        return side, minDistance

plateformes = []

plateforme_positions = [(35, HAUTEUR - PLATEFORME_HAUTEUR - 75),
                        (465, HAUTEUR - PLATEFORME_HAUTEUR - 75),
                        (850, HAUTEUR - PLATEFORME_HAUTEUR - 75),
                        # Ajoutez autant de positions de plateformes que vous le souhaitez
                        ]

def ajouter_plateforme(x, y):
    plateforme = PlateformeBalcon(x, y)
    plateformes.append(plateforme)
    
# Charger l'image du fond + joueur + PNJ
try:    
    fond = pygame.image.load("Assets/BG5.png").convert_alpha()
    fond = pygame.transform.scale(fond, (LARGEUR, HAUTEUR))
    personnage = pygame.image.load("Assets/pnj.png").convert_alpha()
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
onGround = False
player = pygame.Rect(position_x, position_y, PERSONNAGE_LARGEUR, PERSONNAGE_HAUTEUR)

# Position initiale du PNJ + initialisation
pnj_x = PNJ_DEPART_X
pnj_y = PNJ_DEPART_Y
direction_pnj = 1  # 1 pour droite, -1 pour gauche
pnj_rect = pygame.Rect(pnj_x, pnj_y, PERSONNAGE_LARGEUR, PERSONNAGE_HAUTEUR)

# Variables de mouvement du personnage
vitesse_x = 0
vitesse_y = 0
nombre_sauts = 0
is_running = False  # Variable pour vérifier si la touche Shift est enfoncée

# Fonction de mouvement du personnage
def deplacer_personnage():
    global position_x, position_y, vitesse_x, vitesse_y, nombre_sauts, onGround

    # Appliquer la gravité seulement si le personnage n'est pas sur le sol
    if not onGround:
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
        onGround = True

# Fonction de collision entre le personnage et le PNJ
def collision_pnj():
    global position_x, position_y, vitesse_x, vitesse_y, onGround

    # Vérifier la collision avec la plateforme
    for plat in plateformes:
        if plat.rect.colliderect(player):
            position_y = plat.rect.top - PERSONNAGE_HAUTEUR
            onGround = True
            vitesse_y = 0  # Arrêter le mouvement vertical
            break
    else:
        onGround = False  # Si le personnage n'est plus sur la plateforme, réinitialiser onGround

    # Même chose pour le mouvement vertical
    if vitesse_y > 0:
        if player.colliderect(pnj_rect):
            position_y = pnj_y - PERSONNAGE_HAUTEUR
            vitesse_y = 0  # Arrêter le mouvement vertical
    elif vitesse_y < 0:
        if player.colliderect(pnj_rect):
            position_y = pnj_y + PNJ_HAUTEUR
            vitesse_y = 0  # Arrêter le mouvement vertical

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
                onGround = False
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
            elif event.key == K_SPACE and onGround:  # Réinitialiser le saut si le personnage est déjà sur le sol
                nombre_sauts = 0
            elif event.key == K_DOWN:
                for plat in plateformes:
                    if plat.rect.colliderect(player):
                        position_y = plat.rect.bottom
                        break

    # Déplacer le personnage
    deplacer_personnage()

    # Déplacer le PNJ avec gestion de collision
    pnj_x += direction_pnj * 1

    if pnj_x <= 0 or pnj_x >= LARGEUR - PNJ_LARGEUR:
        direction_pnj *= -1

    # Vérifier la collision entre le personnage et le PNJ
    collision_pnj()

    # Afficher le fond à l'arrière-plan
    fenetre.blit(fond, (0, 0))

    # Afficher le personnage à sa position actuelle
    fenetre.blit(personnage, (position_x, position_y))

    # Afficher les plateformes
    for plat in plateformes:
        fenetre.blit(plat.image, plat.rect)

    # Afficher le PNJ à sa position actuelle
    fenetre.blit(pnj, (pnj_x, pnj_y))

    # Mettre à jour l'affichage
    pygame.display.flip()

    # Limiter la vitesse de rafraîchissement à 60 FPS
    clock.tick(60)

# Quitter Pygame
pygame.quit()
