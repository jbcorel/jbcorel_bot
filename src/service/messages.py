from abc import ABC, abstractmethod
from bson.json_util import dumps
import json
import logging
from fastapi import status 
from typing import List
from src.schema.messages import Message
from src.repository.db import AbstractInterface
from src.schema.messages import Response
from src.common.error import InternalError


class AbstractService(ABC):
    
    @abstractmethod
    async def fetch_all():
        pass
    
    
    @abstractmethod
    async def create_one():
        pass 
    
    
    @abstractmethod
    def get_db_client():
        pass
    
    
    @abstractmethod
    async def close():
        pass

class MessageService(AbstractService):
    
    def __init__(self, repo: AbstractInterface) -> None:
        self.repo = repo
    
    
    async def fetch_all(self) -> Response:
        try:
            messages = await self.repo.fetch_all()
        except Exception as e:
            raise InternalError([{'message': 'Failed to retrieve all messages', 'code': e}])
        
        return messages

    
    async def create_one(self, item: Message) -> Response:
        
        try:
            message = item.model_dump()

            await self.repo.create_one(message)

            data_lst = [message] 
            
            return data_lst
        
        except Exception as e:
            logging.error(e)
            raise InternalError([{'message': 'Failed to create message', 'code': str(e)}])
    
    
    def get_db_client(self):
        return self.repo.get_db_client()
    
    def close (self):
        self.repo.close()
    
        
        
    
    