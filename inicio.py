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
logging.basicConfig(level=logging.INFO, filename='log_exchange_2010', filemode='w', 
                    format='%(asctime)s  %(name)s  %(levelname)s: %(message)s', datefmt='%m-%d %H:%M')
                    
correos_obtenidos = []
driver = None
path_web_driver = ''

#ruta del webdriver de chrome
path_web_driver = "/usr/bin/webdrivers/geckodriver"
path_web_driver_local_firefox = 'C:\webdrivers\geckodriver.exe'
path_web_driver_local_chrome = 'C:\webdrivers\geckodriver.exe'

#url exchange 2010 por probar
url_exchange = "https://exchangeadministrado.com/owa"

def iniciar_prueba(correo):

    # lista de carpetas por navegar (estos los obtenemos por medio del webdriver)
    carpetas_formateadas = []

    # genera la estructura del archivo JSON (resultado/salida)
    objeto_json = JsonPorEnviar.generar_nuevo_template_json()

    # establece el datetime de inicio dentro del json
    objeto_json = EvaluacionStepsJson.establecer_fecha_tiempo_de_inicio(objeto_json)

    # objeto con lista de objetos result el cual verificara cada una de 
    # las validaciones para cada uno de los steps y el cual nos permitira adjuntar 
    # el resultado en el JSON
    lista_validaciones = ValidacionResultList()

    # inicializa el driver, ya ses con un navegador chrome o firefox
    driver = SeleniumTesting.inicializar_webdriver_firefox(path_web_driver_local_firefox)

    lista_validaciones = SeleniumTesting.navegar_a_sitio(driver, url_exchange, lista_validaciones)
    lista_validaciones = SeleniumTesting.iniciar_sesion_en_owa(driver, correo, lista_validaciones)

    time.sleep(2)
    carpetas_formateadas = SeleniumTesting.obtener_carpetas_en_sesion(driver)

    lista_validaciones = SeleniumTesting.navegacion_de_carpetas_por_segundos(carpetas_formateadas, 
                                                  driver,lista_validaciones, numero_de_segundos=30)

    #se cierra sesion desde el OWA
    lista_validaciones = SeleniumTesting.cerrar_sesion(driver, lista_validaciones)
    
    # reinicia la lista de las carpetas
    carpetas_formateadas = []

    objeto_json = EvaluacionStepsJson.formar_cuerpo_json(lista_validaciones, objeto_json)

    # escribe el archivo JSON
    with open('result_json_{}.json'.format(datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")), 'w') as fp:
        json.dump(objeto_json, fp, indent=4, separators=(',', ': '))

# Punto de partida/ejecucion principal del script
def main():

    argumentos = sys.argv[1:]
    correo_a_probar = None

    # verifica que al menos se hayan ingresado dos argumentos
    if len(argumentos) != 2:
        print('favor de ingresar correo y password')
        return exit(1)
    else:
        correo_a_probar = Correo(argumentos[0],argumentos[1])
        print('cuenta por analizar: {}'.format(correo_a_probar))

    iniciar_prueba(correo_a_probar)

    # Se obtienen los correos a probar
    #lista_cuentas_correos = DbUtils.obtener_lista_cuentas_db()

    #for user_correo in lista_cuentas_correos:
    #    iniciar_prueba(user_correo)


# Ejecucion principal del Script
main()
