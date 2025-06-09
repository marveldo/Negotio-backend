from fastapi import APIRouter
from users.views import user_router
from chatbot.views import chat_router
from users.websocket_views import userwebsocketrouter
from chatbot.websocket_view import chatbot_websocket_router

api_main_route = APIRouter(prefix='/api/v1')
websocket_main_route = APIRouter(prefix='/ws')

api_main_route.include_router(user_router)
api_main_route.include_router(chat_router)
websocket_main_route.include_router(userwebsocketrouter)
websocket_main_route.include_router(chatbot_websocket_router)