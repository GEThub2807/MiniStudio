import pygame
from pygame.locals import *
from tools import EventHandle
# Constantes
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Menu")

# Initialisation de Pygame
pygame.init()

# Chargement des ressources
try:
    fond = pygame.image.load("Assets/Fond.jpg").convert()
except pygame.error as e:
    print("Erreur lors du chargement des images :", str(e))
    pygame.quit()
    exit()

# Fonction pour obtenir une police
def get_font(size):
    return pygame.font.Font("Assets/klfrances.ttf", size)

# Fonction pour afficher le menu principal
def main_menu():
    running = True
    a = 255
    b = 255
    c = 255
    while running:
        # Gestion des événements
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        # Affichage du fond
        SCREEN.blit(fond, (0, 0))

        # Affichage du texte
        MENU_TEXT = get_font(100).render("Vive la France", True, (a, b, c)) 

        MENU_RECT = MENU_TEXT.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 10))

        PLAY_BUTTON = EventHandle(image=pygame.image.load("Assets/Play Rect.png"), pos=(SCREEN_WIDTH/2, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = EventHandle(image=pygame.image.load("Assets/Options Rect.png"), pos=(SCREEN_WIDTH/2, 400), 
                            text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = EventHandle(image=pygame.image.load("Assets/Quit Rect.png"), pos=(SCREEN_WIDTH/2, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    a = 0
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    pygame.exit()
        pygame.display.update()

def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(SCREEN_WIDTH/2, 260))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_SCREEN_SIZE = EventHandle(image=None, pos=(SCREEN_WIDTH/2, 560), 
                            text_input="ECRAN", font=get_font(75), base_color="Black", hovering_color="Green")
        OPTIONS_BACK = EventHandle(image=None, pos=(SCREEN_WIDTH/2, 460), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_SCREEN_SIZE.changeColor(OPTIONS_MOUSE_POS)

        for button in [OPTIONS_BACK, OPTIONS_SCREEN_SIZE]:
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                pygame.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()
                if OPTIONS_SCREEN_SIZE.checkForInput(OPTIONS_MOUSE_POS):
                    new_width =  800
                    new_height = 400
                    pygame.display.set_mode((new_width, new_height))

        pygame.display.update()
# Lancement du menu principal
main_menu()

# Fermeture de Pygame
pygame.quit()
