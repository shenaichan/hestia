import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class CommandConsumer(WebsocketConsumer):
    
    def connect(self):
        self.accept()
        async_to_sync(self.channel_layer.group_add)('my_group', self.channel_name)
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
        async_to_sync(self.channel_layer.group_discard)('my_group', self.channel_name)

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        self.send(text_data=json.dumps({
            'message': message
        }))

    def from_MQTT(self, event):
        print("in mqtt receipt")
        self.send(text_data=json.dumps({"message": event["message"]}))
