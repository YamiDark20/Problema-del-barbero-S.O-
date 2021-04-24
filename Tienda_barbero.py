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
dejar_silla_b = threading.Semaphore(0)
pago = threading.Semaphore(0)
recibo = threading.Semaphore(0)
terminado = [threading.Semaphore(0) for i in range(50)]
count = 0
cliente_b = None
colaCorte = []
colaPago = []
realiza_pago = threading.Semaphore(1)


class Cliente(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.numcliente = 0

    def run(self):
        global count
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
        time.sleep(2)
        dejar_silla_b.release()
        print("Pagar cuenta", self.numcliente)
        time.sleep(7)

        realiza_pago.acquire()
        colaPago.append(self.numcliente)
        pago.release()
        recibo.acquire()
        print("Salir de la tienda")
        time.sleep(3)
        max_cap.release()

class Barbero(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while(True):
            cliente_listo.acquire()
            mutex2.acquire()
            aux = colaCorte.pop()
            print("Agregar en cola a cliente", aux)
            mutex2.release()
            coord.acquire()
            print("Cortando el pelo del cliente", aux)
            time.sleep(4)
            coord.release()
            terminado[aux].release()
            dejar_silla_b.acquire()
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
barbero = [Barbero() for _ in range(3)]
cajero = Cajero()

for c in clientes:
    c.start()

for b in barbero:
    b.start()

cajero.start()
print("Todo esta iniciado")
#https://www.youtube.com/watch?v=lsHCzboWK0U