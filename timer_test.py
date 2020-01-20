import threading
import time

segundos = 0

def tarea():
    global segundos
    while segundos < 120:
        segundos = segundos + 1
        time.sleep(1)
        

hilo = threading.Thread(target=tarea)
hilo.start()


