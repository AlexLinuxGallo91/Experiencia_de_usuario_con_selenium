import db_utils

lista = db_utils.DbUtils.obtener_lista_cuentas_db()

for e in lista:
    print(e)