import redis.asyncio as redis 
from typing import List, Dict
from src.schema.messages import Message, Response
from datetime import datetime
import json
import logging


class RedisService:
    def __init__(self, redis: redis.Redis) -> None:
        self.redis = redis
    
    
    async def fetch_all(self) -> List[Dict]:
        try:
            keys = await self.redis.keys('*')
            messages = []
            for key in keys:
                message = await self.redis.get(key)
                if message:
                    messages.append(json.loads(message))
                    
            logging.info(f'Fetched all entries from redis')
            messages.sort(key=lambda x: datetime.fromisoformat(x['date_created']))
            return messages
        except Exception as e:
            logging.exception(f'Unable to fetch entries from redis. Code: {e}')
            return
    
    async def erase_all(self) -> None:
        try:
            keys = await self.redis.keys('*')
            if keys:
                await self.redis.delete(*keys)
            logging.info('Erased all entries from redis')
        except Exception as e:
            logging.exception(f'Unable to erase entries from redis. Code: {e}')
            return
            
    
    async def store_all(self, messages: List[Message]) -> None:
        try:
            await self.erase_all()  
            for message in messages:
                message_date_iso: datetime= message['date_created'].isoformat()
                message['date_created'] = message_date_iso
                message_id = f"message:{message['author']}:{message['date_created']}"
                await self.redis.set(message_id, json.dumps(message))
            logging.info('Stored all messages in Redis')
        except Exception as e:
            logging.exception(f'Unable to insert entries into redis. Code: {e}')
            return
                
    
    
    