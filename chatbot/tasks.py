from app.celery.conf import celery
import asyncio
import json
from celery import current_task
from .services import Chatbot, Chatroomservices
from .websocket_view import socket_manager
from openai import APIError , APIConnectionError , RateLimitError
from app.db import get_db

async def boradcastfromcelery(channel_name : str , message : str) -> None:
    await socket_manager.redis_manager.connect()
    await socket_manager.redis_manager.broadcast(channel_name=channel_name , message=message)

@celery.task(name='chatbot.tasks.chatwithbot')
def chatwithbot(room_id , prompt) :
    db = next(get_db())
    bot = Chatbot()
    try :
       response = bot.get_answer(prompt=prompt)
       message = Chatroomservices.create_room_messge(db=db , message=response , room_id=room_id , message_from="chatbot")

       data = {
        'status': 'success',
        'message' : response 
        }
    
       serialized_data = json.dumps(data)

       event_loop = asyncio.get_event_loop()

       event_loop.run_until_complete(boradcastfromcelery(channel_name=room_id, message=serialized_data))
    except (APIConnectionError ,APIError ,RateLimitError) as e :
        data = {
            'status' : 'Error',
            'message' : f'Error {e}'
        }
        serialized_data = json.dumps(data)
        event_loop = asyncio.get_event_loop()
        event_loop.run_until_complete(boradcastfromcelery(channel_name=room_id, message=serialized_data))

   