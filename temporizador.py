import threading
import time

class Temporizador:

    segundos_transcurridos = 0
    hilo = None

    @staticmethod
    def inicializar_hilo():
        Temporizador.hilo = threading.Thread(target=Temporizador.verificar_temporizador)
        Temporizador.hilo.start()

    @staticmethod
    def verificar_temporizador():
        while Temporizador.segundos_transcurridos < 120:
            Temporizador.segundos_transcurridos = Temporizador.segundos_transcurridos + 1
            time.sleep(1) 

    @staticmethod
    def reiniciar_segundos(self):
        Temporizador.segundos_transcurridos = 0

    @staticmethod
    def obtener_segundos_transcurridos():
        return Temporizador.segundos_transcurridos

