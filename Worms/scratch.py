import pygame
from pygame import time
from pygame.locals import *

pygame.init()
pygame.key.set_repeat(2,40)

movingLeft = False
movingRight = False

walkCount = 0

walkRight = [pygame.image.load('tile000.png'),
             pygame.image.load('tile001.png'),
             pygame.image.load('tile002.png'),
             pygame.image.load('tile003.png'),
             pygame.image.load('tile004.png'),
             pygame.image.load('tile005.png'),
             pygame.image.load('tile006.png'),
             pygame.image.load('tile007.png'),
             pygame.image.load('tile008.png')]

walkLeft = [pygame.image.load('tile000-Reversed.png'),
            pygame.image.load('tile001-Reversed.png'),
            pygame.image.load('tile002-Reversed.png'),
            pygame.image.load('tile003-Reversed.png'),
            pygame.image.load('tile004-Reversed.png'),
            pygame.image.load('tile005-Reversed.png'),
            pygame.image.load('tile006-Reversed.png'),
            pygame.image.load('tile007-Reversed.png'),
            pygame.image.load('tile008-Reversed.png')]

width = 80
height = 80

# Ouverture de la fenêtre Pygame
fenetre = pygame.display.set_mode((626, 352))

# Chargement et collage du fond
fond_ciel = pygame.image.load("ciel.jpg").convert()

fond_grass = pygame.image.load("background.jpg").convert()
position_floor = fond_grass.get_rect(x=0,y=300)

# Chargement et collage du personnage
perso = pygame.image.load("tile000.png").convert_alpha()
position_perso = perso.get_rect(x=0,y=0)
fenetre.blit(perso, position_perso)

# Rafraîchissement de l'écran
pygame.display.flip()
clock = time.Clock()

class Projectile(object):

    def __init__(self,x,y,radius,color,facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self):
        pygame.draw.circle(fenetre, self.color, (self.x,self.y), self.radius, 1)


def displayer():
    global walkCount
    fenetre.blit(fond_ciel, (0, 0))
    fenetre.blit(fond_grass, (0, 300))
    if walkCount + 1 > 27:
        walkCount = 0
    if movingLeft:
        fenetre.blit(walkLeft[walkCount//3], position_perso)
        walkCount += 1
    elif movingRight:
        fenetre.blit(walkRight[walkCount//3], position_perso)
        walkCount += 1
    else:
        fenetre.blit(perso, position_perso)
    pygame.display.flip()

# BOUCLE INFINIE
continuer = 1
while continuer:
    dt = clock.tick(60)
    for event in pygame.event.get():  # Attente des événements
        if event.type == QUIT:
            continuer = 0
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                movingLeft = False
                movingRight = True
                position_perso = position_perso.move(5, 0)
            elif event.key == K_LEFT:
                movingLeft = True
                movingRight = False
                position_perso = position_perso.move(-5, 0)
            elif event.key == K_e:
                for i in range(100):
                    pygame.draw.circle(fenetre,(0,0,0), (i,i), 2, 0)
                pass
            else:
                movingLeft = False
                movingRight = False
        else:
            movingLeft = False
            movingRight = False
            walkCount = 0

    if position_perso.colliderect(position_floor) != 1:
        position_perso = position_perso.move(0, 0.7 * dt)
    if position_perso.y > 240:
        print(position_perso.y)
        position_perso = position_perso.move(0,-50)
    position_perso = pygame.Rect(position_perso.x,position_perso.y, 75,75)
    # Re-collage
    displayer()
    # Rafraichissement

