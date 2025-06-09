from app.celery.conf import celery
from celery import current_task
from .websocket_views import socket_manager
import json
import asyncio


async def boradcastfromcelery(channel_name : str , message : str) -> None:
    await socket_manager.redis_manager.connect()
    await socket_manager.redis_manager.broadcast(channel_name=channel_name , message=message)


@celery.task(name='users.tasks.add')
def add(x , y):
    
    task_id = current_task.request.id

    message = {
        'type' : 'task_update',
        'task_id' : str(task_id),
        'result' : x + y
    }
 
    serialized_message = json.dumps(message)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(boradcastfromcelery(channel_name='results', message=serialized_message))
    
    

    
    return x + y