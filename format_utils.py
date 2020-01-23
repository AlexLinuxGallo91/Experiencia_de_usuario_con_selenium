import configparser

class FormatUtils:

    CADENA_VACIA = ''

    # lector de propiedades dentro de un archivo ini
    @staticmethod
    def lector_archivo_ini(path_archivo_ini):
        config = None

        try:
            config = configparser.ConfigParser()
            config.read('config.ini')
        except Error as e:
            print('sucedio un error al leer el archivo de configuracion: {}'.format(e))
        
        return config
            

    # remueve los espacios en los textos de los elementos HTML
    @staticmethod
    def remover_backspaces(cadena):
        return cadena.replace('&nbsp;', ' ')

    

    