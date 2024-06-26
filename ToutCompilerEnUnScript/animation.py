import pygame
import spritesheet

LARGEUR = 1920  # Largeur de la fenêtre du jeu
HAUTEUR = 1080  # Hauteur de la fenêtre du jeu

pygame.init()

pygame.display.set_caption('Spritesheets')

fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))

sprite_sheet_image = pygame.image.load("Assets/anim.png").convert_alpha()
sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)

BG = (50, 50, 50)
BLACK = (0, 0, 0)

animList = [] #crée le tableau avec les sprites pour l'anim
animSteps = [4, 6, 3 , 4] #définit le nombre de sprites qui seront affichées
action = 0
lastUpdate = pygame.time.get_ticks()
animCD = 500 #définit le temps de la boucle d'animation
frame = 0
stepCount = 0

for animation in animSteps:
    tempImgList = []
    for _ in range(animation):
        tempImgList.append(sprite_sheet.get_image(stepCount, 24, 24, 3, BLACK))
        stepCount += 1
    animList.append(tempImgList)

run = True
while run:

    # update bg
    fenetre.fill(BG)
    
    #update anim
    currentTime = pygame.time.get_ticks()
    if currentTime - lastUpdate >= animCD:
        frame += 1
        lastUpdate = currentTime
        if frame >= len(animList[action]):
            frame = 0

    # print les img
    fenetre.blit(animList[action][frame], (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            
            run = False

    pygame.display.update()

pygame.quit()