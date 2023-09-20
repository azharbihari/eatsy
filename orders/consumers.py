from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from orders.models import Order


class OrderStatusConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.pk = self.scope['url_route']['kwargs']['pk']

        if self.scope['user'].is_authenticated:
            self.user = self.scope['user']
            self.order = await database_sync_to_async(Order.objects.get)(
                pk=self.pk, user=self.user
            )
            self.group_name = f'order_{self.pk}'

            if self.order:
                await self.channel_layer.group_add(
                    self.group_name,
                    self.channel_name
                )

                await self.accept()

                await self.send_json(content={'status': self.order.get_status_display()})
            else:
                self.close()
        else:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def update_order_status(self, event):
        await self.send_json(content={'status': event['status']})
