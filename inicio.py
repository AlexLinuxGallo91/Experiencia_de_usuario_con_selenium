from selenium.webdriver import chrome
from selenium.webdriver.chrome import options
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from correo import Correo
from temporizador import Temporizador
import logging
import time
import json

#inicializa el logging
logging.basicConfig(level=logging.INFO,filename='log_exchange_2010', filemode='w', 
                    format='%(asctime)s  %(name)s  %(levelname)s: %(message)s', datefmt='%m-%d %H:%M')

correos_obtenidos = []
carpetas_formateadas = []
driver = None
path_web_driver = ''

def obtencion_datos_json():
    with open('correos.json') as f:
        datos_obtenidos_json = json.load(f)
    
    for item in datos_obtenidos_json['correos']:
        logging.info('correo por revisar: {} - {}'.format(item['usuario'], item['password']))
        correos_obtenidos.append(Correo(item['usuario'], item['password']))   

    print(datos_obtenidos_json['path_web_driver']) 

def testing_correo_navegador(correo):
    driver = webdriver.Chrome(path_web_driver, chrome_options=options)

    driver.get(url_exchange)
    logging.info('se ingresa al sitio: {}'.format(driver.title))

    correo_usuario = correo.correo
    correo_password = correo.password

    input_usuario = driver.find_element_by_id('username')
    input_password = driver.find_element_by_id('password')
    boton_ingreso_correo = driver.find_element_by_xpath("//input[@type='submit'][@class='btn']")

    input_usuario.send_keys(correo_usuario)
    input_password.send_keys(correo_password)
    boton_ingreso_correo.send_keys(Keys.RETURN)

    time.sleep(3)

    elementos_carpetas_encontradas = driver.find_elements_by_xpath("//*[@id='spnFldrNm']")

    for carpeta in elementos_carpetas_encontradas:
        carpetas_formateadas.append(carpeta.get_attribute('innerHTML').replace('&nbsp;', ' '))

    logging.info('numero de carpetas obtenidas: {}'.format(len(elementos_carpetas_encontradas)))

    for carpeta in carpetas_formateadas:
        logging.info('carpeta obtenida: {}'.format(carpeta))

    time.sleep(3)

    #se cierra sesion desde el OWA
    boton_cerrar_sesion = driver.find_element_by_id('aLogOff')
    boton_cerrar_sesion.send_keys(Keys.RETURN)
    driver.refresh()
    driver.close()

obtencion_datos_json()

#ruta del webdriver de chrome
path_web_driver = 'C:\webdrivers\chromedriver.exe'

#url exchange 2010 por probar
url_exchange = "https://exchangeadministrado.com/owa"
print()
logging.info('ingresando a la siguiente URL: {}'.format(url_exchange))

#establece ignorar certificados de seguridad con el fin de evitar
#que aparezca la ventana de advertencia para paginas inseguras
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')

for correo in correos_obtenidos:
    testing_correo_navegador(correo)
