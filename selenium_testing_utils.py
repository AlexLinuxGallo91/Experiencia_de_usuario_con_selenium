from selenium import webdriver
from selenium.webdriver import chrome
from selenium.webdriver import Firefox
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from correo import Correo
from format_utils import FormatUtils
from temporizador import Temporizador
from validacion_result import Result
import mysql.connector
import json
import time

class SeleniumTesting:

    # inicializa un nuevo driver (firefox) para la experiencia de usuario
    # con el uso del navefador Mozilla Firefox
    @staticmethod
    def inicializar_webdriver_firefox(path_driver):
        #opciones_firefox = webdriver.FirefoxOptions()
        perfil_firefox = webdriver.FirefoxProfile()
        firefox_capabilities = webdriver.DesiredCapabilities().FIREFOX.copy()
        firefox_capabilities.update({'acceptInsecureCerts': True, 'acceptSslCerts': True})
        firefox_capabilities['acceptSslCerts'] = True

        # ignora las certificaciones de seguridad, esto solamente se realiza
        # para la experiencia de usuario
        #opciones_firefox.add_argument('--ignore-certificate-errors')
        #opciones_firefox.accept_insecure_certs = True
        perfil_firefox.accept_untrusted_certs = True
        perfil_firefox.assume_untrusted_cert_issuer = False
         
        # opciones_firefox.headless = True

        return webdriver.Firefox(executable_path=path_driver, 
                                 #firefox_options=opciones_firefox, 
                                 firefox_profile=perfil_firefox,
                                 capabilities=firefox_capabilities)


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
        resultado = Result()

        resultado.inicializar_tiempo_de_ejecucion()
        print('ingresando a la siguiente url: "{}"'.format(url_a_navegar))
        try:
            webdriver.set_page_load_timeout(10)
            webdriver.get(url_a_navegar)
            resultado.mensaje_error = 'Se ingresa al sitio con exito'
            resultado.validacion_correcta = True
            print(resultado.mensaje_error)
        except TimeoutException as e:
            resultado.mensaje_error = 'Han transcurrido mas de 10 segundos sin'\
                                      'poder acceder al sitio: {}'.format(e.msg)
            resultado.validacion_correcta = False
            print(resultado.mensaje_error)
        
        resultado.finalizar_tiempo_de_ejecucion()
        resultado.establecer_tiempo_de_ejecucion()
        return resultado


    @staticmethod
    def iniciar_sesion_en_owa(driver, correo_en_prueba):
        # obtiene los elementos html para los campos de usuario, password y el boton de inicio de
        # sesion
        time.sleep(2)
        input_usuario = driver.find_element_by_id('username')
        input_password = driver.find_element_by_id('password')
        boton_ingreso_correo = driver.find_element_by_xpath("//input[@type='submit'][@class='btn']")
        mensaje_error_de_credenciales = None
        result = Result()

        # ingresa los datos en cada uno de los inputs localizados en el sitio de owa, uno por
        # cada segundo
        time.sleep(1)
        input_usuario.send_keys(correo_en_prueba.correo)
        time.sleep(1)
        input_password.send_keys(correo_en_prueba.password)
        time.sleep(1)
        boton_ingreso_correo.send_keys(Keys.RETURN)
        time.sleep(3)

        driver.accept_insecure_certs = True
        driver.accept_untrusted_certs = True

        # verifica que se haya ingresado correctamente al OWA, se localiza si esta establecido
        # el mensaje de error de credenciales dentro del aplicativo del OWA
        try:
            mensaje_error_de_credenciales = driver.find_element_by_id('trInvCrd')
            print('No se puede ingresar al aplicativo debido a error de credenciales:')
            mensaje_error_de_credenciales = driver.find_element_by_xpath("//tr[@id='trInvCrd']/td")
            print('Se muestra el siguiente mensaje de advertencia: {} '.format(
                mensaje_error_de_credenciales.get_attribute('innerHTML')))
            result.mensaje_error = 'No se puede ingresar al portal. Error de credenciales'
            result.validacion_correcta = False
        except NoSuchElementException:
            print('No se encontro el mensaje de error de credenciales')
            result.mensaje_error = 'No se encontro el mensaje de error de credenciales'
            result.validacion_correcta = True
        
        return result

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

        tiempo_por_verificar = numero_de_segundos + Temporizador.obtener_tiempo_timer()
        tiempo_de_inicio = Temporizador.obtener_tiempo_timer()
        segundos = 0
        while Temporizador.obtener_tiempo_timer() <= tiempo_por_verificar:
            for carpeta in lista_carpetas:
                
                segundos = Temporizador.obtener_tiempo_timer() - tiempo_de_inicio  
                print('Tiempo transcurrido: {}s'.format(segundos))

                if segundos > numero_de_segundos:
                    print('Han transcurrido 2 minutos, se procede a cerrar la sesion')
                    return

                print('Ingresando a la carpeta: {}'.format(carpeta))
                elemento_html_carpeta = driver.find_element_by_xpath('//span[@id="spnFldrNm"][@fldrnm="{}"]'.format(carpeta))
                time.sleep(4)
                SeleniumTesting.verificar_dialogo_de_interrupcion(driver)
                elemento_html_carpeta.click()
                
                
    # verifica que no aparezca el dialogo de interrupcion (dialogo informativo que en algunas ocasiones
    # aparece cuando se ingresa a una carpeta con correos nuevos)
    @staticmethod
    def verificar_dialogo_de_interrupcion(driver):
        if len(driver.find_elements_by_id('divPont')) > 0:
                print('Se ha encontrado un dialogo informativo, se procede a cerrarlo')
                
                try:
                    time.sleep(8)
                    boton_remover_dialogo = driver.find_element_by_id('imgX')
                    boton_remover_dialogo.click()
                except ElementClickInterceptedException:
                    print('Se encontro un dialogo informativo pero fue imposible cerrarlo.')
                    print('Se intenta nuevamente el cierre del dialogo')
                    SeleniumTesting.verificar_dialogo_de_interrupcion(driver)

        
    # Cierra la sesion desde el aplicativo y termina la sesion en el webdriver
    @staticmethod
    def cerrar_sesion(driver):
        elemento_html_btn_cerrar_sesion = driver.find_element_by_id('aLogOff')
        elemento_html_btn_cerrar_sesion.click()
        time.sleep(8)

        url_actual = driver.current_url

        if 'exchangeadministrado.com/owa/auth/logoff.aspx' in url_actual:
            print('Se cierra con exito la sesion')

        driver.refresh()

        time.sleep(10)

        driver.close()
        driver.quit()
