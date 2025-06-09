import redis.asyncio as aioredis
from app.settings import settings

class RedisManager :

    def __init__(self, host=settings.REDIS_HOST,
                  port=settings.REDIS_PORT, 
                  password=settings.REDIS_PASSWORD,
                   db = settings.REDIS_DATABASE ):
        
        """Initializing the Redis Connection
        """

        self.redis_host = host
        self.redis_port = port
        self.redis_password = password
        self.redis_db = db
        self.redis_pubsub = None
    
    async def _getredisconnection(self) -> aioredis.Redis:

        """Connecting to the redis Server

        Returns:
            _type_: _description_
        """

        return await aioredis.Redis(host=self.redis_host ,
                                    port=self.redis_port,
                                    db=self.redis_db,
                                    password=self.redis_password
                                    )
    async def connect(self) -> None:
        """Getting the Connection and using pubsub for broadcasting messages
        """
        self.redis_connection = await self._getredisconnection()
        self.redis_pubsub = self.redis_connection.pubsub()

    async def subscribe(self, channel_name : str) -> aioredis.Redis:
        """Subscribing a new Channel into the redis pubsub

        Args:
            channel_name (str): _description_

        Returns:
            aioredis.Redis: _description_
        """
        await self.redis_pubsub.subscribe(channel_name)
        return self.redis_pubsub

    async def unsubscribe(self, channel_name : str) -> None :

        await self.redis_pubsub.unsubscribe(channel_name)



    async def broadcast(self , channel_name:str , message):
        await self.redis_connection.publish(channel_name, message)