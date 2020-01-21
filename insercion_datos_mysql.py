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

mi_cursor.execute(sentencia_insert_sql, (1, 'MTYDG1DS01DB001', 'APCNMBX01', 'mtydg1ds01db001@srv2010.vivetelmex.com', 
                                        'SUFiav+@92Lp0359@', 'Exchange 2010', '2017-10-26 03:00:40', '2018-02-02 04:47:43', 0))

mi_cursor.execute(sentencia_insert_sql, (2, 'MTYDG1DS01DB002', 'APCNMBX02', 'mtydg1ds01db002@srv2010.vivetelmex.com', 
                                        'SUFiav+@92Lp0359@', 'Exchange 2010', '2017-10-26 03:00:40', '2018-02-02 04:47:43', 0))

mi_cursor.execute(sentencia_insert_sql, (3, 'MTYDG1DS01DB003', 'APCNMBX03', 'mtydg1ds01db003@srv2010.vivetelmex.com', 
                                        'SUFiav+@92Lp0359@', 'Exchange 2010', '2017-10-26 03:00:40', '2018-02-02 04:47:43', 0))

mi_cursor.execute(sentencia_insert_sql, (4, 'MTYDG1DS01DB004', 'APCNMBX04', 'mtydg1ds01db004@srv2010.vivetelmex.com', 
                                        'SUFiav+@92Lp0359@', 'Exchange 2010', '2017-10-26 03:00:40', '2018-02-02 04:47:43', 0))

mi_cursor.execute(sentencia_insert_sql, (5, 'MTYDG1DS01DB005', 'APCNMBX17', 'mtydg1ds01db005@srv2010.vivetelmex.com', 
                                        'SUFiav+@92Lp0359@', 'Exchange 2010', '2017-10-26 03:00:40', '2018-02-02 04:47:43', 0))

mi_cursor.execute(sentencia_insert_sql, (6, 'MTYDG1DS01DB006', 'APCNMBX18', 'mtydg1ds01db006@srv2010.vivetelmex.com', 
                                        'SUFiav+@92Lp0359@', 'Exchange 2010', '2017-10-26 03:00:40', '2018-02-02 04:47:43', 0))

mi_cursor.execute(sentencia_insert_sql, (7, 'MTYDG1DS01DB007', 'APCNMBX19', 'mtydg1ds01db007@srv2010.vivetelmex.com', 
                                        'SUFiav+@92Lp0359@', 'Exchange 2010', '2017-10-26 03:00:40', '2018-02-02 04:47:43', 0))

mi_cursor.execute(sentencia_insert_sql, (8, 'MTYDG1DS01DB008', 'APCNMBX20', 'mtydg1ds01db008@correo.local', 
                                        'SUFiav+@92Lp0359@', 'Exchange 2010', '2017-10-26 03:00:40', '2018-02-02 04:47:43', 0))

mi_cursor.execute(sentencia_insert_sql, (9, 'MTYDG1DS01DB009', 'APCNMBX33', 'mtydg1ds01db009@srv2010.vivetelmex.com', 
                                        'SUFiav+@92Lp0359@', 'Exchange 2010', '2017-10-26 03:00:40', '2018-02-02 04:47:43', 0))

mi_cursor.execute(sentencia_insert_sql, (10, 'MTYDG1DS01DB010', 'APCNMBX21', 'mtydg1ds01db010@srv2010.vivetelmex.com', 
                                        'SUFiav+@92Lp0359@', 'Exchange 2010', '2017-10-26 03:00:40', '2018-02-02 04:47:43', 0))

mi_cursor.close()
db_connection.close()