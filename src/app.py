from datetime import datetime
from flask import Flask, render_template, request

from conf import config
from conexion_oracle import connection, cursor

app = Flask(__name__, static_folder='static', template_folder='template')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/createEvent', methods = ['GET', 'POST'])
def createEvent():
    if request.method == 'POST':
        data = request.form
        cursor = connection.cursor()

        data = request.form
        
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
            modalEvent = data['modalidadEvento'], 
            clasEvent = data['clasificationEvento'], 
            dateEvent1 = data['date1'], 
            timeEvent1=data['time1'], 
            dateEvent2 = data['date2'], 
            timeEvent2=data['time2']
        )

        connection.commit()
        cursor.close()
    return render_template('index2.html')


@app.route('/tusEventosPage')
def tusEventosPage():
    return render_template('index1.html')

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()
