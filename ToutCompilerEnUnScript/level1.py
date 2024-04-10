import pygame
from pygame.locals import *
from random import randint
import time
import random
import spritesheet


from plateformes import PlateformesRythm


class Jeu:
    def run_game():
        # Constantes
        BLACK = (0, 0, 0)
        LARGEUR = 1920 # Largeur de la fenêtre du jeu
        HAUTEUR = 1080  # Hauteur de la fenêtre du jeu
        GRAVITE = 0.5
        VITESSE_X = 5
        VITESSE_Y = 10
        VITESSE_COURSE = 10  # Vitesse de déplacement en mode course
        PERSONNAGE_LARGEUR = 50  # Largeur du personnage
        PERSONNAGE_HAUTEUR = 50  # Hauteur du personnage
        """ NPC_VITESSE = randint(-5, -3) if randint(0, 1) else randint(3, 5) """
        NPC_VITESSE= randint(-5, -3) if randint(0, 1) else randint(3, 5)
        # crée variable score
        score = 0
        # crée variable de collectibles requis
        Nb_Collectibles = 3


        # Initialisation de Pygame
        pygame.init()

        pygame.display.set_caption('Spritesheets')
        sprite_sheet_image = pygame.image.load("Assets/anim.png").convert_alpha()
        sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)

        # Définir la taille de la fenêtre du jeu
        fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))

        # Charger les images des personnages et du fond
        try:
            fond = pygame.image.load("Assets/obese.jpg").convert()
            lengthFond : list[int] = fond.get_size()

            personnage = pygame.image.load("Assets/perso.png").convert_alpha()
            personnage = pygame.transform.scale(personnage, (PERSONNAGE_LARGEUR, PERSONNAGE_HAUTEUR))

            
            pnj1 = pygame.image.load("Assets/pnj1.png").convert_alpha()
            pnj2 = pygame.image.load("Assets/pnj2.png").convert_alpha()
            pnj3 = pygame.image.load("Assets/pnj3.png").convert_alpha()
            
            # Liste de tous les pnjs
            npc = [pnj1, pnj2, pnj3]

            pnj_choice = randint(0, len(npc) - 1)
            lengthNpc = npc[pnj_choice].get_size()

        except pygame.error as e:
            print("Erreur lors du chargement des images :", str(e))
            pygame.quit()
            exit()

        # Position initiale du personnage
        position_x = 0
        position_y = lengthFond[1] - 501

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
        npc_pos_x = (randint(0, lengthFond[0]))
        npc_pos_y = (lengthFond[1] - 300)

        Jeu.coins_image = pygame.image.load("Assets/coins.png").convert()
        # Liste toutes les colliders des collectibles présent dans le niveau
        Jeu.coins_list = [
            pygame.Rect(500, 750, 23, 23),
            pygame.Rect(800, 750, 23, 23),
            pygame.Rect(1200, 750, 23, 23)
        ]
        # Fonction de mouvement du personnage
        def deplacer_personnage():
            nonlocal position_x, position_y, vitesse_x, vitesse_y, nombre_sauts

            # Appliquer la gravité au personnage
            vitesse_y += GRAVITE

            # Mettre à jour la position du personnage
            position_x += vitesse_x
            position_y += vitesse_y

            # Limiter la position du personnage à l'écran
            position_x = max(0, min(position_x, lengthFond[0] - PERSONNAGE_LARGEUR))
            position_y = max(0, min(position_y, lengthFond[1] - PERSONNAGE_HAUTEUR - 300))

            # Réinitialiser le nombre de sauts si le personnage est au sol
            if position_y >= lengthFond[1] - PERSONNAGE_HAUTEUR - 300:
                nombre_sauts = 0

        # Fonction pour déplacer la caméra
        def deplacer_camera():
            nonlocal camera_x, camera_y

            delta_x = position_x - (camera_x + CAMERA_LARGEUR // 2)
            delta_y = position_y - (camera_y + CAMERA_HAUTEUR // 2)

            if camera_x <= 0 and delta_x < 0:
                delta_x = 0

            if camera_x + LARGEUR >= lengthFond[0] and delta_x > 0:
                delta_x = 0

            if camera_y <= 0 and delta_y < 0:
                delta_y = 0

            if camera_y + HAUTEUR >= lengthFond[1] and delta_y > 0:
                delta_y = 0

            camera_x += delta_x * 0.1
            camera_y += delta_y * 0.1

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

            def move(self):
                self.pos_x += self.velocity

                # Vérifier si le PNJ est hors de l'écran à gauche ou à droite
                if self.pos_x >= LARGEUR and self.velocity > 0:
                    self.pos_x = 0 - self.size[0]
                    self.change_image()
                elif self.pos_x <= 0 - self.size[0] and self.velocity < 0:
                    self.pos_x = LARGEUR
                    self.change_image()

            def change_image(self):
                # Changer l'image du PNJ de manière aléatoire
                self.image_index = random.randint(0, len(self.images) - 1)
                self.image = self.images[self.image_index]

            def draw(self, screen, camera_x, camera_y):
                screen.blit(self.image, (self.pos_x - camera_x, self.pos_y - camera_y))
            
            # Charger les images des personnages et du fond
        try:
            fond = pygame.image.load("Assets/obese.jpg").convert()
            lengthFond = fond.get_size()

            personnage = pygame.image.load("Assets/perso.png").convert_alpha()
            personnage = pygame.transform.scale(personnage, (PERSONNAGE_LARGEUR, PERSONNAGE_HAUTEUR))

            pnj1 = pygame.image.load("Assets/pnj1.png").convert_alpha()
            pnj2 = pygame.image.load("Assets/pnj2.png").convert_alpha()
            pnj3 = pygame.image.load("Assets/pnj3.png").convert_alpha()

            poisson = pygame.image.load("Assets/poiscaille.png").convert_alpha()

            # Liste de tous les pnjs
            npc = [pnj1, pnj2, pnj3]

            pnj_choice = randint(0, len(npc) - 1)
            lengthNpc = npc[pnj_choice].get_size()

        except pygame.error as e:
            print("Erreur lors du chargement des images :", str(e))
            pygame.quit()
            exit()

        import random

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
                self.image_index = random.randint(0, len(self.images) - 1)
                self.image = self.images[self.image_index]

            def draw(self, screen, camera_x, camera_y):
                screen.blit(self.image, (self.pos_x - camera_x, self.pos_y - camera_y))

            def destroy(self):
                # Code pour détruire le NPC
                self.pos_x = -1000  # Déplacer le NPC hors de l'écran
                self.pos_y = -1000
                self.velocity = 0  # Arrêter le mouvementµ

        class Jeu:
            def __init__(self):
                self.plateformes_image = pygame.image.load("Assets/Plateformes.png").convert()
                self.plateformes_image = pygame.transform.scale(self.plateformes_image, (50, 50))

                self.plateformes_list = [PlateformesRythm(100, 600, self.plateformes_image),
                                        PlateformesRythm(300, 600, self.plateformes_image),
                                        PlateformesRythm(600, 600, self.plateformes_image),
                                        PlateformesRythm(800, 600, self.plateformes_image),
                                        PlateformesRythm(1000, 600, self.plateformes_image)
                                        ]
                
            def Afficher_Plateformes_paires(self):
                for i in range(0, len(self.plateformes_list)):
                    if i % 2 == 0:
                        self.ecran.blit(self.plateformes_list[i].image,
                                        (self.plateformes_list[i].x, self.plateformes_list[i].y))
                    else:
                        self.ecran.blit(self.plateformes_list[i].image,
                                        (self.plateformes_list[i].x, self.plateformes_list[i].y + 1000))

            def Afficher_Plateformes_Impaires(self):
                for j in range(0, len(self.plateformes_list)):
                    if j % 2 == 0:
                        self.ecran.blit(self.plateformes_list[j].image,
                                        (self.plateformes_list[j].x, self.plateformes_list[j].y + 1000))
                    else:
                        self.ecran.blit(self.plateformes_list[j].image,
                                        (self.plateformes_list[j].x, self.plateformes_list[j].y))



        # Créer une instance de la classe NPC
        npc_images = [pnj1, pnj2, pnj3]
        npc = NPC(npc_images, randint(0, lengthFond[0]), lengthFond[1] - 700, NPC_VITESSE)


        class NPCManager:
            def __init__(self, spawn_interval, fish_spawn_interval):
                self.spawn_interval = spawn_interval  # Intervalle de spawn en secondes pour les PNJs
                self.fish_spawn_interval = fish_spawn_interval  # Intervalle de spawn en secondes pour les poissons
                self.last_spawn_time = time.time()  # Temps du dernier spawn de PNJ
                self.last_fish_spawn_time = time.time()  # Temps du dernier spawn de poisson
                self.npcs = []  # Liste des PNJs
                self.fish_list = []  # Liste des poissons
                self.is_fish_spawned = False  # Indique si un poisson est déjà apparu

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

                # Vérifier si le temps écoulé depuis le dernier spawn de poisson est supérieur à l'intervalle
                if current_time - self.last_fish_spawn_time >= self.fish_spawn_interval:
                    # Spawn d'un nouveau poisson
                    self.spawn_fish()
                    # Mettre à jour le temps du dernier spawn de poisson
                    self.last_fish_spawn_time = current_time

            def spawn_npc(self):
                # Coordonnées initiales aléatoires dans les limites de l'écran
                initial_x = LARGEUR + lengthNpc[0] - camera_x  # Utiliser lengthNpc pour obtenir la taille du PNJ
                spawn_y = 500
                velocity = 5  # Vitesse constante pour cet exemple
                return NPC(npc_images, initial_x, spawn_y, velocity)

            
            def is_npc_near_player(self, player_x, player_y):
                for npc in self.npcs:
                    if abs(player_x - npc.pos_x) < 200 and abs(player_y - npc.pos_y) < 200:
                        return True
                return False

            def spawn_fish(self):
                global position_x, position_y

                # Vérifier si aucun poisson n'est actuellement apparu et s'il y a des PNJs
                if not self.is_fish_spawned and self.npcs:
                    # Vérifier si un PNJ est à proximité du joueur
                    if self.is_npc_near_player(position_x, position_y):
                        # Ajouter le poisson à la liste des poissons
                        self.fish_list.append((position_x, position_y))
                        # Indiquer qu'un poisson est apparu
                        self.is_fish_spawned = True

            def update_fish(self):
                for i, fish in enumerate(self.fish_list):
                    x, y = fish
                    # Vérifier si le poisson n'a pas atteint le sol
                    if y < lengthFond[1] - 500:  # Modifier cette valeur selon votre besoin
                        y += 5
                    self.fish_list[i] = (x, y)

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


        spawn_interval = 3  # Intervalle de spawn en secondes pour les PNJs
        fish_spawn_interval = 5  # Intervalle de spawn en secondes pour les poissons
        npc_manager = NPCManager(spawn_interval, fish_spawn_interval)

        Timer = 0
        Loop = 1
        pygame.time.set_timer(USEREVENT, 1000)
        # Charge la police d'écriture installé
        font = pygame.font.Font("Assets/Parisish.ttf", 50)
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
            #update anim
            currentTime = pygame.time.get_ticks()
            if currentTime - lastUpdate >= animCD:
                frame += 1
                lastUpdate = currentTime
                if frame >= len(animList[action]):
                    frame = 0

            # print les img
            fenetre.blit(animList[action][frame], (0, 0))

            # Créé le collider du player après chaque déplacement
            player_collider = pygame.Rect(Jeu.player.x, Jeu.player.y, Jeu.player.width, Jeu.player.height)

            # Vérifie si il y a collision avec un collectible et le joueur et actualise le score si vrai
            for c in Jeu.coins_list:
                if c.colliderect(player_collider):
                    Jeu.coins_list.remove(c)
                    score += 1

            Jeu.ecran.blit(Jeu.background, (0, 0))

            # Affiche les collectibles
            for c in Jeu.coins_list:
                Jeu.ecran.blit(Jeu.coins_image, (c[0], c[1]))

            # Déplacer le personnage
            deplacer_personnage()

            # Déplacer la caméra
            deplacer_camera()

            # Déplacer les PNJs
            npc.move()

            fenetre.fill((0,0,0))

            # Afficher le fond à l'arrière-plan
            fenetre.blit(fond, (0 - camera_x, 0 - camera_y))

            # Afficher le personnage à sa position actuelle (par rapport à la caméra)
            fenetre.blit(personnage, (position_x - camera_x, position_y - camera_y))

            if Loop % 2 == 0:
                Jeu.Afficher_Plateformes_paires()
            else:
                Jeu.Afficher_Plateformes_Impaires()

            # Afficher les PNJs
            for npc in npc_manager.npcs:
                npc.draw(fenetre, camera_x, camera_y)

            # Mettre à jour et afficher les poissons
            npc_manager.update_fish()
            for fish_pos in npc_manager.fish_list:
                fenetre.blit(poisson, (fish_pos[0] - camera_x, fish_pos[1] - camera_y))   

            # Affiche le score actuel sur l'écran
            Jeu.ecran.blit(font.render(str(score) + "/" + str(Nb_Collectibles), 1, (0, 0, 0)), (5, 5))

            # Mettre à jour l'affichage
            pygame.display.flip()

            pygame.display.update()

            # Limiter la vitesse de rafraîchissement à 60 FPS
            clock.tick(60)

        # Quitter Pygame après la sortie de la boucle principale
        pygame.quit()