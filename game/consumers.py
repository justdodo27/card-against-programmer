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
        self.room = await self.get_room(self.room_code)
        if self.room is not None:
            await self.accept()
            await self.send(text_data='{"info": "authenticate"}')
        else: 
            await self.close()

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        type = text_data_json["type"]

        if type == "authenticate":
            user_id = text_data_json['user']
            if user := await self.get_user(user_id=user_id):
                self.user = user
                if await self.is_member() or await self.is_creator() or self.room.password is None:
                    if not await self.is_member():
                        await self.add_player()
                    if await self.is_creator():
                        await self.send(text_data='{"creator": true}')
                    
                    await self.channel_layer.group_add(
                        self.room_code,
                        self.channel_name
                    )

                    await self.channel_layer.group_send(
                    self.room_code,
                    {
                        'type': 'refresh',
                        'players': await self.get_players(),
                        'settings': []
                    }
                )
                elif self.room.password is not None:
                    await self.send(text_data='{"info": "password"}')
            else:
                await self.send(text_data='{"error": "Wrong user!"}')
        elif type == "login":
            user = await self.login(text_data_json)
            if user:
                await self.send(text_data='{"info": "user", "id":'+f'{user.id}, "username":"{user.username}"'+"}")
            else:
                await self.send(text_data='{"error": "Wrong password!"}')
        elif type == "logout":
            pass
        elif type == "password" and self.user:
            password = text_data_json['password']
            if self.room.password == password:
                if not await self.add_player():
                    await self.send(text_data='{"info": "full"}')
                await self.channel_layer.group_add(
                    self.room_code,
                    self.channel_name
                )

                await self.send(text_data='{"info": "ok"}')

                await self.channel_layer.group_send(
                    self.room_code,
                    {
                        'type': 'refresh',
                        'players': await self.get_players(),
                        'settings': []
                    }
                )
                
                await self.channel_layer.group_send(
                    self.room_code,
                    {
                        'type': 'chat_msg',
                        'server': True,
                        'message': f"{self.user.username} joined",
                    }
                )
            else: 
                await self.send(text_data='{"error": "Wrong password!"}')
        elif type == "message" and self.user and await self.is_member():
            await self.channel_layer.group_send(
                self.room_code,
                {
                    'type': 'chat_msg',
                    'server': False,
                    'user': self.user.username,
                    'message': text_data_json["message"],
                }
            )
        elif type == "config" and self.user:
            if await self.is_creator() is False:
                await self.send(text_data='{"error": "You are not the game creator!"}')
            else:
                data = {
                    'name': text_data_json['name'], 
                    'password': text_data_json['password']
                }
                await self.update_room(data)
        elif type == "start" and self.user:
            pass
        
    async def chat_msg(self, event):
        message = event['message']
        if event['server']:
            user = 'Server'
        else:
            user = event['user']

        await self.send(text_data=json.dumps({
            'user': user,
            'message': message,
        }))

    async def refresh(self, event):
        players = event['players']

        await self.send(text_data=json.dumps({
            'info': 'refresh',
            'players': players
        }))

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_code,
            self.channel_name
        )
        if self.user and not await self.is_creator() and self.room:
            await self.disconnect_player()

    @database_sync_to_async
    def get_room(self, code):
        if (room := Game.objects.filter(code=code).first()) is None:
            return None
        else:
            return room

    @database_sync_to_async
    def get_user(self, user_id, token=None): # change it later to token authorization etc.
        return Player.objects.filter(id=user_id).first()

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
            return None

    @database_sync_to_async
    def is_creator(self):
        return self.user.id == self.room.creator.id

    @database_sync_to_async
    def is_member(self):
        return self.user in self.room.players.all()

    @database_sync_to_async
    def add_player(self):
        game = Game.objects.filter(pk=self.room.id).first()
        # add players count validation etc.
        game.players.add(self.user)
        return True

    @database_sync_to_async
    def disconnect_player(self):
        self.room.players.remove(self.user)

    @database_sync_to_async
    def get_players(self):
        players = self.room.players.all()
        result = []

        for player in players:
            result.append(player.username)

        return result

    @database_sync_to_async
    def update_room(self, data):
        room = Game.objects.filter(id=self.room.id)
        room.update(name = data['name'])
        room.update(password = data['password'])
        self.room = room.first()