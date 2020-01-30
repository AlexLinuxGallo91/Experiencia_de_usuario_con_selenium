from selenium import webdriver
from selenium.webdriver import chrome
from selenium.webdriver import Firefox
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import InvalidSessionIdException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from validacion_result import ValidacionResultList
from correo import Correo
from format_utils import FormatUtils
from temporizador import Temporizador
from validacion_result import Result
import logging
import mysql.connector
import json
import time

class SeleniumTesting:

    log = logging.getLogger(__name__)

    # inicializa un nuevo driver (firefox) para la experiencia de usuario
    # con el uso del navefador Mozilla Firefox
    @staticmethod
    def inicializar_webdriver_firefox(path_driver):
        opciones_firefox = webdriver.FirefoxOptions()
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
         
        opciones_firefox.headless = True

        return webdriver.Firefox(executable_path=path_driver, 
                                 firefox_options=opciones_firefox, 
                                 firefox_profile=perfil_firefox,
                                 capabilities=firefox_capabilities)


    # inicializa un nuevo driver (chrome driver) para la experiencia de usuario
    # con el uso del navefador google chrome
    #
    # UPDATE 29/enero/2020 11:51 P.M.
    #
    # En caso de utilizar el driver de chrome, el test de experiencia de usuario 
    # en el OWA fallara. Esto debido a que al momento de inicializar el driver
    # en modo "headless" (sin usar una interfaz grafica o el navegador en modo grafico)
    # no podra ejecutar ni permitir scripts en javascript. El ultimo paso
    # que se realiza de manera exitosa es al ingresar al portal de acceso OWA, pero 
    # al momento de navegar entre las carpetas y cerrar la sesion, estos pasos fallaran,
    # debido a que no renderiza/carga todo el contenido del sitio web por no permitir
    # la ejecucion de scripts al momento de utilizar el driver en modo headless.
    # 
    # Por ello es mejor utilizar el driver de Firefox, ya que hasta el momento es el
    # que ha dado menos problemas en realizar la prueba conectividad al OWA

    @staticmethod
    def inicializar_webdriver_chrome(path_driver):
        opciones_chrome = webdriver.ChromeOptions()
        
        # ignora las certificaciones de seguridad, esto solamente se realiza
        # para la experiencia de usuario
        opciones_chrome.add_argument('--ignore-certificate-errors')
        opciones_chrome.add_argument("--headless")
        opciones_chrome.add_argument('--allow-running-insecure-content')
        opciones_chrome.add_argument("--enable-javascript")
        opciones_chrome.add_argument('window-size=1920x1080')

        chrome_capabilities = webdriver.DesiredCapabilities().CHROME.copy()
        chrome_capabilities['acceptSslCerts'] = True 
        chrome_capabilities['acceptInsecureCerts'] = True

        return webdriver.Chrome(path_driver, chrome_options=opciones_chrome, 
        desired_capabilities=chrome_capabilities)

    # funcion el cual permite navegar hacia la url que se establezca como parametro
    @staticmethod
    def navegar_a_sitio(webdriver, url_a_navegar, result_list):
        
        resultado = Result()
        resultado.tiempo_inicio_de_ejecucion = 0
        resultado.inicializar_tiempo_de_ejecucion()
        
        SeleniumTesting.log.info('ingresando a la siguiente url: "{}"'.format(url_a_navegar))
        try:
            webdriver.set_page_load_timeout(20)
            webdriver.get(url_a_navegar)
            resultado.mensaje_error = 'Se ingresa al sitio con exito'
            resultado.validacion_correcta = True
            SeleniumTesting.log.info(resultado.mensaje_error)
        except WebDriverException as e:
            resultado.mensaje_error = 'No se puede ingresar al sitio, favor de verificar la red'
            resultado.validacion_correcta = False
            SeleniumTesting.log.error(resultado.mensaje_error)
        except TimeoutException as e:
            resultado.mensaje_error = 'Han transcurrido mas de 20 segundos sin'\
                                      ' poder acceder al sitio: {}'.format(e.msg)
            resultado.validacion_correcta = False
            SeleniumTesting.log.error(resultado.mensaje_error)    
        
        resultado.finalizar_tiempo_de_ejecucion()
        resultado.establecer_tiempo_de_ejecucion()
        result_list.result_validacion_ingreso_url = resultado
        return result_list


    @staticmethod
    def iniciar_sesion_en_owa(driver, correo_en_prueba, result_list):

        driver.accept_insecure_certs = True
        driver.accept_untrusted_certs = True

        resultado = Result()
        
        resultado.tiempo_inicio_de_ejecucion = Temporizador.obtener_tiempo_timer()
        resultado.datetime_inicial = Temporizador.obtener_fecha_tiempo_actual()
        
        # resultado.inicializar_tiempo_de_ejecucion()
        mensaje_error_de_credenciales = None
       
        try:
            # obtiene los elementos html para los campos de usuario, password y el boton de inicio de
            # sesion
            time.sleep(3)

            input_usuario = driver.find_element_by_id('username')
            input_password = driver.find_element_by_id('password')
            boton_ingreso_correo = driver.find_element_by_xpath("//input[@type='submit'][@class='btn']")

            # ingresa los datos en cada uno de los inputs localizados en el sitio de owa, uno por
            # cada segundo
            time.sleep(1)
            input_usuario.send_keys(correo_en_prueba.correo)
                
            time.sleep(1)
            input_password.send_keys(correo_en_prueba.password)
                
            time.sleep(1)
            boton_ingreso_correo.send_keys(Keys.RETURN)
            time.sleep(3)

        except NoSuchElementException:
            resultado.mensaje_error = 'No fue posible ingresar al portal, no se encontraron los inputs para credenciales'
            resultado.validacion_correcta = True
            SeleniumTesting.log.error(resultado.mensaje_error)
        except WebDriverException:
            resultado.mensaje_error = 'No se puede ingresar al sitio, favor de verificar la red'
            resultado.validacion_correcta = False
            SeleniumTesting.log.error(resultado.mensaje_error)
        
        # verifica que se haya ingresado correctamente al OWA, se localiza si esta establecido
        # el mensaje de error de credenciales dentro del aplicativo del OWA

        if resultado.validacion_correcta == False:
            try:
                mensaje_error_de_credenciales = driver.find_element_by_id('trInvCrd')
                SeleniumTesting.log.error('No se puede ingresar al aplicativo debido a error de credenciales:')
                mensaje_error_de_credenciales = driver.find_element_by_xpath("//tr[@id='trInvCrd']/td")
                SeleniumTesting.log.error('Se muestra el siguiente mensaje de advertencia: {} '.format(
                    mensaje_error_de_credenciales.get_attribute('innerHTML')))
                resultado.mensaje_error = 'No se puede ingresar al portal. Error de credenciales'
                resultado.validacion_correcta = False
            except NoSuchElementException:
                resultado.mensaje_error = 'Se ingresa correctamente al OWA'
                resultado.validacion_correcta = True
                SeleniumTesting.log.info(resultado.mensaje_error)
            except InvalidSessionIdException:
                resultado.mensaje_error = 'No se ingreso correctamente al portal. Error de conexion'
                resultado.validacion_correcta = False
                SeleniumTesting.log.error(resultado.mensaje_error)


        resultado.finalizar_tiempo_de_ejecucion()
        resultado.establecer_tiempo_de_ejecucion()
        result_list.result_validacion_acceso_portal_owa = resultado
        return result_list


    # verifica si se encontro el elemento deseado mediante el id
    # retorna True si se encontro el elemento
    # en caso contrario retorna False
    @staticmethod
    def verificar_elemento_encontrado_por_id(driver, id):
        elemento_html = None

        try:
            elemento_html = driver.find_element_by_id(id)
            SeleniumTesting.log.info('Se localiza el elemento {} correctamente'.format(elemento_html.id))
            return True
        except NoSuchElementException as e:
            SeleniumTesting.log.error('No se encontro el elemento con el id: {}'.format(id))
            SeleniumTesting.log.error(e)
            return False 


    # cuando se ingresa correctamen al OWA, se localizan las listas de folders
    # que contiene el usuario en sesion    
    @staticmethod
    def obtener_carpetas_en_sesion(driver):
        lista_de_carpetas_localizadas = [] 
        lista_nombres_de_carpetas_formateadas = []  

        time.sleep(8)
        lista_de_carpetas_localizadas = driver.find_elements_by_xpath("//*[@id='spnFldrNm']")

        for carpeta in lista_de_carpetas_localizadas:
            nombre_de_carpeta = FormatUtils.remover_backspaces(carpeta.get_attribute('innerHTML')) 
            SeleniumTesting.log.info('Se obtiene la carpeta: {}'.format(nombre_de_carpeta))
            lista_nombres_de_carpetas_formateadas.append(nombre_de_carpeta)
        
        return lista_nombres_de_carpetas_formateadas


    # ejecuta la navegacion de cada una de las carpetas que tiene la sesion de correo electronico
    # se establece como parametro el numero de segundos en que se estara ejecutando la navegacion
    # entre carpetas (lo estipulado con 2 min -> 120 s)
    @staticmethod
    def navegacion_de_carpetas_por_segundos(lista_carpetas, driver, result_list, numero_de_segundos=120):
                
        result_navegacion_carpetas = Result()
        result_navegacion_carpetas.inicializar_tiempo_de_ejecucion()
        tiempo_por_verificar = numero_de_segundos + Temporizador.obtener_tiempo_timer()
        tiempo_de_inicio = Temporizador.obtener_tiempo_timer()
        segundos = 0

        # verifica se tenga al menos una carpeta
        if len(lista_carpetas) == 0:
            result_navegacion_carpetas.finalizar_tiempo_de_ejecucion()
            result_navegacion_carpetas.establecer_tiempo_de_ejecucion()
            result_navegacion_carpetas.validacion_correcta = False
            result_navegacion_carpetas.mensaje_error = 'No se encontraron carpetas dentro de la sesion'
            result_list.result_validacion_navegacion_carpetas = result_navegacion_carpetas
            SeleniumTesting.log.info('No se encontraron carpetas por navegar')

            return result_list

        while Temporizador.obtener_tiempo_timer() <= tiempo_por_verificar:
            for carpeta in lista_carpetas:
                segundos = Temporizador.obtener_tiempo_timer() - tiempo_de_inicio  

                if segundos > numero_de_segundos:
                    SeleniumTesting.log.info('Han transcurrido 2 minutos, se procede a cerrar la sesion')
                    break

                SeleniumTesting.log.info('Ingresando a la carpeta: {}'.format(carpeta))

                try:     
                    elemento_html_carpeta = driver.find_element_by_xpath(
                        '//span[@id="spnFldrNm"][@fldrnm="{}"]'.format(carpeta))

                    time.sleep(3)
                    SeleniumTesting.verificar_dialogo_de_interrupcion(driver, result_navegacion_carpetas)
                    time.sleep(3)
                    elemento_html_carpeta.click()
                except StaleElementReferenceException as e:
                    SeleniumTesting.log.error('Una de las carpetas no se localiza, se intentara ingresar nuevamente')
                    SeleniumTesting.log.error('error: {}'.format(e.msg))
                    driver.refresh()
                    time.sleep(3)
                except ElementClickInterceptedException as e:
                    SeleniumTesting.log.error('Una de las carpetas no se localiza, se intentara ingresar nuevamente')
                    SeleniumTesting.log.error('error: {}'.format(e.msg))
                    driver.refresh()
                    time.sleep(3)
                except NoSuchElementException as e:
                    SeleniumTesting.log.error('Una de las carpetas no se localiza, se intentara ingresar nuevamente')
                    SeleniumTesting.log.error('error: {}'.format(e.msg))
                    driver.refresh()
                    time.sleep(3)
        
        result_navegacion_carpetas.finalizar_tiempo_de_ejecucion()
        result_navegacion_carpetas.establecer_tiempo_de_ejecucion()
        result_navegacion_carpetas.validacion_correcta = True
        result_navegacion_carpetas.mensaje_error = 'Se navega correctamente en las carpetas de la cuenta'
        result_list.result_validacion_navegacion_carpetas = result_navegacion_carpetas
        return result_list
                
    # verifica que no aparezca el dialogo de interrupcion (dialogo informativo que en algunas ocasiones
    # aparece cuando se ingresa a una carpeta con correos nuevos)
    @staticmethod
    def verificar_dialogo_de_interrupcion(driver, result):
        if len(driver.find_elements_by_id('divPont')) > 0:
                SeleniumTesting.log.info('Se ha encontrado un dialogo informativo, se procede a cerrarlo')
                
                try:
                    time.sleep(4)
                    boton_remover_dialogo = driver.find_element_by_id('imgX')
                    boton_remover_dialogo.click()
                except ElementClickInterceptedException:
                    SeleniumTesting.log.error('Se encontro un dialogo informativo pero fue imposible cerrarlo.')
                    SeleniumTesting.log.error('Se intenta nuevamente el cierre del dialogo')
                    SeleniumTesting.verificar_dialogo_de_interrupcion(driver, result)

        
    # Cierra la sesion desde el aplicativo y termina la sesion en el webdriver
    @staticmethod
    def cerrar_sesion(driver, result_list):

        resultado_cierre_sesion = Result()
        resultado_cierre_sesion.inicializar_tiempo_de_ejecucion()
        url_actual = ''
        elemento_html_btn_cerrar_sesion = None

        try:
            driver.refresh()
            time.sleep(3)

            # verifica que no haya algun dialogo que impida el cierre de sesion
            SeleniumTesting.verificar_dialogo_de_interrupcion(driver, resultado_cierre_sesion)
            
            elemento_html_btn_cerrar_sesion = driver.find_element_by_id('aLogOff')
            elemento_html_btn_cerrar_sesion.click()
            time.sleep(8)

            # obtiene la url actual como una cadena
            url_actual = driver.current_url

        except NoSuchElementException as e:
            SeleniumTesting.log.error('Error al salir de la sesion, no se localizo la opcion para el cierre de sesion')
            resultado_cierre_sesion.mensaje_error = 'No fue posible cerrar la sesion correctamente'
            resultado_cierre_sesion.validacion_correcta = False
        except ElementClickInterceptedException as e:
            SeleniumTesting.log.error('Error al salir de la sesion, no fue posible dar clic en la opcion de cierre de sesion')
            SeleniumTesting.log.error('Se intentara nuevamente el cierre de sesion')
            driver.refresh()
            time.sleep(2)
            SeleniumTesting.cerrar_sesion(driver, result_list)
        finally:
            driver.close()
            driver.quit()

        if 'exchangeadministrado.com/owa/auth/logoff.aspx' in url_actual:
            SeleniumTesting.log.info('Se cierra con exito la sesion')
            resultado_cierre_sesion.mensaje_error = 'Se cierra la sesion exitosamente'
            resultado_cierre_sesion.validacion_correcta = True
        else:
            resultado_cierre_sesion.mensaje_error = 'No fue posible cerrar la sesion correctamente'
            resultado_cierre_sesion.validacion_correcta = False
            SeleniumTesting.log.error(resultado_cierre_sesion.mensaje_error)

        resultado_cierre_sesion.finalizar_tiempo_de_ejecucion()
        resultado_cierre_sesion.establecer_tiempo_de_ejecucion()
        result_list.result_validacion_cierre_sesion = resultado_cierre_sesion

        return result_list
