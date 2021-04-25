import threading
import time

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
terminado = [threading.Semaphore(0) for i in range(50)]
count = 0
cliente_b = None
colaCorte = []
colaPago = []
realiza_pago = threading.Semaphore(1)
prueba = 70  # Variable para aumentar el tiempo que tardan en ejecutarse los
             # clientes
mutex3 = threading.Semaphore(1)

#Las siguientes 3 variables son para almacenar los indicadores
#de que proceso Cliente i esta en la silla del barbero j
trab_silla1 = None
trab_silla2 = None
trab_silla3 = None

# Tablas vacias donde se van a mostrar los datos
Tabla = """\
+---------------------------------------------------------------------+
| N° Cliente| Silla_B| Sofa| Area_Esp| Dentro_Shop| Fuera_Shop| Cajero|
|---------------------------------------------------------------------|
{}
+---------------------------------------------------------------------+\
"""
Tabla2 = """\
+-----------------------+
| N° Cliente| N° Barbero|
|-----------------------|
{}
+-----------------------+\
"""
Tabla3 = """\
+---------------------------------------------+
| N° Cliente| N° Barbero| Cortando| Finalizado|
|---------------------------------------------|
{}
+---------------------------------------------+\
"""
Tabla4 = """\
+-------------------------------------+
| N° Cliente| Pagando| Recibo Recibido|
|-------------------------------------|
{}
+-------------------------------------+\
"""

#sillasActivas = [["N° Cliente", "N° Barbero"], [- 1, 0], [- 1, 1], [- 1, 2]]
sillasActivas2 = [[- 1, 0], [- 1, 1], [- 1, 2]]


