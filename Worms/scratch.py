import pygame
import math
import numpy as np
pygame.init()

screenX = 1500
screenY = 700
win = pygame.display.set_mode((screenX,screenY))

pygame.display.set_caption('Worms Eater')

run = True

class projectile():

    def __init__(self, x, y, mouse_pos, speed=100):
        self.x = x
        self.y = y
        self.gravity = -9.81
        self.mouse_pos = mouse_pos
        self.speed = speed
        self.t = 0
        self.firstTime = True
        self.draw()

    def draw(self):

        print("hello")
        alpha = 0

        #Position des point afin de construire l'angle
        a = np.array([self.mouse_pos])
        b = np.array([self.x, self.y])
        c = np.array([screenX, self.y])

        ba = a - b
        bc = c - b

        #Utilisation de lib Numpy afin d'obtenir les vecteur normaux et le produit vectoriel
        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        alpha = np.arccos(cosine_angle)
        self.firstTime = False


        self.x = (-self.speed * math.cos(alpha) * self.t) + 250
        self.y = ((-0.5 * self.gravity * self.t ** 2 + (-self.speed * math.sin(alpha) * self.t))) + 600
        self.t += 0.05
        proj = pygame.draw.rect(win, (255, 0, 0), (self.x, self.y, 5, 5))
        pygame.display.update()


        if self.t >= math.fabs((2 * -self.speed * math.sin(alpha)) / self.gravity):
            self.t = 0
            return True
        else:
            return False








class character():

    def __init__(self,x,y,width,heigth,vel):
        self.x = x
        self.y = y
        self.width = width
        self.heigth = heigth
        self.vel = vel
        self.jumpCount = 10
        self.isJump = False
        self.keys = pygame.key.get_pressed()
        self.Drawable = True
        self.canBeDrawn = False

    def actionTester(self):
        self.keys = pygame.key.get_pressed()

        if self.keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.vel
        if self.keys[pygame.K_RIGHT] and self.x < 500 - self.width:
            self.x += self.vel

        if not self.isJump:
            if self.keys[pygame.K_UP] and self.y > 0:
                self.y -= self.vel
            if self.keys[pygame.K_DOWN] and self.y < 500 - self.heigth:
                self.y += self.vel
            if self.keys[pygame.K_SPACE]:
                self.isJump = True
        else:
            if self.jumpCount >= -10:
                self.neg = 1
                if self.jumpCount < 0:
                    self.neg = -1
                self.y -= (self.jumpCount ** 2) * 0.5 * self.neg
                self.jumpCount -= 1

            else:
                self.isJump = False
                self.jumpCount = 10

        if pygame.mouse.get_pressed()[0] and self.Drawable:
            mousePos = pygame.mouse.get_pos()
            self.proj = projectile(self.x, self.y, mousePos)
            self.Drawable = False
            print("Ye")


        if not self.Drawable:
            self.shoot()

    def draw(self):
        perso = pygame.draw.rect(win, (255, 0, 0), (self.x, self.y, self.width, self.heigth))


    def shoot(self):


       self.Drawable = self.proj.draw()









ch = character(50,50,50,20,5)
while run:
    pygame.time.delay(20)
    pygame.display.update()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False






    ch.actionTester()
    win.fill((0,0,0))
    ch.draw()



pygame.quit()