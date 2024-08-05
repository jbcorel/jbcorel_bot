from abc import ABC, abstractmethod
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from src.schema.messages import Message
from src.common.error import InternalError

class AbstractInterface(ABC):

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


class MongoInterface(AbstractInterface):
    def __init__(self, conn_client: AsyncIOMotorClient) -> None:
        self.conn = conn_client
        self.messages = self.conn['messages']
    
    async def fetch_all(self):
        messages = []
        async for message in self.messages.find():
            message.pop('_id')
            messages.append(message)
        return messages
    
    async def create_one(self, item: dict) -> dict:
        
        await self.messages.insert_one(item.copy())
    
    
    def get_db_client(self):
        return self.conn
    
    
    def close(self):
        if self.conn is not None:
            print('self conn is not none', type(self.conn))
            self.conn.close()
            self.conn = None

            