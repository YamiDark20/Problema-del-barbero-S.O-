import threading
import time
#n_sem = 1
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


class Cliente(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.numcliente = 0

    def run(self):
        global count, prueba, trab_silla1, trab_silla2, trab_silla3
        max_cap.acquire()
        print("Entrar a la tienda")
        time.sleep(3)
        mutex1.acquire()
        self.numcliente = count
        count += 1
        mutex1.release()
        sofa.acquire()
        print("Sentarse en sofa", self.numcliente)
        time.sleep(3)
        silla_barbero.acquire()
        print("Levantarse del sofa", self.numcliente)
        time.sleep(4)
        sofa.release()

        print("Sentarse en silla de barbero", self.numcliente)
        time.sleep(5)
        mutex2.acquire()
        print("Cliente ", self.numcliente, "en cola")
        colaCorte.append(self.numcliente)
        cliente_listo.release()
        mutex2.release()
        terminado[self.numcliente].acquire()
        print("Dejar silla del barbero", self.numcliente)

        #Las siguientes 8 lineas de codigo han sido modificada para
        #realizar lo pedido en la b)
        valorS = - 1
        if(trab_silla1[1] == 0 and trab_silla1[0] == self.numcliente):
            valorS = 0
        elif(trab_silla2[1] == 1 and trab_silla2[0] == self.numcliente):
            valorS = 1
        elif(trab_silla3[1] == 2 and trab_silla3[0] == self.numcliente):
            valorS = 2
        print(valorS)
        #Las siguientes lineas de codigo del if hasta el time.sleep
        #Las realice para simular que la lentintud de los primeros
        #procesos
        if(prueba > 0):
            prueba -= 10
        time.sleep(2 + prueba)
        ############################################
        #La siguiente linea de codigo la realice para saber el nombre del
        #proceso que esta en curso
        print(threading.current_thread().getName())

        #La siguiente linea es parte de lo que nos pide en la b)
        dejar_silla_b[valorS].release()
        print("Pagar cuenta", threading.current_thread().getName(), self.numcliente)
        time.sleep(7)

        realiza_pago.acquire()
        colaPago.append(self.numcliente)
        pago.release()
        recibo.acquire()
        print("Salir de la tienda", threading.current_thread().getName())
        print("\n\n\n")
        #time.sleep(3)
        max_cap.release()

class Barbero(threading.Thread):
    def __init__(self, index):
        threading.Thread.__init__(self)
        self.i = index

    def run(self):
        while(True):
            global trab_silla1, trab_silla2, trab_silla3
            cliente_listo.acquire()
            mutex2.acquire()
            aux = colaCorte.pop()
            print("Agregar en cola a cliente", aux, threading.current_thread().getName())
            mutex2.release()
            coord.acquire()
            print("Cortando el pelo del cliente", aux)
            time.sleep(4)
            coord.release()

            #La siguiente linea de codigo la realice para saber el nombre del
            #proceso que esta en curso
            print(threading.current_thread().getName(), self.i)

            #Las siguientes 8 lineas de codigo han sido modificada para
            #realizar lo pedido en la b)
            mutex3.acquire()
            if(self.i == 0):
                trab_silla1 = [aux, self.i]
            elif(self.i == 1):
                trab_silla2 = [aux, self.i]
            elif(self.i == 2):
                trab_silla3 = [aux, self.i]
            mutex3.release()
            terminado[aux].release()
            dejar_silla_b[self.i].acquire()
            ######################################################
            silla_barbero.release()
            print("Corte finalizado del cliente", aux)

class Cajero(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while(True):
            pago.acquire()
            coord.acquire()
            print("Realizando pago del cliente", colaPago.pop())
            time.sleep(4)
            coord.release()
            recibo.release()
            realiza_pago.release()

clientes = [Cliente() for _ in range(10)]
barbero = [Barbero(i) for i in range(3)]
cajero = Cajero()

for c in clientes:
    c.start()

for b in barbero:
    b.start()

cajero.start()
print("Todo esta iniciado")
#https://www.youtube.com/watch?v=lsHCzboWK0U