import time #modulo necesario para utlizacion de funcion sleep()
import random #modulo necesario para utilizar la funcion randint()
import threading #modulo utilizado para la manipulacion de hilos

N = 5
TIEMPO_TOTAL = 3

class filosofo(threading.Thread):
    semaforo = threading.RLock() #semaforo binario, el cual nos asegura la exclusion mutua
    estado = [] #guarda el estado de cada filosofo
    tenedores = [] #arreglo de semaforos, muestra quien esta en la cola del tenedor
    count=0 

    #constructor
    def __init__(self):
        super().__init__()    #nos sirve para heredar 
        self.id=filosofo.count #se le asigna el id al filosofo
        filosofo.count+=1 #incrementa el contador de filosofos
        filosofo.estado.append('PENSANDO') #se ejecuta el filosofo con estado "PENSANDO"
        filosofo.tenedores.append(threading.Semaphore(0)) #agrega el semaforo de su tenedor (tenedor a la izquierda)
        print("FILOSOFO {0} - PENSANDO".format(self.id)) #imprimimos el numero de filosofo con el estado "PENSANDO"
    
    #destructor
    def __del__(self):
        print("FILOSOFO {0} - Se para de la mesa".format(self.id))  #se necesita para saber cuando termina el proceso o hilo

    def pensar(self):
        time.sleep(random.randint(0,5)) #se le asigna un tiempo aleatorio a cada filosofo para pensar

    def derecha(self,i):
        return (i-1)%N #buscamos a la derecha

    def izquierda(self,i):
        return(i+1)%N #buscamos a la izquierda

    def verificar(self,i):
        if filosofo.estado[i] == 'HAMBRIENTO' and filosofo.estado[self.izquierda(i)] != 'COMIENDO' and filosofo.estado[self.derecha(i)] != 'COMIENDO':
            filosofo.estado[i]='COMIENDO' #le asigna al filosofo el estado "COMIENDO"
            filosofo.tenedores[i].release()  #verifica si los vecinos no estan comiendo, si es asi aumenta el semaforo y cambia su estado a "COMIENDO"

    def tomar(self):
        filosofo.semaforo.acquire() #exclusion mutua
        filosofo.estado[self.id] = 'HAMBRIENTO' #cambia el estado del filosofo a "HAMBRIENTO"
        self.verificar(self.id) #verifica a sus vecinos
        filosofo.semaforo.release() #cambia el arreglo de estado (ya intento de tomar los tenedores)
        filosofo.tenedores[self.id].acquire() #en caso de poder tomarlos, este se bloqueara con estado "COMIENDO"

    def soltar(self):
        filosofo.semaforo.acquire() #soltara los tenedores
        filosofo.estado[self.id] = 'PENSANDO' #cambia estado a "PENSANDO"
        self.verificar(self.izquierda(self.id)) #verifica a la izquierda
        self.verificar(self.derecha(self.id)) #verifica a la derecha
        filosofo.semaforo.release() #fin de minipulacion de tenedores

    def comer(self):
        print("FILOSOFO {} COMIENDO".format(self.id))
        time.sleep(2) #tiempo dado para comer, es el tiempo de espera
        print("FILOSOFO {} TERMINO DE COMER".format(self.id))

    #funciones que se ejecutaran:
    def run(self):
        for i in range(TIEMPO_TOTAL): #tiempo asignado al principio del codigo
            self.pensar() #filosofo filosofando
            self.tomar() #tomar los tenedores correspondientes
            self.comer() #el filosofo come
            self.soltar() #suelta tenedores

def main():
    lista=[]
    for i in range(N):
        lista.append(filosofo()) #agregamos un filosofo a la lista

    for f in lista:
        f.start() #equivale a run() nos sirve para que el programa empiece a trabajar

    for f in lista:
        f.join() #bloquea hasta terminado el hilo

if __name__=="__main__":
    main()
