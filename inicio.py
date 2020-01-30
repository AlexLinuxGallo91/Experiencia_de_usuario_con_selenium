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
import sys
import logging
import time
import json
import datetime

#inicializa el logging
logging.basicConfig(level=logging.INFO, 
                    filename='log_exchange_owa', 
                    filemode='a', 
                    format='%(asctime)s  %(name)s  %(levelname)s: %(message)s', 
                    datefmt='%d-%m-%YT%H:%M:%S')
                    
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

def iniciar_prueba(correo):
    
    # obtiene los datos del archivo de configuracion
    archivo_configuracion_ini = FormatUtils.lector_archivo_ini()
    url_exchange = archivo_configuracion_ini.get('UrlPorProbar','urlPortalExchange')
    driver_por_usar = archivo_configuracion_ini.get('Driver', 'driverPorUtilizar')
    ruta_driver_navegador = archivo_configuracion_ini.get('Driver', 'ruta')
    driver = None
    objeto_json = None

    # lista de carpetas por navegar (estos los obtenemos por medio del webdriver)
    carpetas_formateadas = []

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

    # verifica que al menos se hayan ingresado dos argumentos
    if len(argumentos) != 2:
        logging.info('favor de ingresar correo y password')
        return exit(1)
    else:
        correo_a_probar = Correo(argumentos[0],argumentos[1])
        logging.info('cuenta por analizar: {}'.format(correo_a_probar))

    iniciar_prueba(correo_a_probar)

    # Se obtienen los correos a probar
    #lista_cuentas_correos = DbUtils.obtener_lista_cuentas_db()

    #for user_correo in lista_cuentas_correos:
    #    iniciar_prueba(user_correo)


# Ejecucion principal del Script
main()
