import pygame
import math
pygame.init()

win = pygame.display.set_mode((1500 ,700))

pygame.display.set_caption('Worms Eater')

run = True


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

    def movement(self):
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

    def draw(self):
        pygame.draw.rect(win, (255, 0, 0), (self.x, self.y, self.width, self.heigth))



draw = False
t = 0
x = 250
y = 600
timer = 0.1
nug = 1
ch = character(50,50,50,20,5)
while run:
    pygame.time.delay(10)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if pygame.key.get_pressed()[pygame.K_e]:
        draw = True

    speed = -80
    alpha = math.radians(135)
    g = -9.81



    if draw:

        x = (speed * math.cos(alpha) * t) + 250
        y = ((-0.5* g * t**2 + (speed * math.sin(alpha) * t))) + 600
        t += 0.05


    pygame.draw.rect(win, (255, 0, 0), (x, y, 5, 5))
    pygame.display.update()

    if not draw:
        t = 0

    if t >= math.fabs((2*speed*math.sin(alpha))/g):
        draw = False


    ch.movement()
    win.fill((0,0,0))
    ch.draw()



pygame.quit()