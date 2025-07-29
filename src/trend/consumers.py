import json

from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        payload = json.loads(text_data)
        content = payload["content"]

        self.send(text_data=json.dumps({"message": content}))
