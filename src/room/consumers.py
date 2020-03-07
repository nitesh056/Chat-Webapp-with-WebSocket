from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json
from .models import Message, Room, UserJoined
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

        await self.channel_layer.group_send(
            self.room_group_id,
            {
                'type': 'user_joined',
                'user': self.user.username
            }
        )

        # In database
        await self.set_status('ONLINE')

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_send(
            self.room_group_id,
            {
                'type': 'user_left',
                'user': self.user.username
            }
        )

        # In database
        await self.set_status('OFFLINE')

        await self.channel_layer.group_discard(
            self.room_group_id,
            self.channel_name
        )

    async def receive(self, text_data):
        js_object_to_dictionary = json.loads(text_data)
        
        request_type = js_object_to_dictionary['type']
        
        if request_type == 'message':
            message = js_object_to_dictionary['message']
            await self.store_message(message)

            await self.channel_layer.group_send(
                self.room_group_id,
                {
                    'type': 'room_message',
                    'message': message,
                    'sender': self.user.username
                }
            )


    # Send message to client/browser called by channel_layer.group_send
    async def send_message(self, obj):
        await self.send(text_data=json.dumps(obj))

    async def room_message(self, event):
        await self.send_message({
            'type': 'message',
            'message': event['message'],
            'sender': event['sender']
        })

    async def user_joined(self, event):
        await self.send_message({
            'type': 'user_joined',
            'user': event['user']
        })
    
    async def user_left(self, event):
        await self.send_message({
            'type': 'user_left',
            'user': event['user']
        })

    # Storing in Database
    @database_sync_to_async
    def store_message(self, message):
        room = Room.objects.get(id=self.room_id)
        Message.objects.create(
            sender=self.user,
            room=room,
            message=message
        )

    @database_sync_to_async
    def set_status(self, status):
        room = Room.objects.get(id=self.room_id)
        user_status = UserJoined.objects.get(user=self.user, room=room)
        user_status.status = status
        user_status.save()
