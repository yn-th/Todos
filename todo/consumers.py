import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        if self.user.is_authenticated:
            # هر کاربر به یک گروه خاص خودش می‌پیوندد
            self.group_name = f'user_{self.user.id}'
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )

    # این متد پیام‌های ارسالی از سرور را دریافت و به WebSocket می‌فرستد
    async def send_notification(self, event):
        await self.send(text_data=json.dumps(event['data']))