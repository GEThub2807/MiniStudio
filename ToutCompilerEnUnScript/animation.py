import pygame
import spritesheet
import os

pygame.init()

pygame.display.set_caption('Spritesheets')

# Charger toutes les images du dossier Ampoule_Idle dans une liste
image_list_Ampoule_Idle = []
for filename in os.listdir("Asset/Ampoule_Idle"):
    if filename.endswith(".png"):
        image_list_Ampoule_Idle.append(pygame.image.load(os.path.join("Asset/Ampoule_Idle", filename)).convert_alpha())

sprite_sheet_Ampoule_Idle = spritesheet.SpriteSheet(image_list_Ampoule_Idle)

image_list_Ampoule_Walk = []
for filename in os.listdir("Asset/Ampoule_Marche"):
    if filename.endswith(".png"):
        image_list_Ampoule_Walk.append(pygame.image.load(os.path.join("Asset/Ampoule_Marche", filename)).convert_alpha())

sprite_sheet_Ampoule_Walk = spritesheet.SpriteSheet(image_list_Ampoule_Walk)

image_list_Ampoule_Jump = []
for filename in os.listdir("Asset/Ampoule_Saut"):
    if filename.endswith(".png"):
        image_list_Ampoule_Jump.append(pygame.image.load(os.path.join("Asset/Ampoule_Saut", filename)).convert_alpha())

sprite_sheet_Ampoule_Jump = spritesheet.SpriteSheet(image_list_Ampoule_Jump)

image_list_Mouette_Idle = []
for filename in os.listdir("Asset/PNJ_Mouette_Idle"):
    if filename.endswith(".png"):
        image_list_Mouette_Idle.append(pygame.image.load(os.path.join("Asset/PNJ_Mouette_Idle", filename)).convert_alpha())

sprite_sheet_Mouette_Idle = spritesheet.SpriteSheet(image_list_Mouette_Idle)

image_list_Mouette_Speak = []
for filename in os.listdir("Asset/PNJ_Mouette_Speak"):
    if filename.endswith(".png"):
        image_list_Mouette_Speak.append(pygame.image.load(os.path.join("Asset/PNJ_Mouette_Speak", filename)).convert_alpha())

sprite_sheet_Mouette_Speak = spritesheet.SpriteSheet(image_list_Mouette_Speak)

image_list_BM_Idle = []
for filename in os.listdir("Asset/PNJ_BM_Idle"):
    if filename.endswith(".png"):
        image_list_BM_Idle.append(pygame.image.load(os.path.join("Asset/PNJ_BM_Idle", filename)).convert_alpha())

sprite_sheet_BM_Idle = spritesheet.SpriteSheet(image_list_BM_Idle)

image_list_BM_Speak = []
for filename in os.listdir("Asset/PNJ_Mere_Speak"):
    if filename.endswith(".png"):
        image_list_BM_Speak.append(pygame.image.load(os.path.join("Asset/PNJ_Mere_Speak", filename)).convert_alpha())

sprite_sheet_BM_Speak = spritesheet.SpriteSheet(image_list_BM_Speak)

image_list_Sardine_Idle = []
for filename in os.listdir("Asset/PNJ_Sardine_Idle"):
    if filename.endswith(".png"):
        image_list_Sardine_Idle.append(pygame.image.load(os.path.join("Asset/PNJ_Sardine_Idle", filename)).convert_alpha())

sprite_sheet_Sardine_Idle = spritesheet.SpriteSheet(image_list_Sardine_Idle)

image_list_Sardine_Speak = []
for filename in os.listdir("Asset/PNJ_Sardine_Speak"):
    if filename.endswith(".png"):
        image_list_Sardine_Speak.append(pygame.image.load(os.path.join("Asset/PNJ_Sardine_Speak", filename)).convert_alpha())

sprite_sheet_Sardine_Speak = spritesheet.SpriteSheet(image_list_Sardine_Speak)

image_list_Mouette_Mob = []
for filename in os.listdir("Asset/Mouette_Mob"):
    if filename.endswith(".png"):
        image_list_Mouette_Mob.append(pygame.image.load(os.path.join("Asset/Mouette_Mob", filename)).convert_alpha())

sprite_sheet_Mouette_Mob = spritesheet.SpriteSheet(image_list_Mouette_Mob)

animList = [] #crée le tableau avec les sprites pour l'anim
animSteps = [] #définit le nombre de sprites qui seront affichées
action = 0
lastUpdate = pygame.time.get_ticks()
animCD = 500 #définit le temps de la boucle d'animation
frame = 0
stepCount = 0

for animation in animSteps:
    tempImgList = []
    for _ in range(animation):
        tempImgList.append(sprite_sheet.get_image(stepCount, 24, 24, 3))
        stepCount += 1
    animList.append(tempImgList)

run = True
while run:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

<<<<<<< Updated upstream
    # update bg
    screen.fill(BG)
    
    #update anim
=======
    # Update animation
>>>>>>> Stashed changes
    currentTime = pygame.time.get_ticks()
    if currentTime - lastUpdate >= animCD:
        lastUpdate = currentTime
        frame += 1
        if frame >= len(animList[action]):
            frame = 0

<<<<<<< Updated upstream
    # print les img
    screen.blit(animList[action][frame], (0, 0))
=======
    # Clear the screen
    fenetre.fill((0, 0, 0))

    # Draw the current frame of the animation
    fenetre.blit(animList[action][frame], (0, 0))
>>>>>>> Stashed changes

    # Update the display
    pygame.display.flip()

pygame.quit()