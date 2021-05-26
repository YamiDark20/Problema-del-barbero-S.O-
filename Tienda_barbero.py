import threading
import time
import pygame
from pygame.locals import *
#import copy

max_cap = threading.Semaphore(10)
sofa = threading.Semaphore(4)
silla_barbero = threading.Semaphore(3)
coord = threading.Semaphore(3)
mutex1 = threading.Semaphore(1)
mutex2 = threading.Semaphore(1)
cliente_listo = threading.Semaphore(0)
dejar_silla_b = [threading.Semaphore(0) for i in range(3)]
pago = threading.Semaphore(0)
recibo = threading.Semaphore(0)
terminado = [threading.Semaphore(0) for i in range(14)]
count = 0  # Se usa para asignar indicadores de los clientes
colaCorte = []  # Se usa para poder saber a cual cliente fue el
#que el barbero le corto el pelo. Se usa en el semaforo terminado
realiza_pago = threading.Semaphore(1)
mutex3 = threading.Semaphore(1)

bAtendiendo = None  # Se usa para almacenar el index del barbero
#que atiende al cliente

NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
espacioVacio = {1: None, 2: None, 3: None, 4: None, 5: None, 6: None}
s_sofa = {1: None, 2: None, 3: None, 4: None}  # Sentarse en sofa
s_silla = {1: None, 2: None, 3: None}  # Sentarse en silla
e_pagar = [None, None, None, None, None, None, None, None]
pos = [[400, 130], [600, 130], [800, 130]]
coordinar = []  # Se usa para saber cual barbero esta activo
#para atender la caja


