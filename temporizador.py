import threading
import time
import datetime

class Temporizador:

    @staticmethod
    def obtener_tiempo_timer():
        return time.perf_counter()


    @staticmethod
    def obtener_fecha_tiempo_actual():
        fecha_actual = datetime.datetime.now()
        return fecha_actual.strftime('%Y-%m-%dT%H:%M-06:00')

    
    


