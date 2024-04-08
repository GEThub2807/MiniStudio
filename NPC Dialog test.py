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
firstTextList = ["text 1", "text 2", "text 3"]
qcm = ["QCM time!", "reponse 1", "reponse 2", "reponse 3"]

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


def NPCQCM(count, dialogList, interactKey):
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
                    pygame.display.flip()
                    
                    # Exit
                    if count == 1:
                        run = False
                    
                
                # Selection
                
                if pressed[pygame.K_UP] and selection > 1:
                    screen.fill(fill) # Clears the screen
                    
                    # Display the text
                    for x in range(arrayLength):
                        displayText(dialogList[x], textFont, (0, 0, 0), SCREEN_WIDTH/4, SCREEN_HEIGHT/4 + x*spacing)
                    
                    selection = selection - 1
                    displayText(dialogList[selection], textFont, (147, 0, 191), SCREEN_WIDTH/4, SCREEN_HEIGHT/4 + selection*spacing)
                    
                    pygame.display.flip()
                    
                if pressed[pygame.K_DOWN] and selection < 3:
                    screen.fill(fill) # Clears the screen
                    
                    # Display the text
                    for x in range(arrayLength):
                        displayText(dialogList[x], textFont, (0, 0, 0), SCREEN_WIDTH/4, SCREEN_HEIGHT/4 + x*spacing)
                    
                    selection = selection + 1
                    displayText(dialogList[selection], textFont, (147, 0, 191), SCREEN_WIDTH/4, SCREEN_HEIGHT/4 + selection*spacing)
                    
                    pygame.display.flip()


#NPCDialog(count, firstTextList, interactKey)
NPCQCM(count, qcm, interactKey)




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