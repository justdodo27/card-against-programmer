import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from typing import Union, List
import uuid
from .models import Player, Game
from django.utils.crypto import get_random_string

class LobbyConsumer(AsyncWebsocketConsumer):
    '''
    Change authorization to JWT/oauth
    '''
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
                await self.send(text_data='{"error": "Wrong password!"}')
        elif type == "logout":
            pass
        elif type == "create":
            game = await self.create_game(text_data_json)
            if game:
                data = {
                    "code": game.code,
                    "name": game.name,
                    "password": game.password,
                    "creator": game.creator.id,
                    "cards": game.cards
                }
                await self.send(text_data=json.dumps(data))
            else:
                await self.send(text_data='{"error": "Cannot create game!"}')
        elif type == "join":
            pass

    @database_sync_to_async
    def login(self, data):
        username = data['username']
        password = data['password']

        if (user := Player.objects.filter(username=username).first()) is None:
            user = Player.objects.create(username=username, password=password)
            return user
        elif user.password == password:
            return user
        else:
            return False
                
    @database_sync_to_async
    def create_game(self, data):
        user_id = data["user"]
        if (user := Player.objects.filter(id=user_id).first()) is None:
            return False
        game = Game.objects.create(creator=user, code=get_random_string(length=8))
        return game


class GameRoomConsumer(AsyncWebsocketConsumer):
    '''
    Basic wroking schema (TODO)
    1. accept connection
    2. check if user is authenticated
    2.1 if yes go to step 3
    2.2 if not wait for authenticate
    3. ask user for password (if needed) 
    4. join user to group and show him game
    5. if user is creator receive information about updating the room or starting the game
    ... rest of the logic for playing the game after start
    '''

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