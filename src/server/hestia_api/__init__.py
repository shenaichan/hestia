import paho.mqtt.client as mqtt
from hestia_api.consumers import CommandConsumer
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

# ws = CommandConsumer(WebsocketConsumer)
channel_layer = get_channel_layer()

# Callback when the client connects to the broker
def on_connect(client, userdata, flags, rc, properties):
    print("Connected with result code " + str(rc))
    client.subscribe("test/django")

# Callback when a message is received from the broker
def on_message(client, userdata, msg):
    payload = msg.payload.decode('utf-8')
    print(msg.topic + " " + payload)
    print(channel_layer)
    async_to_sync(channel_layer.group_send)(
        'my_group',
        {
            'type': 'from.MQTT',
            'message': payload
        }
    )
    print("sent to my group possibly?")
    # ws.send(text_data={"message": payload})

# try:
# Create an MQTT client instance
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

# Assign the callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to the local broker
client.connect("localhost", 1883, 60)

client.loop_start()

# finally:
#     if client is not None:
#         client.loop_stop()

