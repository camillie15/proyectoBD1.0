import cx_Oracle 

try: 
    connection = cx_Oracle.connect(
        user = 'CAMI',
        password = 'CAMI',
        dsn = 'localhost:1521/XEPDB1',
        encoding = 'UTF-8'
    )
    print(connection.version)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM USUARIO")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
except Exception as ex:
    print(ex)
finally: connection.close()
print("Conexion finalizada")