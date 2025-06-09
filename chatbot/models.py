from sqlalchemy import(
    ForeignKey , 
    Column , 
    String,
    Enum
)
import enum

from app.models.BaseModel import BaseModel
from sqlalchemy.orm import relationship

class Messagesenderenum(enum.Enum):
    user = "user"
    chatbot = "chatbot"


class ChatRoom(BaseModel):
    
    __tablename__ = "rooms"

    user_id = Column(String , ForeignKey('users.id'), nullable=True)
    room_name = Column(String , nullable=True)

    user = relationship('User', back_populates="chatroom")
    messages = relationship("ChatRoommessages", back_populates="chatroom", cascade="all, delete")





class ChatRoommessages(BaseModel):

    __tablename__ = "messages"

    room_id = Column(String , ForeignKey("rooms.id"))
    message_from = Column(Enum(Messagesenderenum, name="message_sender"), nullable=False)
    message = Column(String , nullable=False)

    chatroom = relationship("ChatRoom", back_populates="messages")



    

