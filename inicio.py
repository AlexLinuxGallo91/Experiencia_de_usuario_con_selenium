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
import logging
import time
import json

#inicializa el logging
logging.basicConfig(level=logging.INFO,
                    filename='log_exchange_2010', 
                    filemode='w', 
                    format='%(asctime)s  %(name)s  %(levelname)s: %(message)s', 
                    datefmt='%m-%d %H:%M')
                    
correos_obtenidos = []
driver = None
path_web_driver = ''

#ruta del webdriver de chrome
path_web_driver = "/usr/bin/webdrivers/geckodriver"

#url exchange 2010 por probar
url_exchange = "https://exchangeadministrado.com/owa"

def iniciar_prueba(correo):
    carpetas_formateadas = []
    driver = SeleniumTesting.inicializar_webdriver_firefox(path_web_driver)
    SeleniumTesting.navegar_a_sitio(driver, url_exchange)
    SeleniumTesting.iniciar_sesion_en_owa(driver, correo)

    time.sleep(3)
    carpetas_formateadas = SeleniumTesting.obtener_carpetas_en_sesion(driver)
    time.sleep(3)

    # se inicializa la navegacion entre carpetas
    SeleniumTesting.navegacion_de_carpetas_por_segundos(carpetas_formateadas, driver)

    #se cierra sesion desde el OWA
    SeleniumTesting.cerrar_sesion(driver)

    # reinicia la lista de las carpetas
    carpetas_formateadas = []


# Punto de partida/ejecucion principal del script
def main():

    # Se obtienen los correos a probar
    lista_cuentas_correos = DbUtils.obtener_lista_cuentas_db()

    for user_correo in lista_cuentas_correos:
        iniciar_prueba(user_correo)

# Ejecucion principal del Script
main()
