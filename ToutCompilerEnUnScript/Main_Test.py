import pygame
from pygame.locals import *
from NPCDialogueQCM import *
from random import randint
import time
from random import *
import spritesheet
from plateformes import PlateformesRythm


class Jeu:
    @staticmethod
    def run_game():
        # Constantes
        LARGEUR = 1920  # Largeur de la fenêtre du jeu
        HAUTEUR = 1080  # Hauteur de la fenêtre du jeu

        # Constantes JOUEUR
        GRAVITE = 0.5
        VITESSE_X = 5
        VITESSE_Y = 10
        VITESSE_COURSE = 10  # Vitesse de déplacement en mode course
        PERSONNAGE_LARGEUR = 100  # Largeur du personnage
        PERSONNAGE_HAUTEUR = 70  # Hauteur du personnag
        GREEN = (144, 201, 120)
        scroll = 0

        # Constantes PLATEFORME
        PLATEFORME_LARGEUR = 145  # Largeur de la plateforme
        PLATEFORME_HAUTEUR = 20  # Hauteur de la plateforme

        # Points de départ et d'arrivée du PNJ
        PNJ_LARGEUR = 70
        PNJ_HAUTEUR = 130
        PNJ_DEPART_X = 500
        PNJ_DEPART_Y = HAUTEUR - PNJ_HAUTEUR
        PNJ_ARRIVEE_X = 600
        PNJ_ARRIVEE_Y = HAUTEUR - PNJ_HAUTEUR

        # COULEUR
        COLOR = (255, 0, 0)

        # Initialisation de Pygame
        pygame.init()

        # Définir la taille de la fenêtre du jeu
        fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))

        # Position de la plateforme
        x = 35 # x pixels du bord gauche de l'écran
        y = HAUTEUR - PLATEFORME_HAUTEUR - 75  # x pixels du bas de l'écran
        # --------------------------------------------------Chargement des images des personnages et du fond, début, Antoine------------------------------------------
        try:
            fond = pygame.image.load("Asset/Rue_du_panier.png").convert_alpha()
            fond = pygame.transform.scale(fond, (LARGEUR, HAUTEUR))
            Length_Fond: tuple[int, int] = fond.get_size()
            ground = pygame.image.load("Asset/SOL.png").convert_alpha()
            fenetre.blit(ground, (0, HAUTEUR - ground.get_height()))
            personnage = pygame.image.load("Asset/Bulb/Ampoule_Idle/Ampoule_idle0001.png").convert_alpha()
            personnage = pygame.transform.scale(personnage, (PERSONNAGE_LARGEUR, PERSONNAGE_HAUTEUR))
            pnj = pygame.image.load("Assets/PNJ.png").convert_alpha()
            pnj = pygame.transform.scale(pnj, (PNJ_LARGEUR, PNJ_HAUTEUR))

        except pygame.error as e:
            print("Erreur lors du chargement de l'image du fond :", str(e))
            pygame.quit()
            exit()
        # --------------------------------------------------Chargement des images des personnages et du fond fin------------------------------------------
        # ----------------------------------------------------Initialisation variables persos et cam, début, Valentin-------------------------------------
        # Position initiale du personnage
        position_x = 0
        position_y = Length_Fond[1] - 501

        # Variables de mouvement du personnage
        vitesse_x = 0
        vitesse_y = 0
        nombre_sauts = 2
        is_running = False  # Variable pour vérifier si la touche Shift est enfoncée

        # Position initiale de la caméra
        camera_x = 0
        camera_y = 0

        # Taille de la zone de la caméra
        CAMERA_LARGEUR = LARGEUR // 2
        CAMERA_HAUTEUR = HAUTEUR // 2

        # Position initiale des pnjs
        npc_pos_x = Length_Fond[0]
        npc_pos_y = Length_Fond[1] - 300
        # ----------------------------------------------------Initialisation variables persos et cam, Fin-------------------------------------
        # -----------------------------------------------------------Systèmes des NPC, Début, Antoine---------------------------------------------
        # Fonction pour déplacer les PNJs
        class NPC:
            def __init__(self, asset_folder_path, initial_x, spawn_y, velocity):
                # self.images = images
                self.image_index = 0
                # self.image = images[self.image_index]
                self.pos_x = initial_x
                self.spawn_y = spawn_y
                self.pos_y = spawn_y
                self.velocity = velocity
                self.sprite: spritesheet.Sprite = spritesheet.Sprite(asset_folder_path)
                self.size = self.sprite.get_size()

            def update(self, dt):
                self.pos_x -= self.velocity

                # Vérifier si le PNJ est hors de l'écran à gauche ou à droite
                if self.pos_x <= 0 - self.size[0] and self.velocity < 0:
                    self.destroy()

                self.sprite.update(dt)

            def draw(self, screen, camera_x, camera_y):
                # screen.blit(self.image, (self.pos_x - camera_x, self.pos_y - camera_y))
                self.sprite.draw(screen, self.pos_x - camera_x, self.pos_y - camera_y)

            def destroy(self):
                # Code pour détruire le NPC
                self.pos_x = -1000  # Déplacer le NPC hors de l'écran
                self.pos_y = -1000
                self.velocity = 0  # Arrêter le mouvement

        # Créer une instance de la classe NPC
        npc_assets_folder = ["Asset/PNJ_Bm", "Asset/PNJ_Sardine", "Asset/PNJ_Seagull"]
        # npc = NPC(npc_images, randint(0, Length_Fond[0]), Length_Fond[1] - 700, NPC_VITESSE)

        import random

        class NPCManager:
            def __init__(self, spawn_interval):
                self.spawn_interval = spawn_interval  # Intervalle de spawn en secondes pour les PNJs
                self.last_spawn_time = time.time()  # Temps du dernier spawn de PNJ
                self.last_fish_spawn_time = time.time()  # Temps du dernier spawn de poisson
                self.npcs = []  # Liste des PNJs

            def update(self):
                current_time = time.time()
                # Vérifier si le temps écoulé depuis le dernier spawn de PNJ est supérieur à l'intervalle
                if current_time - self.last_spawn_time >= self.spawn_interval:
                    # Ajouter un nouveau PNJ
                    npc = self.spawn_npc()  # Créer une nouvelle instance de NPC
                    self.npcs.append(npc)
                    # Mettre à jour le temps du dernier spawn de PNJ
                    self.last_spawn_time = current_time

            def spawn_npc(self):
                # Coordonnées initiales aléatoires dans les limites de l'écran
                initial_x = LARGEUR + Length_Fond[0] - camera_x  # Utiliser lengthNpc pour obtenir la taille du PNJ
                spawn_y = Length_Fond[1] - 500
                velocity = 5

                self.image_index = randint(0, len(npc_assets_folder) - 1)
                return NPC(npc_assets_folder[self.image_index], initial_x, spawn_y, velocity)

        spawn_interval = 3  # Intervalle de spawn en secondes pour les PNJs
        npc_manager = NPCManager(spawn_interval)

        # -----------------------------------------------------------Systèmes des NPC, Fin, Antoine---------------------------------------------
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

                if rect.right < self.Rect.left:
                    return 0, 0
                if rect.left > self.Rect.right:
                    return 0, 0
                if rect.top > self.Rect.bottom:
                    return 0, 0
                if rect.bottom < self.Rect.top:
                    return 0, 0

                distances: list[int] = []
                distances.append(abs(rect.right - self.Rect.left))
                distances.append(abs(rect.left - self.Rect.right))
                distances.append(abs(rect.bottom - self.Rect.top))
                distances.append(abs(rect.top - self.Rect.bottom))

                minDistance = 2000
                side: int = 0
                for i in range(0, len(distances)):
                    if minDistance > distances[i]:
                        minDistance = distances[i]
                        side = i + 1
                
                return side, minDistance

        plateformes = []

        plateforme_positions = [(35, HAUTEUR - PLATEFORME_HAUTEUR - 75), #1
                                (465, HAUTEUR - PLATEFORME_HAUTEUR - 75), #2
                                (902, HAUTEUR - PLATEFORME_HAUTEUR - 68), #3
                                (1112, HAUTEUR - PLATEFORME_HAUTEUR - 61),#4
                                (1290, HAUTEUR - PLATEFORME_HAUTEUR - 61),#5
                                (1728, HAUTEUR - PLATEFORME_HAUTEUR - 60),#6
                                (1728, HAUTEUR - PLATEFORME_HAUTEUR - 271),#7
                                (1410, HAUTEUR - PLATEFORME_HAUTEUR - 271),#8
                                (1518, HAUTEUR - PLATEFORME_HAUTEUR - 271),#8-2
                                (1217, HAUTEUR - PLATEFORME_HAUTEUR - 271),#9
                                (1112, HAUTEUR - PLATEFORME_HAUTEUR - 271),#9-2
                                (902, HAUTEUR - PLATEFORME_HAUTEUR - 288),#10
                                (685, HAUTEUR - PLATEFORME_HAUTEUR - 288),#11
                                (482, HAUTEUR - PLATEFORME_HAUTEUR - 308),#12
                                (252, HAUTEUR - PLATEFORME_HAUTEUR - 308),#13
                                (35, HAUTEUR - PLATEFORME_HAUTEUR - 308),#14
                                (35, HAUTEUR - PLATEFORME_HAUTEUR - 515),#15
                                (252, HAUTEUR - PLATEFORME_HAUTEUR - 515),#16
                                (482, HAUTEUR - PLATEFORME_HAUTEUR - 515),#17
                                (685, HAUTEUR - PLATEFORME_HAUTEUR - 520),#18
                                (902, HAUTEUR - PLATEFORME_HAUTEUR - 520),#19
                                (1410, HAUTEUR - PLATEFORME_HAUTEUR - 490),#20
                                (1518, HAUTEUR - PLATEFORME_HAUTEUR - 490),#20-2
                                (1217, HAUTEUR - PLATEFORME_HAUTEUR - 490),#21
                                (1112, HAUTEUR - PLATEFORME_HAUTEUR - 490),#21-2
                                (1728, HAUTEUR - PLATEFORME_HAUTEUR - 490),#22
                                (1728, HAUTEUR - PLATEFORME_HAUTEUR - 650),#22
                                # Ajoutez autant de positions de plateformes que vous le souhaitez
                                ]

        def ajouter_plateforme(x, y):
            plateforme = PlateformeBalcon(x, y)
            plateformes.append(plateforme)
            
        # Charger l'image du fond + joueur + PNJ


        #load images
        def load_images():
            global sky_img, Notre_dame, ground, initial_ground_height
            sky_img = pygame.image.load("sky.png")
            Notre_dame = pygame.image.load("bonne_mere.png")
            ground = pygame.image.load("sol.png")
            initial_ground_height = ground.get_height() # Stocker la hauteur initiale du sol

        #store tiles in a list
        img_list = []

        #create function for drawing background
        def draw_bg():
            fenetre.fill(GREEN)
            width = sky_img.get_width()
            for x in range(4):
                fenetre.blit(sky_img, ((x * width) - scroll * 0.5, 0))
                fenetre.blit(Notre_dame, ((x * width) - scroll * 0.6, 0))
            fenetre.blit(ground, (0, 100 - initial_ground_height)) # Utiliser la hauteur initiale du sol

        # Position initiale du personnage
        position_x = 100
        position_y = 1000
        onGround = False
        player = pygame.Rect(position_x, position_y, PERSONNAGE_LARGEUR, PERSONNAGE_HAUTEUR)

        # Position initiale du PNJ
        pnj_x = PNJ_DEPART_X
        pnj_y = PNJ_DEPART_Y

        # Variables de mouvement du personnage
        vitesse_x = 0
        vitesse_y = 0
        nombre_sauts = 0
        is_running = False  # Variable pour vérifier si la touche Shift est enfoncée

        # Variable de direction du PNJ
        direction_pnj = 1  # 1 pour droite, -1 pour gauche

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

        # Fonction pour déplacer la caméra
        def Deplacer_Camera():
            nonlocal camera_x, camera_y

            delta_x = position_x - (camera_x + CAMERA_LARGEUR // 2)
            delta_y = position_y - (camera_y + CAMERA_HAUTEUR // 2)

            if camera_x <= 0 and delta_x < 0:
                delta_x = 0

            if camera_x + LARGEUR >= Length_Fond[0] and delta_x > 0:
                delta_x = 0

            if camera_y <= 0 and delta_y < 0:
                delta_y = 0

            if camera_y + HAUTEUR >= Length_Fond[1] and delta_y > 0:
                delta_y = 0

            camera_x += delta_x * 0.1
            camera_y += delta_y * 0.1

        def Print_FPS(fps):
            pygame.draw.rect(fenetre, (0, 0, 0), (1620, 0, 300, 50))
            fenetre.blit(font.render("FPS: " + fps, 1, (255, 255, 255)), (1630, 0))

        # Fonction de collision entre le personnage et le PNJ
        # Modifier la fonction de collision
        # Modifier la fonction de collision avec la plateforme
        def collision_pnj():
            global position_x, position_y, vitesse_x, vitesse_y, onGround

            # Vérifier la collision avec la plateforme
            if PlateformCollision(pygame.Rect(x,y,PLATEFORME_LARGEUR,PLATEFORME_HAUTEUR), player): 
                position_y = y - PERSONNAGE_HAUTEUR
                onGround = True
                vitesse_y = 0  # Arrêter le mouvement vertical
            else:
                onGround = False  # Si le personnage n'est plus sur la plateforme, réinitialiser onGround

            # Même chose pour le mouvement vertical
            if vitesse_y > 0:
                if position_x + PERSONNAGE_LARGEUR > pnj_x and position_x < pnj_x + PNJ_LARGEUR:
                    if position_y + PERSONNAGE_HAUTEUR > pnj_y and position_y < pnj_y + PNJ_HAUTEUR:
                        position_y = pnj_y - PERSONNAGE_HAUTEUR
                        vitesse_y = 0  # Arrêter le mouvement vertical
            elif vitesse_y < 0:
                if position_x + PERSONNAGE_LARGEUR > pnj_x and position_x < pnj_x + PNJ_LARGEUR:
                    if position_y < pnj_y + PNJ_HAUTEUR and position_y + PERSONNAGE_HAUTEUR > pnj_y:
                        position_y = pnj_y + PNJ_HAUTEUR
                        vitesse_y = 0  # Arrêter le mouvement vertical

        def PlateformCollision(PlatRect, PlayerRect):
                if (PlatRect.left + PlatRect.width >= PlayerRect.left and 
                    PlatRect.left <= PlayerRect.left + PlayerRect.width and
                    PlatRect.top + PlatRect.height >= PlayerRect.bottom - 10  and 
                    PlatRect.top <= PlayerRect.top + PlayerRect.height): #Collision avec le sol  
                    return True
                return False






        # Creates the text box into an image then includes it into the scene
        def displayTextPrint(text, font, textColor, x, y, fenetre):
            img = font.render(text, True, textColor)
            fenetre.blit(img, (x, y))

        # Quelques variables
        running = True
        clock = pygame.time.Clock()
        afficherTexte = False
        afficherQCM = False
        count = -1
        playIntro = True
        playEnfant = False
        choixEnfant = False
        textColor = (255, 255, 255)
        textColorSelected = (17, 255, 0)

        # -----------------------------------------------------------Déclaration de variables et autres, début-------------------------------------------------
        Timer = 0
        Loop = 1
        pygame.time.set_timer(USEREVENT, 1000)
        # Charge la police d'écriture installé
        font = pygame.font.Font("Assets/Parisish.ttf", 50)
        # -----------------------------------------------------------Déclaration de variables et autres, fin-------------------------------------------------

        # QCM specific
        run = True
        spacing = 30
        selection = 1

        # Boucle principale du jeu
        while running:
            # Afficher le fond à l'arrière-plan
            fenetre.blit(fond, (0, 0))
            
            # Display dialog partie trigger
            if afficherTexte == True:
                displayTextPrint(currentText[count], textFont, textColor, pos_intro_x, pos_intro_y, fenetre)

            if afficherQCM == True:
                # Selected
                displayTextPrint(enfantChoix[selection], textFont, textColorSelected, pos_intro_x, pos_intro_y + selection*spacing, fenetre)
                # Display QCM
                for x in range(arrayLength):
                    displayTextPrint(enfantChoix[x], textFont, textColor, pos_intro_x, pos_intro_y + x*spacing, fenetre)





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








                    # There has to be a better way than this, but i cant figure it out so this is fine
                    # Dialogue intro
                    elif event.key == interactKey and len(Introduction) != count and playIntro == True:
                        currentText = Introduction
                        count += 1
                        afficherTexte = True
                        pygame.display.flip()

                        # If the list has reached its end, exit the function and play the next one
                        if len(Introduction) == count:
                            afficherTexte = False
                            count = -1
                            playIntro = False
                            playEnfant = True
                    
                    # Dialogue intro question enfant (copy paste)
                    elif event.key == interactKey and len(enfantIntro) != count and playEnfant == True:
                        currentText = enfantIntro
                        count += 1
                        afficherTexte = True
                        pygame.display.flip()

                        if len(Introduction) == count and choixEnfant == False:
                            afficherTexte = False
                            count = -1
                            playEnfant = False
                            choixEnfant = True
                        
                        if choixEnfant == True:
                            count = count + 1
                            arrayLength = len(enfantChoix)
                            afficherQCM = True
                            count = -1
                            playQCM = True
                    
                    # Selection
                    elif event.key == pygame.K_UP and selection > 1 and choixEnfant == True: # Up
                        selection = selection - 1
                        
                    elif event.key == pygame.K_DOWN and selection < (len(enfantChoix)-1) and choixEnfant == True: # Down
                        selection = selection + 1
                    
                    # Choix
                    elif event.key == interactKey and len(enfantChoixOui) != count and playQCM == True:
                        afficherQCM = False
                        choixEnfant = False
                        
                        if selection == enfantChoixReponse:
                            currentText = enfantChoixOui
                        else:
                            currentText = enfantChoixNon
                        
                        count = count + 1
                        afficherTexte = True
                        pygame.display.flip()
                        
                        if len(enfantChoixOui) == count and currentText == enfantChoixOui:
                            playQCM = False
                            afficherTexte = False
                            count = -1
                            enfantSuccesDialogue = True
                            
                        if len(enfantChoixNon) == count and currentText == enfantChoixNon:
                            playQCM = False
                            afficherQCM = False
                            afficherTexte = False
                            count = -1
                            playEnfant = True
                            selection = 1
                    
                    elif event.key == interactKey and len(Introduction) != count and enfantSuccesDialogue == True:
                        currentText = enfantSucces
                        count += 1
                        afficherTexte = True
                        pygame.display.flip()

                        # If the list has reached its end, exit the function and play the next one
                        if len(Introduction) == count:
                            afficherTexte = False
                            count = -1
                            enfantSuccesDialogue = False






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
                    elif event.key == K_DOWN and PlateformCollision(pygame.Rect(x,y,PLATEFORME_LARGEUR,PLATEFORME_HAUTEUR), pygame.Rect(position_x,position_y,PERSONNAGE_LARGEUR,PERSONNAGE_HAUTEUR)): 
                        position_y = y + PLATEFORME_HAUTEUR  # Descendre du collider
            
            # Déplacer le personnage
            deplacer_personnage()

            # Déplacer le PNJ avec gestion de collision
            pnj_x += direction_pnj * 1

            if pnj_x <= 0 or pnj_x >= LARGEUR - PNJ_LARGEUR:
                direction_pnj *= -1

            # Vérifier la collision entre le personnage et le PNJ
            collision_pnj()

            # Création des rectangles pour le personnage et le PNJ
            personnage_rect = pygame.Rect(position_x, position_y, PERSONNAGE_LARGEUR, PERSONNAGE_HAUTEUR)
            pnj_rect = pygame.Rect(pnj_x, pnj_y, PNJ_LARGEUR, PNJ_HAUTEUR)

            # Afficher le personnage à sa position actuelle
            fenetre.blit(personnage, (position_x, position_y))
            pygame.draw.rect(fenetre, (0, 0, 0), personnage_rect) #Draws a rectangle instead so delete that
            for plateforme in plateformes:
                pygame.draw.rect(fenetre, COLOR, plateforme.rect)
                if PlateformCollision(plateforme.rect, personnage_rect):
                    position_y = plateforme.rect.top - PERSONNAGE_HAUTEUR
                    onGround = True
                    vitesse_y = 0
            for position in plateforme_positions:
                ajouter_plateforme(position[0], position[1])

            # Afficher le PNJ à sa position actuelle
            fenetre.blit(pnj, (pnj_x, pnj_y))

            # Mettre à jour l'affichage
            pygame.display.flip()

            # Limiter la vitesse de rafraîchissement à 60 FPS
            clock.tick(60)

        # Quitter Pygame
        pygame.quit()