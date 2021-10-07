import paho.mqtt.client as mqtt
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import mariadb 
import json
from datetime import date
import time


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def on_connect(client, userdata, flags, rc):
    print("Conectado rc = "+str(rc))
    client.subscribe("PV/ESP32/01")
    client.subscribe("PV/ESP32/02")
    client.subscribe("PV/ESP32/03")
    client.subscribe("PV/ESP32/04")
    client.subscribe("PV/ESP32/05")
    
def on_disconnect(client, userdata, rc=0):
    logging.debug("Desconectado rc = "+str(rc))
    client.loop_stop()


def on_message(client, userdata, message):
    message_received=str(message.payload.decode("utf-8"))
    print("recebeu nova mensagem")

    readings_json = json.loads(message_received)        
    socketio.emit('temperature', {'data': readings_json['temperature']})
    socketio.emit('humidity', {'data': readings_json['humidity']})
    
    today = date.today()
    d1 = today.strftime("%d/%m/%Y")
    now = time.localtime()
    t1 = time.strftime("%H:%M:%S", now)
    
    print("mensagem recebida: ", readings_json)
    
    if message.topic == "PV/ESP32/01":
        conn = mariadb.connect(
            user="admin",
            password="admin",
            host="localhost",
            database="PAVIMENTO_UEMA")
        c = conn.cursor() 
        c.execute("""INSERT INTO infos_uema(temperature,
                humidity, currentdate, currenttime, device, device_rpi) VALUES((?), (?), (?),
                (?), (?), (?))""", (readings_json['temperature'],readings_json['humidity'], d1, t1, 'PV/ESP/01', 'PV/RASP/01') )
        conn.commit()
        conn.close()
        
    elif message.topic == "PV/ESP32/02":
        conn = mariadb.connect(
            user="admin",
            password="admin",
            host="localhost",
            database="PAVIMENTO_UEMA")
        c = conn.cursor() 
        c.execute("""INSERT INTO infos_uema(temperature,
                humidity, currentdate, currenttime, device, device_rpi) VALUES((?), (?), (?),
                (?), (?), (?))""", (readings_json['temperature'],readings_json['humidity'], d1, t1, 'PV/ESP/02', 'PV/RASP/01') )
        conn.commit()
        conn.close()
        
    elif message.topic == "PV/ESP32/03":
        conn = mariadb.connect(
            user="admin",
            password="admin",
            host="localhost",
            database="PAVIMENTO_UEMA")
        c = conn.cursor() 
        c.execute("""INSERT INTO infos_uema(temperature,
                humidity, currentdate, currenttime, device, device_rpi) VALUES((?), (?), (?),
                (?), (?), (?))""", (readings_json['temperature'],readings_json['humidity'], d1, t1, 'PV/ESP/03', 'PV/RASP/01') )
        conn.commit()
        conn.close()
        
    elif message.topic == "PV/ESP32/04":
        conn = mariadb.connect(
            user="admin",
            password="admin",
            host="localhost",
            database="PAVIMENTO_UEMA")
        c = conn.cursor() 
        c.execute("""INSERT INTO infos_uema(temperature,
                humidity, currentdate, currenttime, device, device_rpi) VALUES((?), (?), (?),
                (?), (?), (?))""", (readings_json['temperature'],readings_json['humidity'], d1, t1, 'PV/ESP/04', 'PV/RASP/01') )
        conn.commit()
        conn.close()
    
    elif message.topic == "PV/ESP32/05":
        conn = mariadb.connect(
            user="admin",
            password="admin",
            host="localhost",
            database="PAVIMENTO_UEMA")
        c = conn.cursor() 
        c.execute("""INSERT INTO infos_uema(temperature,
                humidity, currentdate, currenttime, device, device_rpi) VALUES((?), (?), (?),
                (?), (?), (?))""", (readings_json['temperature'],readings_json['humidity'], d1, t1, 'PV/ESP/05', 'PV/RASP/01') )
        conn.commit()
        conn.close()
        
        
               
mqttc=mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.connect("localhost",1883,60)
mqttc.loop_start()

@app.route("/")
def main():
   conn = mariadb.connect(
            user="admin",
            password="admin",
            host="localhost",
            database="PAVIMENTO_UEMA")
   c=conn.cursor(dictionary=True)
   c.execute("SELECT * FROM infos_uema ORDER BY id DESC LIMIT 1")
   data = c.fetchall()
   # Pass the template data into the template main.html and return it to the user
   return render_template('index.html', async_mode=socketio.async_mode, data=data)

#SELECT * FROM infos_uema ORDER BY id DESC LIMIT 1

   
@app.route("/historic")
def historic():
    
   conn = mariadb.connect(
            user="admin",
            password="admin",
            host="localhost",
            database="PAVIMENTO_UEMA")
   c=conn.cursor(dictionary=True)
   c.execute("SELECT * FROM infos_uema ORDER BY id DESC")
   readings = c.fetchall()
   #print(readings)
   return render_template('historic.html', readings=readings)
   
@socketio.on('my event')
def handle_my_custom_event(json):
    print('received json data here: ' + str(json))

if __name__ == "__main__":
   socketio.run(app, host='0.0.0.0', port=8181, debug=False)
