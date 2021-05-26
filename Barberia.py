import pygame
from pygame.locals import *
from Tienda_barbero import *

NEGRO = (0, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
pygame.init()
window = pygame.display.set_mode((1200, 700))


class Sofa(pygame.sprite.Sprite):

    def __init__(self, imageName):
        super().__init__()

        self.image = pygame.image.load(imageName).convert()
        color = self.image.get_at((0, 0))
        self.image.set_colorkey(color, RLEACCEL)
        self.rect = self.image.get_rect()
        self.rect.center = (620, 620)


class Caja(pygame.sprite.Sprite):

    def __init__(self, imageName):
        super().__init__()

        self.image = pygame.image.load(imageName).convert()
        color = self.image.get_at((0, 0))
        self.image.set_colorkey(color, RLEACCEL)
        self.rect = self.image.get_rect()
        self.rect.center = (1050, 370)


class Silla(pygame.sprite.Sprite):

    def __init__(self, imageName, x, y):
        super().__init__()

        self.image = pygame.image.load(imageName).convert()
        color = self.image.get_at((0, 0))
        self.image.set_colorkey(color, RLEACCEL)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


sillas = pygame.sprite.Group()
sofas = pygame.sprite.Group()
cajas = pygame.sprite.Group()

run = True
x = 30
y = 40
clientes = [Cliente() for _ in range(14)]
barbero = [Barbero(i) for i in range(3)]
cajero = Cajero()

for c in clientes:
    c.start()

for b in barbero:
    b.start()

cajero.start()
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    sofa = Sofa("Sofa2.png")
    caja = Caja("caja.png")
    silla1 = Silla("silla.png", 400, 240)
    silla2 = Silla("silla.png", 600, 240)
    silla3 = Silla("silla.png", 800, 240)

    window.fill((96, 96, 64))
    sofas.add(sofa)
    sofas.draw(window)
    cajas.add(caja)
    cajas.draw(window)
    sillas.add(silla1)
    sillas.add(silla2)
    sillas.add(silla3)
    sillas.draw(window)
    pygame.draw.line(window, VERDE, (0, 10), (50, 10), 10)
    pygame.draw.line(window, VERDE, (0, 110), (50, 110), 10)
    pygame.draw.line(window, VERDE, (1150, 590), (1200, 590), 10)
    pygame.draw.line(window, VERDE, (1150, 690), (1200, 690), 10)
    for c in clientes:
        c.pintarCirculo(window, 30)
    pintarCirculoB1(window, 30)
    pintarCirculoB2(window, 30)
    pintarCirculoB3(window, 30)
    pygame.display.flip()

pygame.quit()
exit()