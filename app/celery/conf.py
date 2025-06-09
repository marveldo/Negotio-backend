from app.settings import settings
from celery import Celery
import importlib


importlib.import_module(('app.tokens.models'))
celery = Celery(__name__)


celery.conf.update(
    broker_url = f'redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DATABASE}',
    result_backend =  f'redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DATABASE}',
    task_serializer='json',
    accept_content=['json'],  # Ignore other content
    result_serializer='json'
)

celery.autodiscover_tasks(['chatbot', 'users'])


