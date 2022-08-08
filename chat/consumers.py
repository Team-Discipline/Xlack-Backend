from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from django.contrib.auth.models import User

from chat.models import Chat
from chat_channel.models import ChatChannel


class ChatConsumer(JsonWebsocketConsumer):
    # TODO: Implement auth jobs for JWT.
    def connect(self):
        self.channel_id = self.scope['url_route']['kwargs']['channel_id']
        print(f'channel_id: {self.channel_id}')
        self.room_group_name = f'chat_{self.channel_id}'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        # Send chat history to user.
        chats = [{'id': chat.id, 'chatter_id': chat.chatter.id, 'message': chat.message} for chat in
                 Chat.objects.filter(channel=self.channel_id)]
        self.send_json(
            chats
        )

    def receive_json(self, content, **kwargs):
        """
        This function JUST receive messages.
        After that, You should send message to group.
        """
        user = User.objects.get(id=3)  # TODO: Fix this 3 to real user id.
        channel = ChatChannel.objects.get(id=self.channel_id)
        chat = Chat(message=content['message'], chatter=user, channel=channel)
        chat.save()

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'speak',
                'user': self.scope['user'].username,
                'message': content['message']
            }
        )

    def speak(self, event):
        """
        This function speaks message to every body in this group.
        """
        self.send_json({
            'user': event['user'],
            'message': event['message']
        })

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            str(code)
        )