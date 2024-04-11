import pygame
from pygame.locals import *

# Initialisation de Pygame
pygame.init()

# Constants and initial variables
#SCREEN_WIDTH = 1920/2
#SCREEN_HEIGHT = 1080/2
#screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
interactKey = pygame.K_e
pos_intro_x = 100
pos_intro_y = 300

# Font
textFont = pygame.font.SysFont("Arial", 30)
# can replace "Arial" with None. And can pass additional flags like (, bold = true)
# can replace SysFont with Font to use downloaded fonts

# This is where the text is stored
Introduction = ["Me voilà enfin à Marseille !",
                "Plus précisement dans la fameuse rue du panier.",
                "C'est une rue très jolie de par ses graffitis et son ambiance."]
enfantIntro = ["Hey !",
        "Excuse moi de te déranger, j'ai perché ma balle de foot sur les toits de la rue...",
        "Tu pourrai aller la chercher pour moi ?"]
enfantChoix = ["Choix:", "Oui", "Non"]
enfantChoixReponse = 1
enfantChoixOui = ["Génial merci beaucoup !",
                "Utilise les déroulants éléctriques et les blacons pour te hisser sur les toits",
                "Attention, il faut être en rythme!"]
enfantChoixNon = ["Dommage, à la prochaine !"]
enfantSucces = ["Waw ! Merci beaucoup !",
                "Tiens, pour te remercier de m'avoir aidé.",
                "(collectible +1)"]


''' old code, delete this

# Fills the screen gray (prob delete)
#fill = (140, 140, 140)
#screen.fill(fill)
#pygame.display.flip()

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
                            displayTextPrint(dialogList[count], textFont, (0, 0, 0), SCREEN_WIDTH/4, SCREEN_HEIGHT/4) # Display the text
                            pygame.display.flip()
                            
                            # If the list has reached its end, exit the function
                            if len(dialogList) == count + 1:
                                run = False
def Select(arrayLength, dialogList, spacing, diffSelect):
    screen.fill(fill) # Clears the screen
    
    # Display the text
    for x in range(arrayLength):
        displayTextPrint(dialogList[x], textFont, (0, 0, 0), SCREEN_WIDTH/4, SCREEN_HEIGHT/4 + x*spacing)

    # Displays selected text in a different color
    displayTextPrint(dialogList[diffSelect], textFont, (147, 0, 191), SCREEN_WIDTH/4, SCREEN_HEIGHT/4 + (diffSelect)*spacing)
    
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
                        displayTextPrint(dialogList[x], textFont, (0, 0, 0), SCREEN_WIDTH/4, SCREEN_HEIGHT/4 + x*spacing)
                    # Initial selected
                    displayTextPrint(dialogList[1], textFont, (147, 0, 191), SCREEN_WIDTH/4, SCREEN_HEIGHT/4 + spacing)
                    
                    if count == 1:
                        screen.fill(fill) # Clears the screen
                        if selection == qcmBonneReponse:
                            displayTextPrint("Correct!", textFont, (0, 0, 0), SCREEN_WIDTH/4, SCREEN_HEIGHT/4 + spacing)
                        else:
                            displayTextPrint("Faux!", textFont, (0, 0, 0), SCREEN_WIDTH/4, SCREEN_HEIGHT/4 + spacing)
                    
                    # Exit
                    if count == 2:
                        run = False
                    
                    pygame.display.flip() # Refresh
'''