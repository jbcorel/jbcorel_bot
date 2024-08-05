from fastapi import APIRouter, Depends, status, Request, BackgroundTasks, Query
from typing import List
import logging
from src.schema.messages import Message, Response
from src.service.messages import MessageService
from src.service.redis import RedisService
from src.depends import get_message_service, get_redis_service
from src.common.error import BaseErrResp

router = APIRouter()


async def store_messages_in_redis(messages):
    redis_service: RedisService = get_redis_service()
    await redis_service.store_all(messages)

async def clear_redis():
    redis_service: RedisService = get_redis_service()
    await redis_service.erase_all()
    


@router.get(
    '/api/v1/messages', 
    response_model= Response,
    description="Листинг всех сообщений", 
    status_code=status.HTTP_200_OK,
)
async def get_messages(
        req: Request,
        background_tasks: BackgroundTasks,
        db_service: MessageService = Depends(get_message_service),
        redis_service: RedisService = Depends(get_redis_service),) -> Response:
        
    messages = await redis_service.fetch_all()
    
    if not messages: 
        
        messages = await db_service.fetch_all()
        
        background_tasks.add_task(store_messages_in_redis, messages)
            
    return Response (
            data=messages,
            status=status.HTTP_200_OK,
            message='Successfully retrieved all messages'
        )
    


@router.post('/api/v1/message',
             response_model=Response,
             status_code=status.HTTP_201_CREATED)
async def post_message(
    message: Message,
    req: Request,
    background_tasks: BackgroundTasks,
    db_service: MessageService = Depends(get_message_service)
    ) -> Response:
    
    background_tasks.add_task(clear_redis)
    
    message = await db_service.create_one(message)
    
    return Response (
            data=message,
            status=status.HTTP_201_CREATED,
            message="Successfully created new message"
        )



