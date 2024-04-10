import pygame
from pygame.locals import *
from random import randint
import time
from random import*
import spritesheet
from plateformes import PlateformesRythm


class Jeu:
    @staticmethod

    def run_game():
        #------------------------------------------------------------Constantes début, tout le monde-----------------------------------------------------------------
        BLACK = (0, 0, 0)
        LARGEUR = 1920 # Largeur de la fenêtre du jeu
        HAUTEUR = 1080  # Hauteur de la fenêtre du jeu
        GRAVITE = 0.5
        VITESSE_X = 5
        VITESSE_Y = 10
        VITESSE_COURSE = 10  # Vitesse de déplacement en mode course
        PERSONNAGE_LARGEUR = 50  # Largeur du personnage
        PERSONNAGE_HAUTEUR = 50  # Hauteur du personnage
        SPAWN_INTERVAL = 3  # Intervalle de spawn en secondes pour les PNJs

        """ NPC_VITESSE = randint(-5, -3) if randint(0, 1) else randint(3, 5) """
        NPC_VITESSE = -5
        #------------------------------------------------------------Constante fin-----------------------------------------------------------------------------

        # crée variable score
        score = 0
        # crée variable de collectibles requis
        Nb_Collectibles = 3

        # Initialisation de Pygame
        pygame.init()

        #-----------------------------------------------------------animation importation, Elouan-----------------------------------------------------------------
        pygame.display.set_caption('Spritesheets')
        Sprite_Sheet_Image = pygame.image.load("Assets/anim.png").convert_alpha()
        Sprite_Sheet = spritesheet.SpriteSheet(Sprite_Sheet_Image)
        #-----------------------------------------------------------animation-------------------------------------------------------------------------

        # Définir la taille de la fenêtre du jeu
        fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))

        #--------------------------------------------------Chargement des images des personnages et du fond, début, Antoine------------------------------------------
        try:
            fond = pygame.image.load("Assets/obese.jpg").convert()
            Length_Fond : list[int] = fond.get_size()

            personnage = pygame.image.load("Assets/perso.png").convert_alpha()
            personnage = pygame.transform.scale(personnage, (PERSONNAGE_LARGEUR, PERSONNAGE_HAUTEUR))

            
            pnj1 = pygame.image.load("Assets/pnj1.png").convert_alpha()
            pnj2 = pygame.image.load("Assets/pnj2.png").convert_alpha()
            pnj3 = pygame.image.load("Assets/pnj3.png").convert_alpha()
            
            # Liste de tous les pnjs
            npc = [pnj1, pnj2, pnj3]

            Pnj_Choice = randint(0, len(npc) - 1)
            Length_Npc = npc[Pnj_Choice].get_size()

        except pygame.error as e:
            print("Erreur lors du chargement des images :", str(e))
            pygame.quit()
            exit()
        #--------------------------------------------------Chargement des images des personnages et du fond fin------------------------------------------
            
        # Charger les images des personnages et du fond
        try:
            fond = pygame.image.load("Assets/obese.jpg").convert()
            Length_Fond = fond.get_size()

            personnage = pygame.image.load("Assets/perso.png").convert_alpha()
            personnage = pygame.transform.scale(personnage, (PERSONNAGE_LARGEUR, PERSONNAGE_HAUTEUR))

            pnj1 = pygame.image.load("Assets/pnj1.png").convert_alpha()
            pnj2 = pygame.image.load("Assets/pnj2.png").convert_alpha()
            pnj3 = pygame.image.load("Assets/pnj3.png").convert_alpha()

            poisson = pygame.image.load("Assets/poiscaille.png").convert_alpha()

            # Liste de tous les pnjs
            npc = [pnj1, pnj2, pnj3]

            Pnj_Choice = randint(0, len(npc) - 1)
            Length_Npc = npc[Pnj_Choice].get_size()

        except pygame.error as e:
            print("Erreur lors du chargement des images :", str(e))
            pygame.quit()
            exit()

        #----------------------------------------------------Initialisation variables persos et cam, début, Valentin-------------------------------------
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
        #----------------------------------------------------Initialisation variables persos et cam, Fin-------------------------------------
        #------------------------------------------------------Initialisation des collectibles,début, Timothé------------------------------------------
        Jeu.coins_image = pygame.image.load("Assets/coins.png").convert()
        # Liste toutes les colliders des collectibles présent dans le niveau
        Jeu.coins_list = [
            pygame.Rect(500, 750, 23, 23),
            pygame.Rect(800, 750, 23, 23),
            pygame.Rect(1200, 750, 23, 23)
        ]
        #------------------------------------------------------Initialisation des collectibles,Fin, Timothé------------------------------------------
        #--------------------------------------------------------Système basiques du jeu, Début, Valentin, Antoine-------------------------------------
        # Fonction de mouvement du personnage
        def Deplacer_Personnage():
            nonlocal position_x, position_y, vitesse_x, vitesse_y, nombre_sauts

            # Appliquer la gravité au personnage
            vitesse_y += GRAVITE

            # Mettre à jour la position du personnage
            position_x += vitesse_x
            position_y += vitesse_y

            # Limiter la position du personnage à l'écran
            position_x = max(0, min(position_x, Length_Fond[0] - PERSONNAGE_LARGEUR))
            position_y = max(0, min(position_y, Length_Fond[1] - PERSONNAGE_HAUTEUR - 300))

            # Réinitialiser le nombre de sauts si le personnage est au sol
            if position_y >= Length_Fond[1] - PERSONNAGE_HAUTEUR - 500:
                nombre_sauts = 0

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
        #--------------------------------------------------------Système basiques du jeu, Fin, Valentin, Antoine-------------------------------------
        #-----------------------------------------------------------Systèmes des NPC, Début, Antoine---------------------------------------------
        # Fonction pour déplacer les PNJs
        class NPC:
            def __init__(self, images, initial_x, spawn_y, velocity):
                self.images = images
                self.image_index = 0
                self.image = images[self.image_index]
                self.pos_x = initial_x
                self.spawn_y = spawn_y
                self.pos_y = spawn_y
                self.velocity = velocity
                self.size = self.image.get_size()

                self.change_image()

            def move(self):
                self.pos_x -= self.velocity

                # Vérifier si le PNJ est hors de l'écran à gauche ou à droite
                if self.pos_x <= 0 - self.size[0] and self.velocity < 0:
                    self.destroy()

            def change_image(self):
                # Changer l'image du PNJ de manière aléatoire
                self.image_index = randint(0, len(self.images) - 1)
                self.image = self.images[self.image_index]

            def draw(self, screen, camera_x, camera_y):
                screen.blit(self.image, (self.pos_x - camera_x, self.pos_y - camera_y))

            def destroy(self):
                # Code pour détruire le NPC
                self.pos_x = -1000  # Déplacer le NPC hors de l'écran
                self.pos_y = -1000
                self.velocity = 0  # Arrêter le mouvement


        # Créer une instance de la classe NPC
        npc_images = [pnj1, pnj2, pnj3]
        npc = NPC(npc_images, randint(0, Length_Fond[0]), Length_Fond[1] - 700, NPC_VITESSE)

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
                    if npc:
                        self.npcs.append(npc)
                    # Mettre à jour le temps du dernier spawn de PNJ
                    self.last_spawn_time = current_time

            def spawn_npc(self):
                # Coordonnées initiales aléatoires dans les limites de l'écran
                initial_x = LARGEUR + Length_Fond[0] - camera_x  # Utiliser lengthNpc pour obtenir la taille du PNJ
                spawn_y = Length_Fond[1] - 500
                velocity = 5  
                return NPC(npc_images, initial_x, spawn_y, velocity)

        spawn_interval = 3  # Intervalle de spawn en secondes pour les PNJs
        npc_manager = NPCManager(spawn_interval)
        #-----------------------------------------------------------Systèmes des NPC, Fin, Antoine---------------------------------------------

        #-----------------------------------------------------------Systèmes des plateformes, Début, Timothé---------------------------------------------
        class Plateformes:
            def __init__(self):
                self.plateformes_image = pygame.image.load("Assets/Plateformes.png").convert()
                self.plateformes_image = pygame.transform.scale(self.plateformes_image, (50, 50))

                self.plateformes_list = [PlateformesRythm(100, 600, self.plateformes_image),
                                        PlateformesRythm(300, 600, self.plateformes_image),
                                        PlateformesRythm(600, 600, self.plateformes_image),
                                        PlateformesRythm(800, 600, self.plateformes_image),
                                        PlateformesRythm(1000, 600, self.plateformes_image)
                                        ]
                
            def Afficher_Plateformes_Paires(self):
                for i in range(0, len(self.plateformes_list)):
                    if i % 2 == 0:
                        fenetre.blit(self.plateformes_list[i].image,
                                        (self.plateformes_list[i].x, self.plateformes_list[i].y))
                    else:
                        fenetre.blit(self.plateformes_list[i].image,
                                        (self.plateformes_list[i].x, self.plateformes_list[i].y + 1000))

            def Afficher_Plateformes_Impaires(self):
                for j in range(0, len(self.plateformes_list)):
                    if j % 2 == 0:
                        fenetre.blit(self.plateformes_list[j].image,
                                        (self.plateformes_list[j].x, self.plateformes_list[j].y + 1000))
                    else:
                        fenetre.blit(self.plateformes_list[j].image,
                                        (self.plateformes_list[j].x, self.plateformes_list[j].y))
            
        plateformes_instance = Plateformes()


        #-----------------------------------------------------------Systèmes des plateformes, Début, Timothé---------------------------------------------
        #-----------------------------------------------------------Initialisation des animations, début, Elouan------------------------------------
        Anim_List = [] #crée le tableau avec les sprites pour l'anim
        Anim_Steps = [4, 6, 3 , 4] #définit le nombre de sprites qui seront affichées
        action = 0
        Last_Update = pygame.time.get_ticks()
        Anim_CD = 500 #définit le temps de la boucle d'animation
        frame = 0
        Step_Count = 0

        for animation in Anim_Steps:
            Temp_Img_List = []
            for _ in range(animation):
                Temp_Img_List.append(Sprite_Sheet.get_image(Step_Count, 24, 24, 3, BLACK))
                Step_Count += 1
            Anim_List.append(Temp_Img_List)
        #-----------------------------------------------------------Initialisation des animations, Elouan------------------------------------
        #-----------------------------------------------------------Déclaration de variables et autres, début-------------------------------------------------
        Timer = 0
        Loop = 1
        pygame.time.set_timer(USEREVENT, 1000)
        # Charge la police d'écriture installé
        font = pygame.font.Font("Assets/Parisish.ttf", 50)
        #-----------------------------------------------------------Déclaration de variables et autres, fin-------------------------------------------------
        #-----------------------------------------------------------Boucle de jeu du level, début, tout le monde--------------------------------------------------------
        # Boucle principale du jeu
        running = True
        clock = pygame.time.Clock()
        while running:
            # Gestion des événements
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
                    elif event.key == K_LSHIFT or event.key == K_RSHIFT:
                        if not is_running:
                            VITESSE_X = VITESSE_COURSE
                            is_running = True  # La touche Shift est enfoncée
                    elif event.key == K_ESCAPE:
                        running = False
                elif event.type == KEYUP:
                    if event.key == K_LEFT and vitesse_x < 0:
                        vitesse_x = 0
                    elif event.key == K_RIGHT and vitesse_x > 0:
                        vitesse_x = 0
                    elif event.key == K_LSHIFT or event.key == K_RSHIFT:
                        if is_running:
                            VITESSE_X = 5
                            is_running = False  # La touche Shift est relâchée
                elif event.type == USEREVENT:
                    Timer += 1

                    if Timer == 3:
                        Loop += 1
                        Timer = 0


            # Mettre à jour le gestionnaire de PNJs pour gérer les spawns
            npc_manager.update()

            # Mettre à jour les positions et les actions des PNJs existants
            for npc in npc_manager.npcs:
                npc.move()

            #update anim
            Current_Time = pygame.time.get_ticks()
            if Current_Time - Last_Update >= Anim_CD:
                frame += 1
                Last_Update = Current_Time
                if frame >= len(Anim_List[action]):
                    frame = 0

            # print les img
            fenetre.blit(Anim_List[action][frame], (0, 0))

            # Créé le collider du personnage après chaque déplacement
            personnage_Collider = pygame.Rect(position_x, position_y, PERSONNAGE_LARGEUR, PERSONNAGE_HAUTEUR)


            # Vérifie si il y a collision avec un collectible et le joueur et actualise le score si vrai
            for c in Jeu.coins_list:
                if c.colliderect(personnage_Collider):
                    Jeu.coins_list.remove(c)
                    score += 1

            fenetre.blit(fond, (0, 0))


            # Affiche les collectibles
            for c in Jeu.coins_list:
                fenetre.blit(Jeu.coins_image, (c[0], c[1]))

            # Déplacer le personnage
            Deplacer_Personnage()

            # Déplacer la caméra
            Deplacer_Camera()

            # Déplacer les PNJs
            npc.move()

            fenetre.fill((0,0,0))

            # Afficher le fond à l'arrière-plan
            fenetre.blit(fond, (0 - camera_x, 0 - camera_y))

            # Afficher le personnage à sa position actuelle (par rapport à la caméra)
            fenetre.blit(personnage, (position_x - camera_x, position_y - camera_y))

            if Loop % 2 == 0:
                plateformes_instance.Afficher_Plateformes_Paires()

            else:
                plateformes_instance.Afficher_Plateformes_Impaires()


            # Afficher les PNJs
            for npc in npc_manager.npcs:
                npc.draw(fenetre, camera_x, camera_y) 

            # Affiche le score actuel sur l'écran
            fenetre.blit(font.render(str(score) + "/" + str(Nb_Collectibles), 1, (0, 0, 0)), (5, 5))

            # Mettre à jour l'affichage
            pygame.display.flip()

            pygame.display.update()

            # Limiter la vitesse de rafraîchissement à 60 FPS
            clock.tick(60)
        #-----------------------------------------------------------Boucle de jeu du level, début, tout le monde--------------------------------------------------------

        # Quitter Pygame après la sortie de la boucle principale
        pygame.quit()