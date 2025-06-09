from pydantic import BaseModel


class ChatRoommodel (BaseModel):

    room_name : str


class Chatmessage(BaseModel):

    message : str