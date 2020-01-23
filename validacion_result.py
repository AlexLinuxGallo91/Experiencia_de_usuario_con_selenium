from temporizador import Temporizador
import constantes_json

class Result:

    def __init__(self):
        self.validacion_correcta = False
        self.mensaje_error = ''
        self.tiempo_ejecucion = 0

class EvaluacionStepsJson:

    # validacion de ingreso a sitio:
    @staticmethod
    def validacion_ingreso_a_sitio(validacion_result, objeto_json):

        objeto_json['steps'][0]['output'][0]['status'] = validacion_result.mensaje_error
        return objeto_json


    # validacion para verificar el inicio de sesion correctamente
    @staticmethod
    def validacion_json_inicio_sesion(validacion_result, objeto_json):

        objeto_json['steps'][0]['output'][0]['status'] = validacion_result.mensaje_error
        return objeto_json


    @staticmethod
    def establecer_fecha_tiempo_de_inicio(objeto_json):

        objeto_json['start'] = Temporizador.obtener_fecha_tiempo_actual()
        return objeto_json

    @staticmethod
    def establecer_tiempo_de_finalizacion(objeto_json):

        objeto_json['time'] = Temporizador.obtener_tiempo_timer()
        objeto_json['status'] = constantes_json.STATUS_CORRECTO
        objeto_json['end'] = Temporizador.obtener_fecha_tiempo_actual()
        return objeto_json

