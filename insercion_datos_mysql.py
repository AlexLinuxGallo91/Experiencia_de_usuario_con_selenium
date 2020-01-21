import mysql.connector

db_connection = mysql.connector.connect(user='root', 
                                        password='root',
                                        host='127.0.0.1')

mi_cursor = db_connection.cursor()
mi_cursor.execute('CREATE DATABASE dummydatabase')
mi_cursor.execute('USE dummydatabase')

mi_cursor.execute("CREATE TABLE IF NOT EXISTS itoc_cat_accounts ("\
                  "idaccount bigint(20) NOT NULL AUTO_INCREMENT,"\
                  "db varchar(128) COLLATE latin1_spanish_ci NOT NULL,"\
                  "server varchar(128) COLLATE latin1_spanish_ci NOT NULL,"\
                  "user varchar(128) COLLATE latin1_spanish_ci NOT NULL,"\
                  "password varchar(32) COLLATE latin1_spanish_ci DEFAULT NULL,"\
                  "service varchar(24) COLLATE latin1_spanish_ci NOT NULL,"\
                  "creation_date timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,"\
                  "modif_date timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',"\
                  "deleted int(1) NOT NULL DEFAULT '0',"\
                  "PRIMARY KEY (idaccount))")

sentencia_insert_sql = 'INSERT INTO itoc_cat_accounts (idaccount, db, server, user, password, service, creation_date, ' \
                       'modif_date, deleted) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'

# Agregar aqui las sentencias de insercion

mi_cursor.close()
db_connection.close()
