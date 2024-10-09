from flask import Flask, request
from flask_socketio import SocketIO
from flask_cors import CORS
from llm.function_routing import answer_and_execute
import paho.mqtt.client as mqtt



app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")



@app.route('/')
def hello():
    # print(request.args.get('code'))
    return "Hello, World!"



@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('command')
def handle_command(command: str):
    mqtt_client.publish("commands", command)
    response = answer_and_execute(command)
    mqtt_client.publish("responses", response)



def mqtt_on_connect(client, userdata, flags, rc, properties):
    print("Connected with result code " + str(rc))
    client.subscribe("commands")
    client.subscribe("responses")

def mqtt_on_message(client, userdata, msg):
    if msg.topic == "commands":
        socketio.emit('command', msg.payload.decode('utf-8'))
    elif msg.topic == "responses":
        socketio.emit('response', msg.payload.decode('utf-8'))

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqtt_client.on_connect = mqtt_on_connect
mqtt_client.on_message = mqtt_on_message
mqtt_client.connect("10.0.0.244", 1883, 60)
mqtt_client.loop_start()



try:
    socketio.run(app, host="0.0.0.0", port="6969", allow_unsafe_werkzeug=True)

except KeyboardInterrupt:
    print("Stopping server")

finally:
    mqtt_client.loop_stop()