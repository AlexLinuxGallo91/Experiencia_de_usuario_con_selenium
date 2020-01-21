from selenium import webdriver
from selenium.webdriver import chrome
from selenium.webdriver import Firefox
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from correo import Correo
from format_utils import FormatUtils
from temporizador import Temporizador
import mysql.connector
import json
import time

class SeleniumTesting:

    # inicializa un nuevo driver (firefox) para la experiencia de usuario
    # con el uso del navefador Mozilla Firefox
    @staticmethod
    def inicializar_webdriver_firefox(path_driver):
        opciones_firefox = webdriver.FirefoxOptions()
        
        # ignora las certificaciones de seguridad, esto solamente se realiza
        # para la experiencia de usuario
        opciones_firefox.add_argument('--ignore-certificate-errors')
        opciones_firefox.headless = True

        return webdriver.Firefox(executable_path=path_driver, firefox_options=opciones_firefox)


    # inicializa un nuevo driver (chrome driver) para la experiencia de usuario
    # con el uso del navefador google chrome
    @staticmethod
    def inicializar_webdriver_chrome(path_driver):
        opciones_chrome = webdriver.ChromeOptions()
        
        # ignora las certificaciones de seguridad, esto solamente se realiza
        # para la experiencia de usuario
        opciones_chrome.add_argument('--ignore-certificate-errors')
        return webdriver.Chrome(path_driver, chrome_options=opciones_chrome)


    # obtencion de usuarios y passwords de los correos electronicos desde un archivo JSON
    # alojado localmente en la carpeta del proyecto
    @staticmethod
    def obtencion_usuarios_desde_archivo_json(path_archivo_json):
        correos_obtenidos = []
        
        with open(path_archivo_json) as f:
            datos_obtenidos_json = json.load(f)
    
        for item in datos_obtenidos_json['correos']:
            print('datos obtenidos --> correo : {} - {}'.format(item['usuario'], item['password']))
            correos_obtenidos.append(Correo(item['usuario'], item['password']))   
        
        return correos_obtenidos


    # funcion el cual permite navegar hacia la url que se establezca como parametro
    @staticmethod
    def navegar_a_sitio(webdriver, url_a_navegar):
        print('navegando hacia {}'.format(url_a_navegar))
        webdriver.get(url_a_navegar)


    @staticmethod
    def iniciar_sesion_en_owa(driver, correo):

        # obtiene los elementos html para los campos de usuario, password y el boton de inicio de
        # sesion
        time.sleep(2)
        input_usuario = driver.find_element_by_id('username')
        input_password = driver.find_element_by_id('password')
        boton_ingreso_correo = driver.find_element_by_xpath("//input[@type='submit'][@class='btn']")

        # ingresa los datos en cada uno de los inputs localizados en el sitio de owa, uno por
        # cada segundo
        input_usuario.send_keys(correo.correo)
        time.sleep(1)
        input_password.send_keys(correo.password)
        time.sleep(1)
        boton_ingreso_correo.send_keys(Keys.RETURN)
        time.sleep(1)

        # verifica que se haya ingresado correctamente al OWA


    # verifica si se encontro el elemento deseado mediante el id
    # retorna True si se encontro el elemento
    # en caso contrario retorna False
    @staticmethod
    def verificar_elemento_encontrado_por_id(driver, id):
        elemento_html = None

        try:
            elemento_html = driver.find_element_by_id(id)
            print('Se localiza el elemento {} correctamente'.format(elemento_html.id))
            return True
        except NoSuchElementException as e:
            print('No se encontro el elemento con el id: {}'.format(id))
            print(e)
            return False 


    # cuando se ingresa correctamen al OWA, se localizan las listas de folders
    # que contiene el usuario en sesion    
    @staticmethod
    def obtener_carpetas_en_sesion(driver):
        lista_de_carpetas_localizadas = [] 
        lista_nombres_de_carpetas_formateadas = []  
        lista_de_carpetas_localizadas = driver.find_elements_by_xpath("//*[@id='spnFldrNm']")

        for carpeta in lista_de_carpetas_localizadas:
            nombre_de_carpeta = FormatUtils.remover_backspaces(carpeta.get_attribute('innerHTML')) 
            print('Se obtiene la carpeta: {}'.format(nombre_de_carpeta))

            lista_nombres_de_carpetas_formateadas.append(nombre_de_carpeta)
        
        return lista_nombres_de_carpetas_formateadas


    # ejecuta la navegacion de cada una de las carpetas que tiene la sesion de correo electronico
    # se establece como parametro el numero de segundos en que se estara ejecutando la navegacion
    # entre carpetas (lo estipulado con 2 min -> 120 s)
    @staticmethod
    def navegacion_de_carpetas_por_segundos(lista_carpetas, driver, numero_de_segundos=120):
                
        # inicializa un thread el cual se encargara de hacer el conteo de los segundos
        Temporizador.inicializar_hilo()

        while Temporizador.obtener_segundos_transcurridos() <= numero_de_segundos:
            for carpeta in lista_carpetas:

                if(Temporizador.obtener_segundos_transcurridos() >= 120):
                    # Se reinicia el temporizador a 0 segundos
                    Temporizador.reiniciar_segundos()
                    return

                print('Tiempo de navegacion de carpetas transcurrido: {}'.format(Temporizador.obtener_segundos_transcurridos()))
                print('Ingresando a la carpeta: {}'.format(carpeta))
                time.sleep(1)
                elemento_html_carpeta = driver
                elemento_html_carpeta = driver.find_element_by_xpath('//span[@id="spnFldrNm"][@fldrnm="{}"]'.format(carpeta))
                time.sleep(3)
                SeleniumTesting.verificar_dialogo_de_interrupcion(driver)
                elemento_html_carpeta.click()
                
    # verifica que no aparezca el dialogo de interrupcion (dialogo informativo que en algunas ocasiones
    # aparece cuando se ingresa a una carpeta con correos nuevos)
    @staticmethod
    def verificar_dialogo_de_interrupcion(driver):
        if len(driver.find_elements_by_id('divPont')) > 0:
                
                print('Se ha encontrado un dialogo informativo, se procede a cerrarlo')
                
                try:
                    time.sleep(2)
                    boton_remover_dialogo = driver.find_element_by_id('imgX')
                    boton_remover_dialogo.click()
                except ElementClickInterceptedException as e:
                    print('Se encontro un dialogo informativo pero fue imposible cerrarlo.')
                    print('Se intenta nuevamente el cierre del dialogo')
                    SeleniumTesting.verificar_dialogo_de_interrupcion(driver)

        
    # Cierra la sesion desde el aplicativo y termina la sesion en el webdriver
    @staticmethod
    def cerrar_sesion(driver):
        elemento_html_btn_cerrar_sesion = driver.find_element_by_id('aLogOff')
        elemento_html_btn_cerrar_sesion.send_keys(Keys.RETURN)
        driver.refresh()
        driver.close()
        driver.quit()
        pass
