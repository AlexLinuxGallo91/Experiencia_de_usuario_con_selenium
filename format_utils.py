import configparser
import logging

class FormatUtils:

    CADENA_VACIA = ''
    NOMBRE_ARCHIVO_CONFIGURACION = 'config.ini'
    BACKSPACE = '&nbsp;'
    ESPACIO = ' '
    log = logging.getLogger(__name__)

    # lector de propiedades dentro de un archivo ini
    @staticmethod
    def lector_archivo_ini():
        config = None

        try:
            config = configparser.ConfigParser()
            config.read(FormatUtils.NOMBRE_ARCHIVO_CONFIGURACION)
        except Error as e:
            FormatUtils.log.error('sucedio un error al leer el archivo de configuracion: {}'.format(e))
        
        return config
            

    # remueve los espacios en los textos de los elementos HTML
    @staticmethod
    def remover_backspaces(cadena):
        return cadena.replace(FormatUtils.BACKSPACE, FormatUtils.ESPACIO)

    

    