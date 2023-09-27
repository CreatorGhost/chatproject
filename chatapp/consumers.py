import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("Connecting...")
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        print(f"Room name: {self.room_name}, Group name: {self.room_group_name}")

        # User authentication
        if self.scope["user"].is_anonymous:
            print("Anonymous user, closing connection...")
            await self.close()
        else:
            # Join room group
            print("Authenticated user, joining room group...")
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        print("Disconnecting, leaving room group...")
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        print(f"Received data: {text_data}")
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
        except json.JSONDecodeError:
            print("Invalid JSON, sending error message...")
            await self.send(text_data=json.dumps({
                'error': 'Invalid JSON'
            }))
        else:
            # Send message to room group
            print("Valid JSON, sending message to room group...")
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender': self.scope["user"].username
                }
            )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        # Send message to WebSocket
        print("Received message from room group, sending to WebSocket...")
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))