import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from typing import Union, List
import uuid
from .models import Player, Game


class LobbyConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        
        type = text_data_json['type']

        if type == "login":
            user = await self.login(text_data_json)
            if user:
                await self.send(text_data='{"id":'+f'{user.id}, "username":"{user.username}"'+"}")
            elif user == False:
                await self.send(text_data=str(-1))
        elif type == "logout":
            pass

    @database_sync_to_async
    def login(self, data):
        print("XDDDDDD")
        username = data['username']
        password = data['password']

        if (user := Player.objects.filter(username=username).first()) is None:
            user = Player.objects.create(username=username, password=password)
            return user
        elif user.password == password:
            return user
        else:
            return False
                


class GameRoomConsumer(AsyncWebsocketConsumer):
    games = dict()

    async def connect(self):
        self.room_code = self.scope['url_route']['kwargs']['room_code']
        self.user = self.scope["user"]
        self.user_uuid = uuid.uuid4()
        

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