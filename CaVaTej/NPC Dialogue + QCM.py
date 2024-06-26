import pygame
from pygame.locals import *

# Initialisation de Pygame
pygame.init()

# Constants and initial variables
SCREEN_WIDTH = 1920/2
SCREEN_HEIGHT = 1080/2
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
interactKey = pygame.K_e

# This is where the text is stored
firstTextList = ["texte 1", "texte 2", "texte 3"]
qcm = ["QCM:", "reponse fausse", "reponse vraie", "reponse fausse", "reponse fausse"]
qcmBonneReponse = 2

# Fills the screen gray
fill = (140, 140, 140)
screen.fill(fill)
pygame.display.flip()

# Creates the text box into an image then includes it into the scene
def displayText(text, font, textColor, x, y):
    img = font.render(text, True, textColor)
    screen.blit(img, (x, y))

# Font
textFont = pygame.font.SysFont("Arial", 30)
# can replace "Arial" with None. And can pass additional flags like (, bold = true)
# can replace SysFont with Font to use downloaded fonts

count = -1

def NPCDialog(count, dialogList, interactKey):
    run = True
    while run:
        for event in pygame.event.get():
                    # Exits the game when clicking the X
                    if event.type == pygame.QUIT:
                        run = False
                    # Displays the text
                    if event.type == pygame.KEYDOWN:
                        pressed = pygame.key.get_pressed()
                        if pressed[interactKey]:
                            count += 1
                            screen.fill(fill) # Clears the screen
                            displayText(dialogList[count], textFont, (0, 0, 0), SCREEN_WIDTH/4, SCREEN_HEIGHT/4) # Display the text
                            pygame.display.flip()
                            
                            # If the list has reached its end, exit the function
                            if len(dialogList) == count + 1:
                                run = False

def Select(arrayLength, dialogList, spacing, diffSelect):
    screen.fill(fill) # Clears the screen
    
    # Display the text
    for x in range(arrayLength):
        displayText(dialogList[x], textFont, (0, 0, 0), SCREEN_WIDTH/4, SCREEN_HEIGHT/4 + x*spacing)

    # Displays selected text in a different color
    displayText(dialogList[diffSelect], textFont, (147, 0, 191), SCREEN_WIDTH/4, SCREEN_HEIGHT/4 + (diffSelect)*spacing)
    
    # Refreshes the screen
    pygame.display.flip()

def NPCQCM(count, dialogList, interactKey, qcmBonneReponse):
    run = True
    spacing = 50
    selection = 1
    
    while run:
        for event in pygame.event.get():
            # Exits the game when clicking the X
            if event.type == pygame.QUIT:
                run = False
            # Displays the text
            if event.type == pygame.KEYDOWN:
                pressed = pygame.key.get_pressed()
                if pressed[interactKey]:
                    count += 1
                    screen.fill(fill) # Clears the screen
                    
                    # Display the text
                    arrayLength = len(dialogList)
                    for x in range(arrayLength):
                        displayText(dialogList[x], textFont, (0, 0, 0), SCREEN_WIDTH/4, SCREEN_HEIGHT/4 + x*spacing)
                    # Initial selected
                    displayText(dialogList[1], textFont, (147, 0, 191), SCREEN_WIDTH/4, SCREEN_HEIGHT/4 + spacing)
                    
                    if count == 1:
                        screen.fill(fill) # Clears the screen
                        if selection == qcmBonneReponse:
                            displayText("Correct!", textFont, (0, 0, 0), SCREEN_WIDTH/4, SCREEN_HEIGHT/4 + spacing)
                        else:
                            displayText("Faux!", textFont, (0, 0, 0), SCREEN_WIDTH/4, SCREEN_HEIGHT/4 + spacing)
                    
                    # Exit
                    if count == 2:
                        run = False
                    
                    pygame.display.flip() # Refresh
                    
                # Selection
                if pressed[pygame.K_UP] and selection > 1: # Up
                    Select(arrayLength, dialogList, spacing, selection - 1)
                    selection = selection - 1
                
                if pressed[pygame.K_DOWN] and selection < (len(qcm)-1): # Down
                    Select(arrayLength, dialogList, spacing, selection + 1)
                    selection = selection + 1


#NPCDialog(count, firstTextList, interactKey)
NPCQCM(count, qcm, interactKey, qcmBonneReponse)


# Fermeture de Pygame
pygame.quit()



#testing for resize, delete this if we are not gonna do anything with it
'''
screen = pygame.display.set_mode((500, 500), HWSURFACE | DOUBLEBUF | RESIZABLE)
pic = pygame.image.load("image.png")
screen.blit(pygame.transform.scale(pic, (500, 500)), (0, 0))
pygame.display.flip()

if event.type == pygame.VIDEORESIZE:
    screen = pygame.display.set_mode(
        event.dict['size'], pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
    screen.blit(pygame.transform.scale(pic, event.dict['size']), (0, 0))
    pygame.display.flip()
'''