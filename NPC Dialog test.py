import pygame
from pygame.locals import *


# Initialisation de Pygame
pygame.init()

# Constants and initial variables
SCREEN_WIDTH = 1920/2
SCREEN_HEIGHT = 1080/2
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


# Content
def NPCDialog():
    
    # Font
    textFont = pygame.font.SysFont("Arial", 30)
    # can replace "Arial" with None. And can pass additional flags like (, bold = true)
    # can replace SysFont with Font to use downloaded fonts
    
    # Creates the text box into an image then includes it into the scene
    def displayText(text, font, textColor, x, y):
        img = font.render(text, True, textColor)
        screen.blit(img, (x, y))
    
    # Fills the screen gray
    screen.fill((140, 140, 140))
    pygame.display.flip()

    # Dialog text
    dialogList = ["1", "2"]


    # Main loop
    run = True
    count = -1
    while run:
        
        for event in pygame.event.get():
            # Exits the game when clicking the X
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                pressed = pygame.key.get_pressed()
                if pressed[pygame.K_e]:
                    count += 1
                    displayText(dialogList[count], textFont, (0, 0, 0), 960/2, 540/2)
                    pygame.display.flip()
                
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

NPCDialog()

# Fermeture de Pygame
pygame.quit()