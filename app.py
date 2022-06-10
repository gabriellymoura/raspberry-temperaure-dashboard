import paho.mqtt.client as mqtt
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from datetime import datetime
import mariadb
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("PV/ESP32/01")

def on_message(client, userdata, message):
    message_received=str(message.payload.decode("utf-8"))

    if message.topic == "PV/ESP32/01":
        readings_json = json.loads(message_received)
        print(readings_json)

        now = datetime.now()
        date = now.strftime("%d/%m/%Y")
        time = now.strftime("%H:%M:%S")
        print(date,time)
            
        conn = mariadb.connect(
            user="root",
            password="root",
            port=3306,
            database="databaseMain"
            )
        c=conn.cursor()
        c.execute("""INSERT INTO tableMain(temperaturaSolo,
                umidadeSolo,temperaturaAr,umidadeAr,
                currentdate, currenttime, device) VALUES((?),(?),(?),
                (?), (?),(?), (?))""",
                (readings_json['tempSolo'],readings_json['humSolo'],
                readings_json['tempAr'],readings_json['humAr'],
                date, time,readings_json['device']) )
        conn.commit()
        conn.close()
               
mqttc=mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.connect("localhost",1883,60)
mqttc.loop_start()

@app.route("/")
def main():
   # Pass the template data into the template main.html and return it to the user
   conn = mariadb.connect(
            user="root",
            password="root",
            port=3306,
            database="databaseMain")
   

   c=conn.cursor()
   c.execute("SELECT * FROM tableMain ORDER BY id DESC LIMIT 1")
   current = c.fetchall()
   return render_template('index.html', async_mode=socketio.async_mode, current=current)
   
@app.route("/historic")
def historic():
   conn = mariadb.connect(
            user="root",
            password="root",
            port=3306,
            database="databaseMain")
   
   c=conn.cursor()
   c.execute("SELECT * FROM tableMain ORDER BY id DESC")
   readings = c.fetchall()
   return render_template('historic.html', readings=readings)
   
@socketio.on('my event')
def handle_my_custom_event(json):
    print('received json data here: ' + str(json))

if __name__ == "__main__":
   socketio.run(app, host='0.0.0.0', port=8181, debug=True)
