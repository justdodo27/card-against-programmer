from email import message
import json
from channels.generic.websocket import AsyncWebsocketConsumer


class GameRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_code = self.scope['url_route']['kwargs']['room_code']

        await self.channel_layer.group_add(
            self.room_code,
            self.channel_name
        )
    
        await self.accept()

        await self.channel_layer.group_send(
            self.room_code,
            {
                'type': 'msg',
                'tester': "test msg",
            }
        )

    async def msg(self, event):
        tester = event['tester']

        await self.send(text_data=json.dumps({
            'tester': tester,
        }))

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_code,
            self.channel_name
        )
    
    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.room_code,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message,
        }))