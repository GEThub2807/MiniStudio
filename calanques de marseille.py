import pygame
from random import*

pygame.init()

#Définir la taille de la fenêtre du jeu
largeur = 586
hauteur = 360
fenetre = pygame.display.set_mode((largeur, hauteur))

background = pygame.image.load('Assets/background.jpg')
  
  

#Boucle principale du jeu
running = True
while running:
  fenetre.blit(background, (0, 0))

  for event in pygame.event.get() :
    if event.type == pygame.QUIT:  
      running = False
      pygame.quit()
      print("fermeture du jeu")

  # Mettre à jour l'affichage
  pygame.draw.rect(fenetre, (0, 0, 255), pygame.Rect(30, 30, 60, 60))
  pygame.display.flip()

#Quitter Pygame
pygame.quit()