from flask import Flask, request
from flask_socketio import SocketIO, send, emit
from flask_cors import CORS

from llm.function_routing import answer_and_execute

import paho.mqtt.client as mqtt


app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Callback when the client connects to the broker
def on_connect(client, userdata, flags, rc, properties):
    print("Connected with result code " + str(rc))
    client.subscribe("commands")
    client.subscribe("responses")

# Callback when a message is received from the broker
def on_message(client, userdata, msg):
    if msg.topic == "commands":
        socketio.emit('command', msg.payload.decode('utf-8'))
    elif msg.topic == "responses":
        socketio.emit('response', msg.payload.decode('utf-8'))

@app.route('/')
def hello():
    print(request.args.get('code'))
    return "Hello, World!"

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('command')
def handle_command(command: str):
    client.publish("commands", command)
    response = answer_and_execute(command)
    client.publish("responses", response)

if __name__ == '__main__':

    # Create an MQTT client instance
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

    # Assign the callback functions
    client.on_connect = on_connect
    client.on_message = on_message

    # Connect to the local broker
    client.connect("10.0.0.244", 1883, 60)

    client.loop_start()

    socketio.run(app, host="0.0.0.0", port="6969", allow_unsafe_werkzeug=True)