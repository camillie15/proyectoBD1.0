from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for

from conf import config
from conexion_oracle import connection, cursor

app = Flask(__name__, static_folder='static', template_folder='template')
evento_Id = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/createEvent', methods = ['GET', 'POST'])
def createEvent():
    global evento_Id
    if request.method == 'POST':
        data = request.form

        checkbox_privada = 'Privada' if 'checkboxPrivada' in data else None
        checkbox_publica = 'Publica' if 'checkboxPublica' in data else None
        clasificacion_id = None
        if checkbox_privada == 'Privada':
            clasificacion_id = 2 
        elif checkbox_publica == 'Publica':
            clasificacion_id = 1  

        checkbox_presencial = 'Presencial' if 'checkboxPresencial' in data else None
        checkbox_virtual = 'Virtual' if 'checkboxVirtual' in data else None
        modalidad_id = None
        if checkbox_virtual == 'Virtual':
            modalidad_id = 2 
        elif checkbox_presencial == 'Presencial':
            modalidad_id = 1  


        cursor = connection.cursor()
        sql = """
            INSERT INTO CAY_EVENTO(
                ID_EVENTO, NOMBRE, UBICACION, DESCRIPCION,
                CANTIDAD_INVITADOS, ID_MODALIDAD, ID_CLASIFICACION, 
                FECHA_INICIO, HORA_INICIO, FECHA_FIN, HORA_FIN
            ) VALUES(
                :idE, :nameE, :ubiEvento, :descripcionE,
                :cantInv, :modalEvent, :clasEvent, 
                TO_DATE(:dateEvent1, 'YYYY-MM-DD'), :timeEvent1,  
                TO_DATE(:dateEvent2, 'YYYY-MM-DD'),  :timeEvent2)
        """ 
        cursor.execute(
            sql, 
            idE = data['idEvento'], 
            nameE = data['nameEvento'], 
            ubiEvento = data['ubicacionEvento'], 
            descripcionE = data['descriptionEvento'], 
            cantInv = data['cantidadInvitados'], 
            modalEvent = modalidad_id, 
            clasEvent = clasificacion_id, 
            dateEvent1 = data['date1'], 
            timeEvent1=data['time1'], 
            dateEvent2 = data['date2'], 
            timeEvent2=data['time2']
        )
        connection.commit()
        cursor.close()
        
        evento_Id = data['idEvento']
        return redirect(url_for('aditionals'))
    return render_template('index2.html')
    
@app.route('/editEvent/<idEvento>', methods=['GET', 'POST'])
def editEvent(idEvento):
    if request.method == 'GET':
        cursor2 = connection.cursor()
        sql = "SELECT * FROM CAY_EVENTO WHERE ID_EVENTO = :idEvento"
        cursor2.execute(sql, idEvento = idEvento)
        evento = cursor2.fetchone()
        print(evento)
        cursor2.close()
        
        if evento:
            evento = list(evento)
            if evento[7] is not None:
                evento[7] = evento[7].strftime('%Y-%m-%d')
            if evento[9] is not None:
                evento[9] = evento[9].strftime('%Y-%m-%d')

            return render_template('index3.html', evento=evento)
        
    elif request.method == 'POST':
            data = request.form

            checkbox_privada = 'Privada' if 'checkboxPrivada' in data else None
            checkbox_publica = 'Publica' if 'checkboxPublica' in data else None
            clasificacion_id = None
            if checkbox_privada == 'Privada':
                clasificacion_id = 2 
            elif checkbox_publica == 'Publica':
                clasificacion_id = 1  

            checkbox_presencial = 'Presencial' if 'checkboxPresencial' in data else None
            checkbox_virtual = 'Virtual' if 'checkboxVirtual' in data else None
            modalidad_id = None
            if checkbox_virtual == 'Virtual':
                modalidad_id = 2 
            elif checkbox_presencial == 'Presencial':
                modalidad_id = 1  

            cursor3 = connection.cursor()
            sql2 = """
                UPDATE CAY_EVENTO
                SET
                    NOMBRE = :nameE,
                    UBICACION = :ubiEvento,
                    DESCRIPCION = :descripcionE,
                    CANTIDAD_INVITADOS = :cantInv,
                    ID_MODALIDAD = :modalEvent,
                    ID_CLASIFICACION = :clasEvent,
                    FECHA_INICIO = TO_DATE(:dateEvent1, 'YYYY-MM-DD'),
                    HORA_INICIO = :timeEvent1,
                    FECHA_FIN = TO_DATE(:dateEvent2, 'YYYY-MM-DD'),
                    HORA_FIN = :timeEvent2
                WHERE ID_EVENTO = :idE
            """ 
            cursor3.execute(
                sql2, 
                nameE = data['nameEvento'], 
                ubiEvento = data['ubicacionEvento'], 
                descripcionE = data['descriptionEvento'], 
                cantInv = data['cantidadInvitados'], 
                modalEvent = modalidad_id, 
                clasEvent = clasificacion_id, 
                dateEvent1 = data['date1'], 
                timeEvent1 = data['time1'],
                dateEvent2 = data['date2'], 
                timeEvent2 = data['time2'],
                idE = data['idEvento']
            )
            connection.commit()
            cursor3.close()
            return redirect(url_for('tusEventosPage'))
        
    return render_template('index3.html')

