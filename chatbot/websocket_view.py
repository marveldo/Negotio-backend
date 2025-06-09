from app.websockets.websocket import WebsocketManager
from fastapi import APIRouter,WebSocket,WebSocketDisconnect
import json
import logging


socket_manager = WebsocketManager()

chatbot_websocket_router = APIRouter(prefix='/chat')



@chatbot_websocket_router.websocket('/{room_id}/')
async def room_websocket(room_id : str ,websocket : WebSocket):

    await socket_manager.connect_user(channel_name=room_id, websocket=websocket)

    try :
        await websocket.receive_text()

    except WebSocketDisconnect :
        logging.info('Task result closed ')
        await socket_manager.remove_user_from_room(channel_name=room_id, websocket=websocket)
    
    except Exception as e : 
          logging.info(f'Task closed duje to {e}')
          await socket_manager.remove_user_from_room(channel_name=room_id, websocket=websocket)
          await websocket.close(code=1088)



