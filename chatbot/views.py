from fastapi import APIRouter,status, Depends
from sqlalchemy.orm import Session
from users.services import UserService
from users.models import User
from .services import Chatroomservices
from fastapi.encoders import jsonable_encoder
from app.db import get_db
from .schema import Chatmessage , ChatRoommodel
from .tasks import chatwithbot

chat_router = APIRouter(prefix="/chat", tags=['Chat'])


@chat_router.post('/', status_code=status.HTTP_201_CREATED)
async def create_new_chat_room(chatdetails : ChatRoommodel , db : Session = Depends(get_db)) :
    room = Chatroomservices.create_room_service(db=db , room_name=chatdetails.room_name)
    
    return {
        'status' : "Success",
        'obj' : jsonable_encoder(room)
    }

 
@chat_router.get('/{room_id}', status_code=status.HTTP_200_OK)
async def get_chat_room(room_id : str , db : Session = Depends(get_db)):

    room = Chatroomservices.get_messages_in_room(db =db , room_id=room_id)

    return {
        'status' : 'success',
        'obj' : jsonable_encoder(room)
    }

@chat_router.post('/user-owned-room', status_code=status.HTTP_201_CREATED)
async def create_user_chat_room(chatdetails : ChatRoommodel , 
                                db : Session = Depends(get_db), 
                                user : User = Depends(UserService.verify_authenticated_user)):
    
    room = Chatroomservices.create_room_service(db=db , room_name=chatdetails.room_name , user=user)

    return {
        'status' : 'Success',
        'obj' : jsonable_encoder(room)
    }

@chat_router.post('/{id}', status_code=status.HTTP_202_ACCEPTED)
async def chat_in_room(message : Chatmessage,
                        id : str,
                       db : Session = Depends(get_db)
                      ):
    
    chat_message = Chatroomservices.create_room_messge(db, message=message.message , room_id=id, message_from='user')

    task_message = chatwithbot.delay(id,message.message) 

    return {
        'status': 'Success', 
        'obj' : jsonable_encoder(chat_message)
    }    

@chat_router.get('/rooms/', status_code=status.HTTP_200_OK)
async def get_all_user_rooms(
    
                             db : Session = Depends(get_db), 
                             user : User = Depends(UserService.verify_authenticated_user)
                             
                             ):

    rooms = Chatroomservices.get_all_rooms(db = db , user = user)
    return {
        'status' : 'success',
        'obj' : jsonable_encoder(rooms)
    }
  
@chat_router.delete('/{room_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_chat_room(room_id : str, db: Session = Depends(get_db)) :

    Chatroomservices.delete_room_service(db =db , room_id=room_id)

    return {}