@app.route('/tusEventosPage')
def tusEventosPage():
    cursor4 = connection.cursor()
    sql = "SELECT * FROM CAY_EVENTO"
    cursor4.execute(sql)
    eventos = cursor4.fetchall()
    cursor4.close()
    return render_template('index1.html', eventos = eventos)

@app.route('/medioPago', methods=['GET', 'POST'])
def medioPago():
    if request.method == 'POST':
        data = request.form
        
        checkbox_card = 'Tarjeta' if 'checkboxCard' in data else None
        checkbox_bank = 'Banco' if 'checkboxBank' in data else None
        medio_pago_id = None
        if checkbox_card == 'Tarjeta':
            medio_pago_id = 2 
        elif checkbox_bank == 'Banco':
            medio_pago_id = 1  

        cursor9 = connection.cursor()
        sql = """
            INSERT INTO CAY_PAGO(
                ID_PAGO, FECHA_PAGO, MONTO, DESCRIPCION, ID_MEDIO_PAGO
            ) VALUES(
                :idP, TO_DATE(:fechaP, 'YYYY-MM-DD'), :montoP, :descriptionP, :idMedioPago
            )
        """
        cursor9.execute(
            sql, 
            idP = data['codigoPago'],
            fechaP = data['datePago'],
            montoP = data['montoPago'],
            descriptionP = data['descripcionPago'],
            idMedioPago = medio_pago_id
        )
        connection.commit()
        cursor9.close()

        cursor11 = connection.cursor()
        sql2 = """
            UPDATE CAY_EVENTO
            SET
                ID_PAGO = :codigoP
            WHERE ID_EVENTO = :eId
        """
        cursor11.execute(
            sql2,
            codigoP = data['codigoPago'],
            eId = evento_Id
        )
        connection.commit()
        cursor11.close()

        return redirect(url_for('tusEventosPage'))
    return render_template('index4.html')

@app.route('/deleteEvent')
def deleteEvent():
    cursor5 = connection.cursor()
    sql = "SELECT * FROM CAY_EVENTO"
    cursor5.execute(sql)
    eventos = cursor5.fetchall()
    cursor5.close()    
    return render_template('index5.html', eventos = eventos)
    
@app.route('/deleteEventId/<idEvento>', methods=['GET', 'POST'])
def deleteEventId(idEvento):
    if request.method == 'GET':
        cursor6 = connection.cursor()
        sql = "SELECT * FROM CAY_EVENTO WHERE ID_EVENTO = :idE"
        cursor6.execute(sql, idE = idEvento)
        evento = cursor6.fetchone()
        print(evento)
        cursor6.close()
        return render_template('index5.html', eventos=[evento])   
         
    elif request.method == 'POST':
        cursor7 = connection.cursor()
        sql2 = "DELETE FROM CAY_EVENTO WHERE ID_EVENTO = :idE"
        cursor7.execute(sql2, idE = idEvento)
        cursor7.close()
        connection.commit()
        
        print(idEvento)
        print("Se ha eliminado el evento")
        return redirect(url_for('tusEventosPage'))

@app.route('/aditionals', methods=['GET', 'POST'])
def aditionals():
    global evento_Id

    if request.method == 'POST':
        data = request.form
        cursor8 = connection.cursor()
        
        suma_cantidades = int(data['cantSillas']) + int(data['cantMesas']) + int(data['cantCarpas']) + int(data['cantParlantes'])

        sql = """
            INSERT INTO CAY_SERVICIO_ADICIONAL(
                ID_SERVICIO_ADICIONAL, TIEMPO, CANTIDAD_MATERIALES
            ) VALUES(
                :idM, :tiempoM, :cantM)
        """
        cursor8.execute(
            sql,
            idM = data['codigoServicio'],
            tiempoM = data['horaServicio'],
            cantM = suma_cantidades
        )
        connection.commit()
        cursor8.close()
        cursor10 = connection.cursor()
        sql2 = """
            UPDATE CAY_EVENTO
            SET
                ID_SERVICIO_ADICIONAL = :codigoS
            WHERE ID_EVENTO = :eId
        """
        cursor10.execute(
            sql2,
            codigoS = data['codigoServicio'],
            eId = evento_Id
        )
        connection.commit()
        cursor10.close()
        return redirect(url_for('medioPago'))
    return render_template('index6.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        cursor11 = connection.cursor()
        sql = "SELECT * FROM CAY_USUARIO"
        cursor11.execute(sql)
        users = cursor11.fetchall()
        print(users)
        for user in users:
            user = list(user)
            if user[1] == data['usuario'] and user[3] == data['contra']:
                cursor11.close()
                return redirect (url_for('home'))
        
        cursor11.close()
        return redirect (url_for('signup'))
        
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.form
        rol_id = 1
        cursor12 = connection.cursor()
        sql = """
            INSERT INTO CAY_USUARIO(
                CORREO, NOMBRE_USUARIO, CONTRASENIA, ID_ROL
            ) VALUES(:correoU, :nombreU, :contraU, :idRol)
        """
        cursor12.execute(
            sql,
            correoU = data['correo'],
            nombreU = data['usuario'],
            contraU = data['contra'],
            idRol = rol_id
            )
        connection.commit()
        cursor12.close()
        return redirect(url_for('login'))
    return render_template('signup.html')

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()