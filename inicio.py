from selenium.webdriver import chrome
from selenium.webdriver.chrome import options
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from db_utils import DbUtils
from itocaccount import ItocAccount
from correo import Correo
from temporizador import Temporizador
from selenium_testing_utils import SeleniumTesting
from format_utils import FormatUtils
from statusJson import JsonPorEnviar
from validacion_result import Result
from validacion_result import EvaluacionStepsJson
from validacion_result import ValidacionResultList
import configparser
import sys
import logging
import time
import json
import datetime
import os
                    
correos_obtenidos = []

# funcion encargada de configurar el driver a utilizar (chrome o firefox)
# dependiendo de los valores que se hayan establecido dentro del archivo
# de configuracion (.ini)
def configurar_webdriver(driver_por_usar, ruta_driver_navegador):
    driver = None

    if len(ruta_driver_navegador.strip()) == 0:
        logging.info('Favor de establecer la ruta del driver por utilizar')
        sys.exit()

    if driver_por_usar == 'chrome':
        logging.info('Configurando driver chrome')
        driver = SeleniumTesting.inicializar_webdriver_chrome(ruta_driver_navegador.strip())
    elif driver_por_usar == 'firefox':
        logging.info('Configurando driver firefox')
        driver = SeleniumTesting.inicializar_webdriver_firefox(ruta_driver_navegador.strip())
    else:
        logging.info('Favor de establecer el driver a configurar (chrome o firefox)')
        sys.exit()

    return driver


def generar_test_json(driver, url_a_navegar, correo):
    lista_carpetas_por_navegar = []
    objeto_json = None

    # objeto con lista de objetos result el cual verificara cada una de 
    # las validaciones para cada uno de los steps y el cual nos permitira adjuntar 
    # el resultado en el JSON
    lista_validaciones = ValidacionResultList()

    # genera la estructura del archivo JSON (resultado/salida)
    objeto_json = JsonPorEnviar.generar_nuevo_template_json()

    # establece el datetime de inicio dentro del json
    objeto_json = EvaluacionStepsJson.establecer_fecha_tiempo_de_inicio(objeto_json)

    # empieza la primera validacion de ingresar a la url del portal
    lista_validaciones = SeleniumTesting.navegar_a_sitio(driver, url_a_navegar, lista_validaciones)

    # intenta ingresar las credenciales de la cuenta dentro del portal, verificando
    # el acceso del correo desde el portal 
    lista_validaciones = SeleniumTesting.iniciar_sesion_en_owa(driver, correo, lista_validaciones)

    # se obtiene la lista de carpetas que contiene el correo electronico
    lista_carpetas_por_navegar = SeleniumTesting.obtener_carpetas_en_sesion(driver)

    # empieza la validacion de la navegacion en cada una de las carpetas que se obtuvieron
    # en la linea anterior
    lista_validaciones = SeleniumTesting.navegacion_de_carpetas_por_segundos(
        lista_carpetas_por_navegar, driver,lista_validaciones)

    # se valida el cierre de sesion desde el OWA
    lista_validaciones = SeleniumTesting.cerrar_sesion(driver, lista_validaciones)

    # establece los datos en el json con los resultados de cada una de las validaciones
    objeto_json = EvaluacionStepsJson.formar_cuerpo_json(lista_validaciones, objeto_json)

    return objeto_json

def iniciar_prueba(correo, url_exchange):
    
    # obtiene los datos del archivo de configuracion
    archivo_configuracion_ini = FormatUtils.lector_archivo_ini()
    driver_por_usar = FormatUtils.CADENA_VACIA
    ruta_driver_navegador = FormatUtils.CADENA_VACIA
    driver = None
    objeto_json = None

    try:
        # url_exchange = archivo_configuracion_ini.get('UrlPorProbar','urlPortalExchange')
        driver_por_usar = archivo_configuracion_ini.get('Driver', 'driverPorUtilizar')
        ruta_driver_navegador = archivo_configuracion_ini.get('Driver', 'ruta')
    except configparser.Error as e:
        logging.error('Sucedio un error al momento de leer el archivo de configuracion')
        logging.error('{}'.format(e.message))
        sys.exit()

    # lista de carpetas por navegar (estos los obtenemos por medio del webdriver)
    carpetas_formateadas = []

    # obtiene los datos necesarios desde el archivo de configuracion

    # establece el driver por utilizar (chrome o firefox)
    driver = configurar_webdriver(driver_por_usar, ruta_driver_navegador)

    # se generan las validaciones y el resultado por medio de un objeto JSON
    objeto_json = generar_test_json(driver, url_exchange, correo)

    # como salida, muestra/imprime el json generado
    print(json.dumps(objeto_json))

# Punto de partida/ejecucion principal del script
def main():

    argumentos = sys.argv[1:]
    correo_a_probar = None
    nombre_archivo_log = 'log_exchange_owa'

    # verifica que el archivo del log, exista
    if os.path.exists(nombre_archivo_log):
        # verifica el tamaño del archivo del log que no revase los 20mb
        if os.path.getsize('log_exchange_owa')/(1024*1024) > 20:
            archivo_log = open(nombre_archivo_log, 'a')
            archivo_log.truncate(0)
            archivo_log.close()

    #inicializa el logging
    logging.basicConfig(level=logging.INFO, 
                        filename='log_exchange_owa', 
                        filemode='a', 
                        format='%(asctime)s  %(name)s  %(levelname)s: %(message)s', 
                        datefmt='%d-%m-%YT%H:%M:%S')

    # verifica que al menos se hayan ingresado dos argumentos
    if len(argumentos) != 3:
        print('favor de ingresar url, correo y password')
        logging.info('favor de ingresar correo y password')
        sys.exit()
    else:
        correo_a_probar = Correo(argumentos[1],argumentos[2])
        logging.info('url por ingresar: {}'.format(argumentos[0]))
        logging.info('cuenta por analizar: {}'.format(correo_a_probar))

    iniciar_prueba(correo_a_probar, argumentos[0])

    # Se obtienen los correos a probar
    #lista_cuentas_correos = DbUtils.obtener_lista_cuentas_db()

    #for user_correo in lista_cuentas_correos:
    #    iniciar_prueba(user_correo)


# Ejecucion principal del Script
main()