class Cliente(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.numcliente = 0
        self.x = -100
        self.y = -100

    def run(self):
        global count, bAtendiendo
        max_cap.acquire()
        time.sleep(3)
        mutex1.acquire()
        self.numcliente = count
        #Entrando a la tienda
        self.entrando()

        count += 1
        mutex1.release()
        sofa.acquire()
        #Sentandose en el sofa
        self.sentarse_sofa()
        time.sleep(3)
        silla_barbero.acquire()

        #Levantandose del sofa
        time.sleep(4)
        sofa.release()

        #Sentandose en la silla
        self.sentarse_silla()
        mutex2.acquire()
        if(self.numcliente < 2):
            time.sleep(1)
        colaCorte.append(self.numcliente)
        cliente_listo.release()
        mutex2.release()
        terminado[self.numcliente].acquire()

        valorS = bAtendiendo
        ##La siguiente linea es parte de lo que nos pide en la b)
        dejar_silla_b[valorS].release()
        self.espera_a_pagar()

        realiza_pago.acquire()
        self.pagarCuenta()
        pago.release()
        recibo.acquire()
        #Saliendo de la tienda
        self.salirTienda()
        max_cap.release()

    def pintarCirculo(self, window, dimensiones):
        pygame.draw.circle(window, NEGRO, (self.x, self.y), 20)
        tipo_letra = pygame.font.Font(pygame.font.match_font('times'),
        dimensiones)
        superficie = tipo_letra.render("C" + str(self.numcliente), True, AZUL)
        rectangulo = superficie.get_rect()
        rectangulo.center = (self.x, self.y)
        window.blit(superficie, rectangulo)

    def entrando(self):
        t = 0.05
        if(espacioVacio[1] is None):
            self.x = 30
            self.y = 40
            espacioVacio[1] = self.numcliente
            time.sleep(t)
            while(self.x != 60):
                if(self.x + 10 <= 60):
                    self.x += 10
                    time.sleep(t)
            while(self.y != 530):
                if(self.y + 10 <= 530):
                    self.y += 10
                    time.sleep(t)
            while(self.x != 450):
                if(self.x + 10 <= 450):
                    self.x += 10
                    time.sleep(t)

        elif(espacioVacio[2] is None):
            self.x = 30
            self.y = 40
            espacioVacio[2] = self.numcliente
            time.sleep(t)
            while(self.x != 60):
                if(self.x + 10 <= 60):
                    self.x += 10
                    time.sleep(t)
            while(self.y != 530):
                if(self.y + 10 <= 530):
                    self.y += 10
                    time.sleep(t)
            while(self.x != 400):
                if(self.x + 10 <= 400):
                    self.x += 10
                    time.sleep(t)

        elif(espacioVacio[3] is None):
            self.x = 30
            self.y = 40
            espacioVacio[3] = self.numcliente
            time.sleep(t)
            while(self.x != 60):
                if(self.x + 10 <= 60):
                    self.x += 10
                    time.sleep(t)
            while(self.y != 530):
                if(self.y + 10 <= 530):
                    self.y += 10
                    time.sleep(t)
            while(self.x != 350):
                if(self.x + 10 <= 350):
                    self.x += 10
                    time.sleep(t)
        elif(espacioVacio[4] is None):
            self.x = 30
            self.y = 40
            espacioVacio[4] = self.numcliente
            time.sleep(t)
            while(self.x != 60):
                if(self.x + 10 <= 60):
                    self.x += 10
                    time.sleep(t)
            while(self.y != 530):
                if(self.y + 10 <= 530):
                    self.y += 10
                    time.sleep(t)
            while(self.x != 300):
                if(self.x + 10 <= 300):
                    self.x += 10
                    time.sleep(t)

        elif(espacioVacio[5] is None):
            self.x = 30
            self.y = 40
            espacioVacio[5] = self.numcliente
            time.sleep(t)
            while(self.x != 60):
                if(self.x + 10 <= 60):
                    self.x += 10
                    time.sleep(t)
            while(self.y != 530):
                if(self.y + 10 <= 530):
                    self.y += 10
                    time.sleep(t)
            while(self.x != 250):
                if(self.x + 10 <= 250):
                    self.x += 10
                    time.sleep(t)

        elif(espacioVacio[6] is None):
            self.x = 30
            self.y = 40
            espacioVacio[6] = self.numcliente
            time.sleep(t)
            while(self.x != 60):
                if(self.x + 10 <= 60):
                    self.x += 10
                    time.sleep(t)
            while(self.y != 530):
                if(self.y + 10 <= 530):
                    self.y += 10
                    time.sleep(t)
            while(self.x != 200):
                if(self.x + 10 <= 200):
                    self.x += 10
                    time.sleep(t)

    def sentarse_sofa(self):
        t = 0.05
        if s_sofa[1] is None:
            for x in espacioVacio.keys():
                if(espacioVacio[x] == self.numcliente):
                    espacioVacio[x] = None
                    break
            s_sofa[1] = self.numcliente
            time.sleep(t)
            while(self.x != 520):
                if(self.x + 10 <= 520):
                    self.x += 10
                    time.sleep(t)
            while(self.y != 560):
                if(self.y + 10 <= 560):
                    self.y += 10
                    time.sleep(t)
        elif s_sofa[2] is None:
            for x in espacioVacio.keys():
                if(espacioVacio[x] == self.numcliente):
                    espacioVacio[x] = None
                    break
            s_sofa[2] = self.numcliente
            time.sleep(t)
            while(self.x != 590):
                if(self.x + 10 <= 590):
                    self.x += 10
                    time.sleep(t)
            while(self.y != 560):
                if(self.y + 10 <= 560):
                    self.y += 10
                    time.sleep(t)
        elif s_sofa[3] is None:
            for x in espacioVacio.keys():
                if(espacioVacio[x] == self.numcliente):
                    espacioVacio[x] = None
                    break
            s_sofa[3] = self.numcliente
            time.sleep(t)
            while(self.x != 660):
                if(self.x + 10 <= 660):
                    self.x += 10
                    time.sleep(t)
            while(self.y != 560):
                if(self.y + 10 <= 560):
                    self.y += 10
                    time.sleep(t)
        elif s_sofa[4] is None:
            for x in espacioVacio.keys():
                if(espacioVacio[x] == self.numcliente):
                    espacioVacio[x] = None
                    break
            s_sofa[4] = self.numcliente
            time.sleep(t)
            while(self.x != 730):
                if(self.x + 10 <= 730):
                    self.x += 10
                    time.sleep(t)
            while(self.y != 560):
                if(self.y + 10 <= 560):
                    self.y += 10
                    time.sleep(t)

    def primerEspacio(self):
        primero = espacioVacio[1]
        espacioVacio[1] = None
        return primero

    def sentarse_silla(self):
        t = 0.05
        if s_silla[1] is None:
            for x in s_sofa.keys():
                if(s_sofa[x] == self.numcliente):
                    s_sofa[x] = None
                    break
            s_silla[1] = self.numcliente
            time.sleep(t)
            while(self.y != 360):
                if(self.y - 10 >= 360):
                    self.y -= 10
                    time.sleep(t)
            while(self.x != 400):
                if(self.x + 10 >= 400):
                    self.x -= 10
                    time.sleep(t)
            while(self.y != 280):
                if(self.y - 10 >= 280):
                    self.y -= 10
                    time.sleep(t)
        elif s_silla[2] is None:
            for x in s_sofa.keys():
                if(s_sofa[x] == self.numcliente):
                    s_sofa[x] = None
                    break
            s_silla[2] = self.numcliente
            time.sleep(t)
            while(self.y != 360):
                if(self.y - 10 >= 360):
                    self.y -= 10
                    time.sleep(t)
            while(self.x != 600):
                if(self.x > 600):
                    if(self.x + 10 >= 600):
                        self.x -= 10
                        time.sleep(t)
                elif(self.x < 600):
                    if(self.x + 10 <= 600):
                        self.x += 10
                        time.sleep(t)
            while(self.y != 280):
                if(self.y - 10 >= 280):
                    self.y -= 10
                    time.sleep(t)
        elif s_silla[3] is None:
            for x in s_sofa.keys():
                if(s_sofa[x] == self.numcliente):
                    s_sofa[x] = None
                    break
            s_silla[3] = self.numcliente
            time.sleep(t)
            while(self.y != 360):
                if(self.y - 10 >= 360):
                    self.y -= 10
                    time.sleep(t)
            while(self.x != 800):
                if(self.x + 10 <= 800):
                    self.x += 10
                    time.sleep(t)
            while(self.y != 280):
                if(self.y - 10 >= 280):
                    self.y -= 10
                    time.sleep(t)

    def espera_a_pagar(self):
        t = 0.05
        if e_pagar[0] is None:
            for x in s_silla.keys():
                if(s_silla[x] == self.numcliente):
                    s_silla[x] = None
                    break
            e_pagar[0] = self.numcliente
            time.sleep(t)
            while(self.y != 460):
                if(self.y + 10 <= 460):
                    self.y += 10
                    time.sleep(t)
            while(self.x != 950):
                if(self.x < 950):
                    if(self.x + 10 <= 950):
                        self.x += 10
                        time.sleep(t)
                elif(self.x > 950):
                    if(self.x - 10 >= 950):
                        self.x -= 10
                        time.sleep(t)
            while(self.y != 560):
                if(self.y + 10 <= 560):
                    self.y += 10
                    time.sleep(t)
        elif e_pagar[1] is None:
            for x in s_silla.keys():
                if(s_silla[x] == self.numcliente):
                    s_silla[x] = None
                    break
            e_pagar[1] = self.numcliente
            time.sleep(t)
            while(self.y != 460):
                if(self.y + 10 <= 460):
                    self.y += 10
                    time.sleep(t)
            while(self.x != 900):
                if(self.x < 900):
                    if(self.x + 10 <= 900):
                        self.x += 10
                        time.sleep(t)
                elif(self.x > 900):
                    if(self.x - 10 >= 900):
                        self.x -= 10
                        time.sleep(t)
            while(self.y != 560):
                if(self.y + 10 <= 560):
                    self.y += 10
                    time.sleep(t)
        elif e_pagar[2] is None:
            for x in s_silla.keys():
                if(s_silla[x] == self.numcliente):
                    s_silla[x] = None
                    break
            e_pagar[2] = self.numcliente
            time.sleep(t)
            while(self.y != 460):
                if(self.y + 10 <= 460):
                    self.y += 10
                    time.sleep(t)
            while(self.x != 850):
                if(self.x < 850):
                    if(self.x + 10 <= 850):
                        self.x += 10
                        time.sleep(t)
                elif(self.x > 850):
                    if(self.x - 10 >= 850):
                        self.x -= 10
                        time.sleep(t)
            while(self.y != 560):
                if(self.y + 10 <= 560):
                    self.y += 10
                    time.sleep(t)
        elif e_pagar[3] is None:
            for x in s_silla.keys():
                if(s_silla[x] == self.numcliente):
                    s_silla[x] = None
                    break
            e_pagar[3] = self.numcliente
            time.sleep(t)
            while(self.y != 460):
                if(self.y + 10 <= 460):
                    self.y += 10
                    time.sleep(t)
            while(self.x != 800):
                if(self.x < 800):
                    if(self.x + 10 <= 800):
                        self.x += 10
                        time.sleep(t)
                elif(self.x > 800):
                    if(self.x - 10 >= 800):
                        self.x -= 10
                        time.sleep(t)
            while(self.y != 560):
                if(self.y + 10 <= 560):
                    self.y += 10
                    time.sleep(t)
        elif e_pagar[4] is None:
            for x in s_silla.keys():
                if(s_silla[x] == self.numcliente):
                    s_silla[x] = None
                    break
            e_pagar[4] = self.numcliente
            time.sleep(t)
            while(self.y != 460):
                if(self.y + 10 <= 460):
                    self.y += 10
                    time.sleep(t)
            while(self.x != 750):
                if(self.x < 750):
                    if(self.x + 10 <= 750):
                        self.x += 10
                        time.sleep(t)
                elif(self.x > 750):
                    if(self.x - 10 >= 750):
                        self.x -= 10
                        time.sleep(t)
            while(self.y != 560):
                if(self.y + 10 <= 560):
                    self.y += 10
                    time.sleep(t)
        elif e_pagar[5] is None:
            for x in s_silla.keys():
                if(s_silla[x] == self.numcliente):
                    s_silla[x] = None
                    break
            e_pagar[5] = self.numcliente
            time.sleep(t)
            while(self.y != 460):
                if(self.y + 10 <= 460):
                    self.y += 10
                    time.sleep(t)
            while(self.x != 750):
                if(self.x < 750):
                    if(self.x + 10 <= 750):
                        self.x += 10
                        time.sleep(t)
                elif(self.x > 750):
                    if(self.x - 10 >= 750):
                        self.x -= 10
                        time.sleep(t)
            while(self.y != 500):
                if(self.y + 10 <= 500):
                    self.y += 10
                    time.sleep(t)
        elif e_pagar[6] is None:
            for x in s_silla.keys():
                if(s_silla[x] == self.numcliente):
                    s_silla[x] = None
                    break
            e_pagar[6] = self.numcliente
            time.sleep(t)
            while(self.y != 450):
                if(self.y + 10 <= 450):
                    self.y += 10
                    time.sleep(t)
            while(self.x != 750):
                if(self.x < 750):
                    if(self.x + 10 <= 750):
                        self.x += 10
                        time.sleep(t)
                elif(self.x > 750):
                    if(self.x - 10 >= 750):
                        self.x -= 10
                        time.sleep(t)
        elif e_pagar[7] is None:
            for x in s_silla.keys():
                if(s_silla[x] == self.numcliente):
                    s_silla[x] = None
                    break
            e_pagar[7] = self.numcliente
            time.sleep(t)
            while(self.y != 450):
                if(self.y + 10 <= 450):
                    self.y += 10
                    time.sleep(t)
            while(self.x != 750):
                if(self.x < 750):
                    if(self.x + 10 <= 750):
                        self.x += 10
                        time.sleep(t)
                elif(self.x > 750):
                    if(self.x - 10 >= 750):
                        self.x -= 10
                        time.sleep(t)

    def pagarCuenta(self):
        t = 0.05
        i = 0
        for x in e_pagar:
            if(x == self.numcliente):
                e_pagar[i] = None
                break
            i += 1
        time.sleep(t)
        while(self.y != 360):
            if(self.y - 10 >= 360):
                self.y -= 10
                time.sleep(t)

        while(self.x != 950):
            if(self.x < 950):
                if(self.x + 10 <= 950):
                    self.x += 10
                    time.sleep(t)
            elif(self.x > 950):
                if(self.x - 10 >= 950):
                    self.x -= 10
                    time.sleep(t)

    def salirTienda(self):
        t = 0.05
        time.sleep(t)
        while(self.y != 660):
            if(self.y + 10 <= 660):
                self.y += 10
                time.sleep(t)
        while(self.x != 1250):
            if(self.x + 10 <= 1250):
                self.x += 10
                time.sleep(t)


class Barbero(threading.Thread):
    def __init__(self, index):
        threading.Thread.__init__(self)
        self.i = index  # indice

    def run(self):
        while(True):
            global bAtendiendo
            cliente_listo.acquire()
            mutex2.acquire()
            client = colaCorte.pop()
            #Preparandose para cortale el pelo al cliente i

            mutex2.release()
            coord.acquire()
            coordinar.append(self.i)
            #Cortandole el pelo al cliente i
            time.sleep(11)
            coord.release()
            coordinar.remove(self.i)

            mutex3.acquire()
            bAtendiendo = self.i
            mutex3.release()
            #Corte de pelo del cliente i finalizado
            terminado[client].release()
            dejar_silla_b[self.i].acquire()
            silla_barbero.release()


def pintarCirculoB1(window, dimensiones):
    pygame.draw.circle(window, ROJO, (pos[0][0], pos[0][1]), 20)
    tipo_letra = pygame.font.Font(pygame.font.match_font('times'),
    dimensiones)
    superficie = tipo_letra.render("B" + str(0), True, AZUL)
    rectangulo = superficie.get_rect()
    rectangulo.center = (pos[0][0], pos[0][1])
    window.blit(superficie, rectangulo)


def pintarCirculoB2(window, dimensiones):
    pygame.draw.circle(window, ROJO, (pos[1][0], pos[1][1]), 20)
    tipo_letra = pygame.font.Font(pygame.font.match_font('times'),
    dimensiones)
    superficie = tipo_letra.render("B" + str(1), True, AZUL)
    rectangulo = superficie.get_rect()
    rectangulo.center = (pos[1][0], pos[1][1])
    window.blit(superficie, rectangulo)


def pintarCirculoB3(window, dimensiones):
    pygame.draw.circle(window, ROJO, (pos[2][0], pos[2][1]), 20)
    tipo_letra = pygame.font.Font(pygame.font.match_font('times'),
    dimensiones)
    superficie = tipo_letra.render("B" + str(2), True, AZUL)
    rectangulo = superficie.get_rect()
    rectangulo.center = (pos[2][0], pos[2][1])
    window.blit(superficie, rectangulo)


def actualizar(x, y, disp):
    global pos, coordinar
    t = 0.05
    if disp is not None:
        if(disp == 0):
            while(y != pos[0][1]):
                if(pos[0][1] - 10 >= y):
                    pos[0][1] -= 10
                    time.sleep(t)
            while(x != pos[0][0]):
                if(pos[0][0] - 10 >= x):
                    pos[0][0] -= 10
                    time.sleep(t)
        elif(disp == 1):
            while(y != pos[1][1]):
                if(pos[1][1] - 10 >= y):
                    pos[1][1] -= 10
                    time.sleep(t)
            while(x != pos[1][0]):
                if(pos[1][0] - 10 >= x):
                    pos[1][0] -= 10
                    time.sleep(t)
        elif(disp == 2):
            while(y != pos[2][1]):
                if(pos[2][1] - 10 >= y):
                    pos[2][1] -= 10
                    time.sleep(t)
            while(x != pos[2][0]):
                if(pos[2][0] - 10 >= x):
                    pos[2][0] -= 10
                    time.sleep(t)
        return None
    if(len(list(filter(lambda x: x == 2, coordinar))) <= 0):
        while(x != pos[2][0]):
            if(pos[2][0] + 10 <= x):
                pos[2][0] += 10
                time.sleep(t)

        while(y != pos[2][1]):
            if(pos[2][1] + 10 <= y):
                pos[2][1] += 10
                time.sleep(t)
        return 2
    elif(len(list(filter(lambda x: x == 1, coordinar))) <= 0):
        while(x != pos[1][0]):
            if(pos[1][0] + 10 <= x):
                pos[1][0] += 10
                time.sleep(t)

        while(y != pos[1][1]):
            if(pos[1][1] + 10 <= y):
                pos[1][1] += 10
                time.sleep(t)
        return 1
    elif(len(list(filter(lambda x: x == 0, coordinar))) <= 0):
        while(x != pos[0][0]):
            if(pos[0][0] + 10 <= x):
                pos[0][0] += 10
                time.sleep(t)

        while(y != pos[0][1]):
            if(pos[0][1] + 10 <= y):
                pos[0][1] += 10
                time.sleep(t)
        return 0


class Cajero(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while(True):
            global coordinar
            pago.acquire()
            coord.acquire()
            i = actualizar(1120, 360, None)
            #Realizando el pago del cliente i
            time.sleep(1.25)
            if i == 0:
                actualizar(400, 130, i)
            elif i == 1:
                actualizar(600, 130, i)
            elif i == 2:
                actualizar(800, 130, i)
            coord.release()
            recibo.release()
            #Recibo entregado al cliente i
            realiza_pago.release()