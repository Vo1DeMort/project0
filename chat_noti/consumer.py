import json
from django.contrib.auth.models import User
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from .models import Room, Message

'''
 Each WebSocket connection established by a user/client is assigned a unique channel name.
 Groups are collections of channel names.
'''

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # self.channel_layer is the instance of channel_layer
       ''' each channel in a Django Channels group can represent a user or a client connection  ''' 
        # ohh, of course this is a method
        # add a channel to the group
        await self.channel_layer.group_add(
            self.room_group_name,
        # channel_name doesn't need to be setup in general, it's handle by django channels based on the routing config
            self.channel_name
        )

        await self.accept()

    async def disconnect(self):
        # remove a channel from the group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        print(data)
        message = data['message']
        username = data['username']
        room = data['room']

        await self.save_message(username, room, message)

        # send a message to all the channels that are part of the specified group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))

    # accessing database
    @sync_to_async
    def save_message(self, username, room, message):
        user = User.objects.get(username=username)
        room = Room.objects.get(slug=room)

        Message.objects.create(user=user, room=room, content=message)

































'''
save the message (data) in the db model which is already created with the form
'''
