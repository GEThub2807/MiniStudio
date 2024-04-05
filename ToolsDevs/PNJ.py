from Main import *

PNJ_LARGEUR = 50
PNJ_HAUTEUR = 50

class PNJ:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def block_player(self, personnage):
        if personnage > self.x:
            self.x += 1
        elif personnage < self.x:
            self.x -= 1

# Exemple d'utilisation
pnj = PNJ(3, 5)
pnj.block_player(personnage)
print(pnj.x)  # Affiche 4 si le joueur se trouve à droite du PNJ, 2 si le joueur se trouve à gauche
try:
    pnj = pygame.image.load("Assets/pnj.png").convert()
    pnj = pygame.transform.scale(pnj, (PNJ_LARGEUR, PNJ_HAUTEUR))
except pygame.error as e:
    print("Erreur lors du chargement des images :", str(e))
    pygame.quit()
    exit()