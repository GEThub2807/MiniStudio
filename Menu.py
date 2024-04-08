import pygame
from pygame.locals import *
from tools import EventHandle

pygame.init()

pygame.mixer.init()
pygame.mixer.music.load("Assets/main_theme.mp3")
click_sound = pygame.mixer.Sound("Assets/Kudasai.mp3")
pygame.mixer.music.play()

screen_info = pygame.display.Info()
SCREEN_HEIGHT = screen_info.current_h
SCREEN_WIDTH = SCREEN_HEIGHT * 16/9
FULLSCREEN = True

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Menu")

try:
    fond = pygame.image.load("Assets/background.jpg").convert()
except pygame.error as e:
    print("Erreur lors du chargement des images :", str(e))
    pygame.quit()
    exit()

def get_font(size):
    return pygame.font.Font("Assets/klfrances.ttf", size)

def main_menu():
    global SCREEN_WIDTH, SCREEN_HEIGHT, FULLSCREEN
    running = True
    a = 255
    b = 255
    c = 255
    
    play_button_pos = (SCREEN_WIDTH/2, SCREEN_HEIGHT * 0.25)
    options_button_pos = (SCREEN_WIDTH/2, SCREEN_HEIGHT * 0.4)
    credit_button_pos = (SCREEN_WIDTH/2, SCREEN_HEIGHT * 0.55)
    quit_button_pos = (SCREEN_WIDTH/2, SCREEN_HEIGHT * 0.7)

    
    while running:

        MENU_MOUSE_POS = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        SCREEN.blit(fond, (0, 0))

        MENU_TEXT = get_font(100).render("Vive la France", True, (a, b, c)) 
        MENU_RECT = MENU_TEXT.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 10))
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        PLAY_BUTTON = EventHandle(image=pygame.image.load("Assets/Play Rect.png"), pos=play_button_pos, 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = EventHandle(image=pygame.image.load("Assets/Play Rect.png"), pos=options_button_pos, 
                            text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        CREDIT_BUTTON = EventHandle(image=pygame.image.load("Assets/Play Rect.png"), pos=credit_button_pos, 
                            text_input="CREDIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = EventHandle(image=pygame.image.load("Assets/Play Rect.png"), pos=quit_button_pos, 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON, CREDIT_BUTTON]:
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_sound
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    a = 0
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if CREDIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    credit()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    pygame.exit()
        pygame.display.update()

def credit():
    global SCREEN_WIDTH, SCREEN_HEIGHT, FULLSCREEN
    while True:
        SCREEN.fill("white")

        CREDIT_TECH_TEXT = get_font(90).render("Gtech", True, "Black")
        TECH = get_font(45).render("Antoine Elouan Mathis Nathan Timothe Valentin", True, "Black")
        CREDIT_BS_TEXT = get_font(90).render("BS", True, "Black")
        BS = get_font(45).render("Anthony Kevin Theophile Titouan Manon", True, "Black")
        CREDIT_ART_TEXT = get_font(90).render("Art", True, "Black")
        ART = get_font(45).render("Louis Alan Leo Eleonore", True, "Black")

        vertical_spacing = 150  

        vertical_position = SCREEN_HEIGHT * 0.15

        RECT_CREDIT_TECH_TEXT = CREDIT_TECH_TEXT.get_rect(center=(SCREEN_WIDTH/2, vertical_position))
        RECT_TECH = TECH.get_rect(center=(SCREEN_WIDTH/2, vertical_position + vertical_spacing))
        RECT_CREDIT_BS_TEXT = CREDIT_BS_TEXT.get_rect(center=(SCREEN_WIDTH/2, vertical_position + 2 * vertical_spacing))
        RECT_BS = BS.get_rect(center=(SCREEN_WIDTH/2, vertical_position + 3 * vertical_spacing))
        RECT_CREDIT_ART_TEXT = CREDIT_ART_TEXT.get_rect(center=(SCREEN_WIDTH/2, vertical_position + 4 * vertical_spacing))
        RECT_ART = ART.get_rect(center=(SCREEN_WIDTH/2, vertical_position + 5 * vertical_spacing))

        SCREEN.blit(CREDIT_TECH_TEXT, RECT_CREDIT_TECH_TEXT)
        SCREEN.blit(TECH, RECT_TECH)
        SCREEN.blit(CREDIT_BS_TEXT, RECT_CREDIT_BS_TEXT)
        SCREEN.blit(BS, RECT_BS)
        SCREEN.blit(CREDIT_ART_TEXT, RECT_CREDIT_ART_TEXT)
        SCREEN.blit(ART, RECT_ART)

        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        OPTIONS_BACK = EventHandle(image=None, pos=(SCREEN_WIDTH/2, SCREEN_HEIGHT * 0.44), 
                                text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")
        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()  
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_sound.play()
                main_menu()

        pygame.display.update()



def options():
    global SCREEN_WIDTH, SCREEN_HEIGHT, FULLSCREEN
    volume_slider_width = 200
    volume_slider_height = 20
    volume_slider_x = (SCREEN_WIDTH - volume_slider_width) // 2
    volume_slider_y = SCREEN_HEIGHT // 2
    volume_min = 0
    volume_max = 100
    volume = pygame.mixer.music.get_volume() * volume_max
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        pygame.draw.rect(SCREEN, "gray", (volume_slider_x, volume_slider_y, volume_slider_width, volume_slider_height))
        pygame.draw.rect(SCREEN, "green", (volume_slider_x, volume_slider_y, (volume / volume_max) * volume_slider_width, volume_slider_height))


        OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "Black")
        VOLUME = get_font(45).render("VOLUME", True, "Black")
        RECT_VOLUME = VOLUME.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT * 0.64))
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT * 0.24))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT,RECT_VOLUME)
        if FULLSCREEN == True:
            OPTIONS_SCREEN_SIZE = EventHandle(image=None, pos=(SCREEN_WIDTH/2, SCREEN_HEIGHT * 0.54), 
                                text_input="FENETRER", font=get_font(75), base_color="Black", hovering_color="Green")
        else:
            OPTIONS_SCREEN_FULL = EventHandle(image=None, pos=(SCREEN_WIDTH/2, SCREEN_HEIGHT * 0.54), 
                        text_input="PLEIN ECRAN", font=get_font(75), base_color="Black", hovering_color="Green")
        OPTIONS_BACK = EventHandle(image=None, pos=(SCREEN_WIDTH/2, SCREEN_HEIGHT * 0.44), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        if FULLSCREEN == True:
            OPTIONS_SCREEN_SIZE.changeColor(OPTIONS_MOUSE_POS)
        else:
            OPTIONS_SCREEN_FULL.changeColor(OPTIONS_MOUSE_POS)

        for button in [OPTIONS_BACK]:
            button.update(SCREEN)

        if FULLSCREEN == True:
            OPTIONS_SCREEN_SIZE.update(SCREEN)
        else:
            OPTIONS_SCREEN_FULL.update(SCREEN)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == VIDEORESIZE:
                pygame.time.delay(200)
                new_height = screen_info.current_h
                new_width = new_height * 16/9
                pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)
                SCREEN_WIDTH, SCREEN_HEIGHT = new_width, new_height
            if event.type == pygame.MOUSEBUTTONDOWN:
                if volume_slider_x <= OPTIONS_MOUSE_POS[0] <= volume_slider_x + volume_slider_width and \
                    volume_slider_y <= OPTIONS_MOUSE_POS[1] <= volume_slider_y + volume_slider_height:
                    # Mettre à jour le volume en fonction de la position du curseur
                    volume = max(0, min((OPTIONS_MOUSE_POS[0] - volume_slider_x) / volume_slider_width * volume_max, volume_max))
                    pygame.mixer.music.set_volume(volume / volume_max)

                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()
                if FULLSCREEN == True and OPTIONS_SCREEN_SIZE.checkForInput(OPTIONS_MOUSE_POS):
                    new_width = 1280
                    new_height = 720
                    FULLSCREEN = False
                    pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)
                    SCREEN_WIDTH, SCREEN_HEIGHT = new_width, new_height
                elif FULLSCREEN == False and OPTIONS_SCREEN_FULL.checkForInput(OPTIONS_MOUSE_POS):
                    new_width = screen_info.current_w
                    new_height = screen_info.current_h
                    FULLSCREEN = True
                    pygame.display.set_mode((new_width, new_height))
                    SCREEN_WIDTH, SCREEN_HEIGHT = new_width, new_height

        pygame.display.update()
main_menu()
pygame.quit()
