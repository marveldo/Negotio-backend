from fastapi import WebSocket, WebSocketDisconnect , APIRouter
from app.websockets.websocket import WebsocketManager
import json

socket_manager = WebsocketManager()
userwebsocketrouter = APIRouter(prefix='/users')

@userwebsocketrouter.websocket('/test/')
async def user_test_websocket(websocket : WebSocket):
    await socket_manager.connect_user(channel_name='UsersGroup', websocket=websocket)
    message = {
        "type": "notification",
        "message": "New User Joined The socket"
    }
    await socket_manager.broadcast_to_channel(channel_name='UsersGroup', message=json.dumps(message))

    try :
        while True :
            data1 =await  websocket.receive_text()
            data = json.loads(data1)
            message = {
                'type':'chat',
                'message': data 
            }
            await socket_manager.broadcast_to_channel(channel_name='UsersGroup', message=json.dumps(message))

    except WebSocketDisconnect :
        await socket_manager.remove_user_from_room(channel_name='UsersGroup', websocket=websocket)
        message = {
        "type": "notification",
        "message": "New User Left The socket"
         }
        await socket_manager.broadcast_to_channel(channel_name='UsersGroup', message=json.dumps(message))

    except Exception as e :
          await socket_manager.remove_user_from_room(channel_name='UsersGroup', websocket=websocket)
          await websocket.close(code=1088)


@userwebsocketrouter.websocket('/task-result/')
async def task_result_websocket( websocket : WebSocket):
    
    
    await socket_manager.connect_user(channel_name='results', websocket=websocket)

    try :
        text =  await websocket.receive_text()
    
    except WebSocketDisconnect :
        
        await socket_manager.remove_user_from_room(channel_name='results', websocket=websocket)
    
    except Exception as e : 
          
          await socket_manager.remove_user_from_room(channel_name='results', websocket=websocket)
          await websocket.close(code=1088)

    
