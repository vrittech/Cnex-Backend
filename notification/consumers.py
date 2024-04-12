from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
import json

class MyAsyncConsumer(AsyncWebsocketConsumer):
    async def connect(self):
      
        # print(self.scope["user"].is_authenticated, " user" , self.scope["user"])
        # Check if the user is authenticated
        if self.scope["user"].is_authenticated:
            await self.accept()
            print(f"WebSocket connection accepted. Channel name: {self.channel_name}")
            user_group_name = f"user_{self.scope['user'].id}"
            # self.room_group_name, = f"user_{self.scope['user'].id}"
            print("connectetd group name ",user_group_name)
            self.room_group_name = user_group_name

            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            self.accept()
            # json.dumps(message)
            await self.send(text_data=json.dumps({'message':"Congratulation you are connected"}))
        else:
            await self.accept()
            await self.send(text_data=json.dumps({'message':"Sorry you are not authenticated!!!"}))
            await self.close()
            

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        print("receiving handler message.")
        import json
        data = json.loads(text_data)
        message_type = data.get("type")

        if message_type == "chat_message":
            await self.chat_message(data)
        else:
            # Handle other message types if needed
            pass

    async def chat_message(self, event):
        # Handle the chat message
        message = event["payload"]
        
        message = json.dumps(message)
        await self.send(text_data=message)