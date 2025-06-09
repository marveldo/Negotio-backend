from fastapi import WebSocket 
from app.redis.conf import RedisManager
import asyncio

class WebsocketManager :

    def __init__(self):
        """Initializing the Websocket Connection and setting up the redis manager
        """
        self.connections : dict = {}
        self.redis_manager = RedisManager()

    async def connect_user(self, channel_name : str, websocket : WebSocket) -> None:
        """Connecting the User to the Websocket

        Args:
            channel_name (str): Channel name to add the user 
            websocket (WebSocket): Websocket Connection of the User
        """
        await websocket.accept()
        if channel_name in self.connections :
            self.connections[channel_name].append(websocket)
        else :
            self.connections[channel_name] = [websocket]
            await self.redis_manager.connect()
            pubsub_subscribed_channel = await self.redis_manager.subscribe(channel_name)
            asyncio.create_task(self.redis_pubsub_reader(pubsub_subscribed_channel))

    async def broadcast_to_channel(self, channel_name : str, message  : str) -> None:
        """Broadcasting messages that are sent in the websocket

        Args:
            channel_name (str): Channel name of the message
            message (str): message that is sent
        """

        await  self.redis_manager.broadcast(channel_name , message)

    async def remove_user_from_room(self, channel_name , websocket : WebSocket):
        """Function to remove a websocket connection from a channel or disconnect a user from a socket channel

        Args:
            channel_name (_type_): Name of channel
            websocket (WebSocket): Socket Connection
        """
        self.connections[channel_name].remove(websocket)
        if len(self.connections[channel_name]) < 1 :
            del self.connections[channel_name] 
            await self.redis_manager.unsubscribe(channel_name)

    async def redis_pubsub_reader(self, pub_sub_channel) :
        """Function To get the messages broadcasted within a channel it constantly runs as long as the 
        user is connected to the socket because of asyncio.create_task

        Args:
            pub_sub_channel (_type_): the redis pubsub object of the subscribed channel
        """
        while True:
             message = await pub_sub_channel.get_message(ignore_subscribe_messages=True)
             if message is not None :
                channel_name = message['channel'].decode('utf-8')
                sockets = self.connections[channel_name]
                for socket in sockets :
                    data = message['data'].decode('utf-8')
                    await socket.send_text(data)

