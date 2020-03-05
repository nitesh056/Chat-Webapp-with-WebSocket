from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json
from .models import Message, Room
from django.contrib.auth.models import User

class RoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_id = 'room_id_' + str(self.room_id)

        self.user = self.scope["user"]

        await self.channel_layer.group_add(
            self.room_group_id,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_id,
            self.channel_name
        )

    async def receive(self, text_data):
        js_object_to_dictionary = json.loads(text_data)
        message = js_object_to_dictionary['message']
        await self.store_message(message)

        await self.channel_layer.group_send(
            self.room_group_id,
            {
                'type' : 'room_message',
                'message' : message,
                'sender' : self.user.username
            }
        )

    async def room_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender']
        }))

    @database_sync_to_async
    def store_message(self, message):
        room = Room.objects.get(id=self.room_id)
        Message.objects.create(
            sender=self.user,
            room=room,
            message=message
        )
