from itocaccount import ItocAccount
from mysql.connector import Error
import mysql.connector
import format_utils

class DbUtils:

    # Constantes para el uso de operaciones dentro de la bd

    QUERY_OBTENER_TODAS_LAS_CUENTAS = 'SELECT idaccount, db, server, user, password, service, creation_date, '\
                                      'modif_date, deleted FROM itoc_cat_accounts'

    @staticmethod
    def leer_datos_conexion_db():
        datos_db = DatosConexionDB()
        config = format_utils.FormatUtils.lector_archivo_ini()
        
        datos_db.user = config.get('DatosConexionBaseDeDatos', 'user')
        datos_db.password = config.get('DatosConexionBaseDeDatos', 'password')
        datos_db.host = config.get('DatosConexionBaseDeDatos', 'host')
        datos_db.database = config.get('DatosConexionBaseDeDatos', 'database')

        return datos_db
    
    @staticmethod
    def generar_conexion_a_db():
        datos_conexion_db = DbUtils.leer_datos_conexion_db()
        conexion_db = None
        try:
            conexion_db = mysql.connector.connect(user=datos_conexion_db.user,
                                                  password=datos_conexion_db.password,
                                                  host=datos_conexion_db.host,
                                                  database=datos_conexion_db.database)
        except Error as e:
            print('sucedio un error al establecer la conexion a la base de datos')
            print(e.msg)

        return conexion_db

    @staticmethod
    def obtener_lista_cuentas_db():
        lista_cuentas = []
        conexion_db = None
        
        try:
            conexion_db = DbUtils.generar_conexion_a_db()

            # obtiene todos los rows de la tabla de las cuentas
            cursor = conexion_db.cursor()
            cursor.execute(DbUtils.QUERY_OBTENER_TODAS_LAS_CUENTAS)
            records = cursor.fetchall()

            # itera en cada fila y agrega cada cuenta a la lista
            for fila in records:
                
                # Parametros para el constructor
                idaccount = fila[0] 
                db = fila[1]
                server = fila[2] 
                user = fila[3]
                password = fila[4]
                service = fila[5]
                creation_date = fila[6]
                modif_date = fila[7]
                deleted = fila[8]
                
                lista_cuentas.append(ItocAccount(idaccount, db, server, user, 
                                                 password, service, creation_date, 
                                                 modif_date, deleted))
        except Error as e:
            print('Sucedio un error al intentar obtener la lista de cuentas de correos')
            print(e.msg)
        finally:
            if(conexion_db.is_connected()):
                conexion_db.close()
                cursor.close()
                
        return lista_cuentas

class DatosConexionDB:

    def __init__(self, user = '', password = '', host = '', database = ''):
        self.user = user
        self.password = password
        self.host = host
        self.database = database

    def __str__(self):
        return 'user:{self.user}, pass:{self.password}, host:{self.host}, '\
               'database:{self.database}'.format(self=self)