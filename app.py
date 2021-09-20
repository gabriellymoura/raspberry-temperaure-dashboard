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
    print("Connected with result code "+str(rc))
    client.subscribe("/esp32/readings")

def on_message(client, userdata, message):
    message_received=str(message.payload.decode("utf-8"))

    if message.topic == "/esp32/readings":
        readings_json = json.loads(message_received)
        print("data recebido: ", readings_json)
        socketio.emit('temperature', {'data': readings_json['temperature']})
        socketio.emit('humidity', {'data': readings_json['humidity']})
        
        today = date.today()
        d1 = today.strftime("%d/%m/%Y")
        now = time.localtime()
        t1 = time.strftime("%H:%M:%S", now)
        
        conn = mariadb.connect(
            user="admin",
            password="admin",
            host="localhost",
            database="PAVIMENTO_UEMA")
        c = conn.cursor() 
  
        c.execute("""INSERT INTO infos_uema(temperature,
                humidity, currentdate, currenttime, device) VALUES((?), (?), (?),
                (?), (?))""", (readings_json['temperature'],readings_json['humidity'], d1, t1, 'PV/ESP/01') )
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
   return render_template('index.html', async_mode=socketio.async_mode)
   
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
   socketio.run(app, host='0.0.0.0', port=8181, debug=True)
