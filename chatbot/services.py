from app.services import BaseServices
from users.models import User
from .models import ChatRoom , ChatRoommessages
from sqlalchemy.orm import Session, joinedload
from openai import OpenAI , APIError , RateLimitError , APIConnectionError
from app.settings import settings
from sqlalchemy import desc

class Chatbot :
    def __init__(self):
        self.client = OpenAI(api_key=settings.API_KEY)

    def get_answer(self, prompt):
        try :
           completion = self.client.chat.completions.create(
           model="gpt-4o-mini",
           messages=[
           {
          "role":"user",
          "content": prompt
           }
           ]
           )
           return completion.choices[0].message.content.strip()
        except (APIError , RateLimitError , APIConnectionError) as e :
            raise e
    

        
class Chatroomservices(BaseServices):
    
    @classmethod
    def create_room_service(cls, db, room_name : str, user : User = None ):

        if user is not None :

           room = ChatRoom.objects.create(db=db , user = user , user_id = user.id , room_name = room_name)
        
        else :
           room = ChatRoom.objects.create(db=db ,room_name = room_name )

        return room
    
    @classmethod
    def get_all_rooms(cls, db : Session , user : User):
        room = ChatRoom.objects.query(db=db).filter_by(user_id = user.id).order_by(desc(ChatRoom.created_at)).all()
        return room
    
    @classmethod
    def create_room_messge(cls, db , message : str , room_id : str , message_from : str) :

        message_model = ChatRoommessages.objects.create(db=db , room_id = room_id , message_from=message_from , message = message )

        return message_model
    
    @classmethod
    def update_room_message_service(cls, db , message_id , **kwargs) :
        message_model : ChatRoommessages = ChatRoommessages.objects.get(db , id = message_id)

        for name , value in kwargs.items() :
            setattr(message_model , name , value)
        
        message_model.save(db=db)

        return message_model
    
    @classmethod
    def update_room_service(cls, db , room_id , **kwargs):

        room : ChatRoom = ChatRoom.objects.get(db=db , id = room_id)

        for name , value in kwargs.items() :
            setattr (room , name , value)

        room.save(db=db)

        return room
    
    @classmethod
    def delete_room_service(cls, db , room_id ) -> None:

        room : ChatRoom = ChatRoom.objects.get(db=db , id=room_id )

        room.delete()

    @classmethod
    def get_room_service(cls, db , room_id ) :

        room : ChatRoom = ChatRoom.objects.get(db=db , id=room_id)

        return room
    
    @classmethod
    def get_messages_in_room(cls, db , room_id):
        messages = ChatRoommessages.objects.query(db = db).filter_by(room_id = room_id).order_by(desc(ChatRoommessages.created_at)).all()

        return messages
    
   

    
    

    



            
    

