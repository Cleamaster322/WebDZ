import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ProtocolConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "protocols"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name,
        )

    async def protocol_status_changed(self, event):
        await self.send(text_data=json.dumps({
            "type": "protocol_status_changed",
            "protocol": event["protocol"],
        }))