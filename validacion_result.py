from temporizador import Temporizador
import constantes_json

class Result:

    def __init__(self):
        self.validacion_correcta = False
        self.mensaje_error = ''
        self.tiempo_inicio_de_ejecucion = 0
        self.tiempo_fin_de_ejecucion = 0
        self.tiempo_total_de_la_ejecucion = 0
        self.datetime_inicial = ''
        self.datetime_final = ''

    def establecer_tiempo_de_ejecucion(self):
        tiempo_inicial = self.tiempo_inicio_de_ejecucion
        tiempo_final = self.tiempo_fin_de_ejecucion
        self.tiempo_total_de_la_ejecucion = tiempo_final - tiempo_inicial

    def inicializar_tiempo_de_ejecucion(self):
        self.datetime_inicial = Temporizador.obtener_fecha_tiempo_actual()
        self.tiempo_inicio_de_ejecucion = Temporizador.obtener_tiempo_timer()

    def finalizar_tiempo_de_ejecucion(self):
        self.datetime_final = Temporizador.obtener_fecha_tiempo_actual()
        self.tiempo_fin_de_ejecucion = Temporizador.obtener_tiempo_timer()
        self.establecer_tiempo_de_ejecucion()
    
    
class EvaluacionStepsJson:

    # validacion de ingreso a sitio:
    @staticmethod
    def validacion_json_ingreso_a_sitio(validacion_result, objeto_json):
        objeto_json['steps'][0]['status'] = constantes_json.STATUS_CORRECTO
        objeto_json['steps'][0]['output'][0]['output'] = validacion_result.mensaje_error
        objeto_json['steps'][0]['output'][0]['status'] = constantes_json.STATUS_CORRECTO
        objeto_json['steps'][0]['start'] = validacion_result.datetime_inicial
        objeto_json['steps'][0]['end'] = validacion_result.datetime_final
        objeto_json['steps'][0]['time'] = validacion_result.tiempo_total_de_la_ejecucion

        return objeto_json


    # validacion para verificar el inicio de sesion correctamente
    @staticmethod
    def validacion_json_inicio_sesion(validacion_result, objeto_json):

        objeto_json['steps'][0]['status'] = constantes_json.STATUS_CORRECTO
        objeto_json['steps'][0]['output'][0]['output'] = validacion_result.mensaje_error
        objeto_json['steps'][0]['output'][0]['status'] = constantes_json.STATUS_CORRECTO
        objeto_json['steps'][0]['start'] = validacion_result.datetime_inicial
        objeto_json['steps'][0]['end'] = validacion_result.datetime_final
        objeto_json['steps'][0]['time'] = validacion_result.tiempo_total_de_la_ejecucion

        return objeto_json


    # validacion para verificar el inicio de sesion correctamente
    @staticmethod
    def validacion_json_navegacion_carpetas(validacion_result, objeto_json):

        objeto_json['steps'][1]['status'] = constantes_json.STATUS_CORRECTO
        objeto_json['steps'][1]['output'][0]['output'] = validacion_result.mensaje_error
        objeto_json['steps'][1]['output'][0]['status'] = constantes_json.STATUS_CORRECTO
        objeto_json['steps'][1]['start'] = validacion_result.datetime_inicial
        objeto_json['steps'][1]['end'] = validacion_result.datetime_final
        objeto_json['steps'][1]['time'] = validacion_result.tiempo_total_de_la_ejecucion

        return objeto_json

    
    # validacion para verificar el inicio de sesion correctamente
    @staticmethod
    def validacion_json_cierre_sesion(validacion_result, objeto_json):

        objeto_json['steps'][2]['status'] = constantes_json.STATUS_CORRECTO
        objeto_json['steps'][2]['output'][0]['output'] = validacion_result.mensaje_error
        objeto_json['steps'][2]['output'][0]['status'] = constantes_json.STATUS_CORRECTO
        objeto_json['steps'][2]['start'] = validacion_result.datetime_inicial
        objeto_json['steps'][2]['end'] = validacion_result.datetime_final
        objeto_json['steps'][2]['time'] = validacion_result.tiempo_total_de_la_ejecucion

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
    
    @staticmethod
    def formar_cuerpo_json(result_list, objeto_json):
        
        # se establece el tiempo de inicio

        # validaciones de cada step
        objeto_json = EvaluacionStepsJson.validacion_json_ingreso_a_sitio(
            result_list.result_validacion_ingreso_url, objeto_json)

        objeto_json = EvaluacionStepsJson.validacion_json_inicio_sesion(
            result_list.result_validacion_acceso_portal_owa, objeto_json)

        objeto_json = EvaluacionStepsJson.validacion_json_navegacion_carpetas(
            result_list.result_validacion_navegacion_carpetas, objeto_json)

        objeto_json = EvaluacionStepsJson.validacion_json_cierre_sesion(
            result_list.result_validacion_cierre_sesion, objeto_json)

        objeto_json = EvaluacionStepsJson.establecer_tiempo_de_finalizacion(objeto_json)

        # se establece el tiempo fin 
            
        return objeto_json

class ValidacionResultList:

    def __init__(self):
        self.result_tiempo_de_ejecucion = Result()
        
        # establece el tiempo de inicio de ejecucion
        self.result_validacion_ingreso_url = Result()
        self.result_validacion_acceso_portal_owa = Result()
        self.result_validacion_navegacion_carpetas = Result()
        self.result_validacion_cierre_sesion = Result()


    def __str__(self):
        v_url = 'validacion url: {}'.format(self.result_validacion_ingreso_url.validacion_correcta)
        
        v_portal_owa = 'validacion ingreso portal owa {}'.format(self.
                                            result_validacion_acceso_portal_owa.validacion_correcta)
        
        v_n_carpetas = 'validacion navegacion carpetas: {}'.format(self.
                                            result_validacion_navegacion_carpetas.validacion_correcta)

        v_cierre_sesion = 'validacion cierre sesion: {}'.format(self.result_validacion_cierre_sesion.
                                            validacion_correcta)

        return '{}\n{}\n{}\n{}\n'.format(v_url, v_portal_owa, v_n_carpetas, v_cierre_sesion)