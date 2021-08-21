#
# Created by Rui Santos
# Complete project details: http://randomnerdtutorials.com
#

import paho.mqtt.client as mqtt
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("/esp32/temperature")

# The callback for when a PUBLISH message is received from the ESP8266.
def on_message(client, userdata, message):
    #socketio.emi
    #socketio.emit('my variable')
    message_received=str(message.payload.decode("utf-8"))
    print("received message =",message_received)
    
    if message.topic == "/esp32/temperature":
        print("temperature update")
    socketio.emit('temperature', {'data': message_received})
    
    conn=sqlite3.connect('asphalt.db')
    c=conn.cursor()
    
    c.execute("""INSERT INTO temp(temperature,
            currentdate, currentime, device) VALUES((?), date('now'),
            time('now','localtime'), (?))""", (message_received,'esp32') )

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
   # connects to SQLite database. File is named "sensordata.db" without the quotes
   # WARNING: your database file should be in the same directory of the app.py file or have the correct path
   conn=sqlite3.connect('asphalt.db')
   conn.row_factory = dict_factory
   c=conn.cursor()
   c.execute("SELECT * FROM temp ORDER BY id DESC")
   readings = c.fetchall()
   #print(readings)
   return render_template('historic.html', readings=readings)
   
   

   
@socketio.on('my event')
def handle_my_custom_event(json):
    print('received json data here: ' + str(json))

if __name__ == "__main__":
   socketio.run(app, host='0.0.0.0', port=8181, debug=True)
