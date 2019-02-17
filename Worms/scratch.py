import pygame
import math
import random
import numpy as np
pygame.init()

screen_x = 1500
screen_y = 700
window = pygame.display.set_mode((screen_x,screen_y))
pygame.display.set_caption('Worms Eater')

run = True

global items_to_update
global players
global wind

def random_wind_interval():
    return (random.uniform(-1, 1), random.uniform(-1, 1))

class Projectile():

    def __init__(self, x, y, mouse_pos, speed=150, mass=10):
        self.x = x
        self.y = y - 1
        self.init_x = x
        self.init_y = y - 1
        self.gravity = -9.81
        self.mouse_pos = mouse_pos
        self.speed = speed
        self.mass = mass
        self.t = 0
        self.first_time = True
        self.alpha = math.radians(0)
        self.draw()


    def draw(self):
        pygame.draw.rect(window,(0,255,0),(screen_x, self.y, 5 ,5))
        if self.first_time:
            #Position des point afin de construire l'angle
            a = np.array([self.mouse_pos[0], self.mouse_pos[1]])
            b = np.array([self.init_x, self.init_y])
            c = np.array([screen_x, self.y])
            ba = a - b
            bc = c - b
            #Utilisation de lib Numpy afin d'obtenir les vecteur normaux et le produit vectoriel
            cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
            self.alpha =  math.fabs(np.arccos(cosine_angle) - math.pi)
            self.first_time = False
        self.x = (-self.speed * math.cos(self.alpha) * self.t) + self.init_x
        self.y = ((-0.5 * self.gravity * self.t ** 2 + (-self.speed * math.sin(self.alpha) * self.t))) + self.init_y
        self.t += 0.05
        proj = pygame.draw.rect(window, (0, 0, 255), (self.x, self.y, 5, 5))
        items_to_update.append(proj)
        if self.t >= math.fabs((2 * -self.speed * math.sin(self.alpha)) / self.gravity):
            self.t = 0
            self.first_time = True
            return True
        else:
            return False

class Grenade(Projectile):

    def __init__(self, x, y, mouse_pos):
        self.wind = wind
        Projectile.__init__(self, x, y, mouse_pos)


    def draw(self):
        pygame.draw.rect(window,(0,255,0),(screen_x, self.y, 5 ,5))
        if self.first_time:
            #Position des point afin de construire l'angle
            a = np.array([self.mouse_pos[0], self.mouse_pos[1]])
            b = np.array([self.init_x, self.init_y])
            c = np.array([screen_x, self.y])
            ba = a - b
            bc = c - b
            #Utilisation de lib Numpy afin d'obtenir les vecteur normaux et le produit vectoriel
            cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
            self.alpha =  math.fabs(np.arccos(cosine_angle) - math.pi)
            self.first_time = False
        self.x = (1 / self.mass * 2) * self.wind[0] * self.t ** 2 + -self.speed * math.cos(self.alpha) * self.t + self.init_x
        self.y = (-0.5 * self.gravity + (1 / self.mass) * self.wind[1]) * self.t ** 2 + -self.speed * math.sin(self.alpha) * self.t + self.init_y
        self.t += 0.05
        proj = pygame.draw.rect(window, (0, 0, 255), (self.x, self.y, 5, 5))
        items_to_update.append(proj)
        if self.t >= math.fabs((2 * -self.speed * math.sin(self.alpha)) / self.gravity) + 1:
            self.t = 0
            self.first_time = True
            return True
        else:
            return False


class Character():

    def __init__(self, x, y, width, height, vel, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.jump_count = 10
        self.is_jump = False
        self.keys = pygame.key.get_pressed()
        self.drawable = True
        self.can_be_drawn = True
        self.color = color
        self.sprite = pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))


    def action(self):
        self.keys = pygame.key.get_pressed()

        if self.keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.vel
        if self.keys[pygame.K_RIGHT] and self.x < screen_x - self.width:
            self.x += self.vel
        if not self.is_jump:
            if self.keys[pygame.K_SPACE]:
                self.is_jump = True
        if pygame.mouse.get_pressed()[0] and self.drawable:
            mouse_pos = pygame.mouse.get_pos()
            self.proj = Projectile(self.x, self.y, mouse_pos)
            self.drawable = False
        if pygame.mouse.get_pressed()[1] and self.drawable:
            mouse_pos = pygame.mouse.get_pos()
            self.proj = Grenade(self.x, self.y, mouse_pos)
            self.drawable = False

    def logic(self):
        if self.is_jump:
            if self.jump_count >= -10:
                self.neg = 1
                if self.jump_count < 0:
                    self.neg = -1
                self.y -= (self.jump_count ** 2) * 0.5 * self.neg
                self.jump_count -= 1
            else:
                self.is_jump = False
                self.jump_count = 10
        if not self.drawable:
            self.shoot()
        try:
            for player in players:
                if pygame.Rect.collidepoint(player.sprite, self.proj.x, self.proj.y):
                    player.die()
        except AttributeError:
            pass
        

    def draw(self):
        if self.can_be_drawn:
            self.sprite = pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))
            items_to_update.append(self.sprite)


    def shoot(self):
       self.drawable = self.proj.draw()


    def die(self):
        self.can_be_drawn = False


items_to_update = []
players = [
    Character(50, 500, 50, 20, 5, (255, 0, 0)),
    Character(1200, 500, 50, 20, 5, (0, 0, 255))
]
player_index = 0
wind = random_wind_interval()
current_player = players[player_index]
next_turn_ticks = pygame.time.get_ticks()

while run:
    pygame.time.delay(20)

    # Events block
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    # If the opponent or the two players are dead, stop the game
    if len(players) <= 1:
        run = False
    current_player.action()
    #
    
    # Logic block
    if (pygame.time.get_ticks() - next_turn_ticks) / 1000 > 10:
        player_index = (player_index + 1) % len(players)
        current_player = players[player_index]
        wind = random_wind_interval()
        next_turn_ticks = pygame.time.get_ticks()
    
    for index, player in enumerate(players):
        if not player.can_be_drawn:
            players.pop(index)
        player.logic()
    if len(items_to_update) > 0:
        pygame.display.update(items_to_update)
        items_to_update = []
    #

    # Draw block
    for player in players:
        player.draw()
    pygame.display.flip()
    window.fill((0,0,0))
    #

pygame.quit()