class Cliente(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.numcliente = 0
        self.info2 = [[- 1, "No", "No", "No", "No", "Si", "No"]]

    def run(self):
        global count, prueba, trab_silla1, trab_silla2, trab_silla3, Tabla
        max_cap.acquire()
        time.sleep(3)
        mutex1.acquire()
        self.numcliente = count
        self.info2[0][0] = self.numcliente
        self.info2[0][3] = "Si"
        self.info2[0][4] = "Si"
        self.info2[0][5] = "No"
        #Entrando a la tienda
        print(Tabla.format('\n'.join(
        "| {:>10}|{:>8}|{:>5}|{:>9}|{:>12}|{:>11}|{:>7}|".format(
        *fila) for fila in self.info2)))

        count += 1
        mutex1.release()
        sofa.acquire()
        self.info2[0][2] = "Si"
        self.info2[0][3] = "No"
        #Sentandose en el sofa
        print(Tabla.format('\n'.join(
        "| {:>10}|{:>8}|{:>5}|{:>9}|{:>12}|{:>11}|{:>7}|".format(
        *fila) for fila in self.info2)))
        time.sleep(3)
        silla_barbero.acquire()

        self.info2[0][2] = "No"
        #Levantandose del sofa
        print(Tabla.format('\n'.join(
        "| {:>10}|{:>8}|{:>5}|{:>9}|{:>12}|{:>11}|{:>7}|".format(
        *fila) for fila in self.info2)))
        time.sleep(4)
        sofa.release()

        self.info2[0][1] = "Si"
        #Sentandose en la silla
        print(Tabla.format('\n'.join(
        "| {:>10}|{:>8}|{:>5}|{:>9}|{:>12}|{:>11}|{:>7}|".format(
        *fila) for fila in self.info2)))
        time.sleep(5)
        mutex2.acquire()
        if(self.numcliente < 2):
            time.sleep(1)
        colaCorte.append(self.numcliente)  # ########
        cliente_listo.release()
        mutex2.release()
        terminado[self.numcliente].acquire()

        #Las siguientes 8 lineas de codigo han sido modificada para
        #realizar lo pedido en la b)
        valorS = - 1
        if(trab_silla1 is not None):
            if(trab_silla1[1] == 0 and trab_silla1[0] == self.numcliente):
                valorS = 0
        if(trab_silla2 is not None):
            if(trab_silla2[1] == 1 and trab_silla2[0] == self.numcliente):
                valorS = 1
        if(trab_silla3 is not None):
            if(trab_silla3[1] == 2 and trab_silla3[0] == self.numcliente):
                valorS = 2
        #Las siguientes lineas de codigo del if hasta el time.sleep
        #Las realice para simular que la lentintud de los primeros
        #procesos
        if(prueba > 0):
            prueba -= 10
        time.sleep(2 + prueba)

        #La siguiente linea es parte de lo que nos pide en la b)
        dejar_silla_b[valorS].release()
        self.info2[0][1] = "No"
        self.info2[0][6] = "Si"
        #Dejando silla y llendo hacia el cajero
        print(Tabla.format('\n'.join(
        "| {:>10}|{:>8}|{:>5}|{:>9}|{:>12}|{:>11}|{:>7}|".format(
        *fila) for fila in self.info2)))
        if (sillasActivas2[0][0] == self.numcliente):
                sillasActivas2[0][0] = - 1
        elif(sillasActivas2[1][0] == self.numcliente):
                sillasActivas2[1][0] = - 1
        elif(sillasActivas2[2][0] == self.numcliente):
                sillasActivas2[2][0] = - 1
        #Tabla de que barbero esta con que cliente
        print(Tabla2.format('\n'.join(
        "| {:>10}|{:>11}|".format(*fila) for fila in sillasActivas2)))
        time.sleep(7)

        realiza_pago.acquire()
        colaPago.append(self.numcliente)
        pago.release()
        recibo.acquire()
        self.info2[0][5] = "Si"
        self.info2[0][6] = "No"
        self.info2[0][4] = "No"
        #Saliendo de la tienda
        print(Tabla.format('\n'.join(
        "| {:>10}|{:>8}|{:>5}|{:>9}|{:>12}|{:>11}|{:>7}|".format(
        *fila) for fila in self.info2)))
        max_cap.release()


class Barbero(threading.Thread):
    def __init__(self, index):
        threading.Thread.__init__(self)
        self.i = index
        self.info = [
            [- 1, - 1, "No", "No"]]

    def run(self):
        while(True):
            global trab_silla1, trab_silla2, trab_silla3
            cliente_listo.acquire()
            mutex2.acquire()
            self.info[0][0] = colaCorte.pop()
            self.info[0][1] = self.i
            if(sillasActivas2[0][1] == self.i):
                sillasActivas2[0][0] = self.info[0][0]
            elif(sillasActivas2[1][1] == self.i):
                sillasActivas2[1][0] = self.info[0][0]
            elif(sillasActivas2[2][1] == self.i):
                sillasActivas2[2][0] = self.info[0][0]

            #Preparandose para cortale el pelo al cliente i
            print(Tabla3.format('\n'.join(
            "| {:>10}|{:>11}|{:>9}|{:>11}|".format(
            *fila) for fila in self.info)))
            #Tabla donde se coloca que barbero esta con que cliente
            print(Tabla2.format('\n'.join(
        "| {:>10}|{:>11}|".format(*fila) for fila in sillasActivas2)))

            mutex2.release()
            coord.acquire()
            self.info[0][2] = "Si"
            #Cortandole el pelo al cliente i
            print(Tabla3.format('\n'.join(
            "| {:>10}|{:>11}|{:>9}|{:>11}|".format(
            *fila) for fila in self.info)))

            time.sleep(4)
            coord.release()

            #Las siguientes 8 lineas de codigo han sido modificada para
            #realizar lo pedido en la b)
            mutex3.acquire()
            if(self.i == 0):
                trab_silla1 = [self.info[0][0], self.i]
            elif(self.i == 1):
                trab_silla2 = [self.info[0][0], self.i]
            elif(self.i == 2):
                trab_silla3 = [self.info[0][0], self.i]
            mutex3.release()
            self.info[0][2] = "No"
            self.info[0][3] = "Si"
            #Corte de pelo del cliente i finalizado
            print(Tabla3.format('\n'.join(
            "| {:>10}|{:>11}|{:>9}|{:>11}|".format(
            *fila) for fila in self.info)))
            terminado[self.info[0][0]].release()
            dejar_silla_b[self.i].acquire()
            silla_barbero.release()
            self.info[0][2] = "No"
            self.info[0][3] = "No"
            #print("Corte finalizado del cliente", self.info[0][0])


class Cajero(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.info = [
            [- 1, "No", "No"]]

    def run(self):
        while(True):
            pago.acquire()
            coord.acquire()
            self.info[0][0] = colaPago.pop()
            self.info[0][1] = "Si"
            #Realizando el pago del cliente i
            print(Tabla4.format('\n'.join(
            "| {:>10}|{:>8}|{:>16}|".format(*fila) for fila in self.info)))
            time.sleep(4)
            coord.release()
            recibo.release()
            self.info[0][1] = "No"
            self.info[0][2] = "Si"
            #Recibo entregado al cliente i
            print(Tabla4.format('\n'.join(
            "| {:>10}|{:>8}|{:>16}|".format(*fila) for fila in self.info)))
            realiza_pago.release()
            self.info[0][1] = "No"
            self.info[0][2] = "No"

clientes = [Cliente() for _ in range(14)]
barbero = [Barbero(i) for i in range(3)]
cajero = Cajero()

for c in clientes:
    c.start()

for b in barbero:
    b.start()

cajero.start()