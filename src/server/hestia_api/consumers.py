import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class CommandConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        async_to_sync(self.channel_layer.group_add)('my_group', self.channel_name)
        print(self.channel_layer)
        print(self.channel_name)
        print("connected to my_group")
        self.send(text_data=json.dumps({
            'message': "hello world :3"
        }))
        async_to_sync(self.channel_layer.group_send)(
        'my_group',
        {
            'type': 'from.MQTT',
            'message': "huhhhh"
        }
    )
    def disconnect(self, close_code):
        pass
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print("in receive")
        print(message)
        self.send(text_data=json.dumps({
            'message': message
        }))
    def from_MQTT(self, event):
        print("in mqtt receipt")
        self.send(text_data=json.dumps({"message": event["message"]}))
