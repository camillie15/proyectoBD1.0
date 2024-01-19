import cx_Oracle 

try: 
    connection = cx_Oracle.connect(
        user = 'CAMI',
        password = 'CAMI',
        dsn = 'localhost:1521/XEPDB1',
        encoding = 'UTF-8'
    )
    print(connection.version)
except Exception as ex:
    print(ex)
