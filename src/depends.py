import logging
from redis.asyncio import Redis
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from src.config import Config
from src.repository.db import MongoInterface
from src.service.messages import MessageService
from src.service.redis import RedisService


load_dotenv('../.env')

db_client: AsyncIOMotorClient = None

db_service: MessageService = None

redis: Redis = None

redis_service: RedisService = None


def get_db(db_client) -> AsyncIOMotorClient:
    db_name = Config.mongo_settings.get('db_name')
    return db_client[db_name]

def get_message_service():
    return db_service

def get_redis_service():
    return redis_service

async def connect_and_init_redis ():
    global redis, redis_service
    if redis is None:
        try:
            redis = Redis (
                host=Config.redis_settings['host'],
                port=Config.redis_settings['port'],
                db=Config.redis_settings['db'],
                decode_responses=True
            )
            redis_service = RedisService(redis=redis)
            logging.info('Connected to Redis')
        except Exception as e:
            logging.exception('Could not connect to Redis')
            raise
            
            


async def connect_and_init_db():
    global db_client, db_service

    if db_client is None:
        try:
            db_client = AsyncIOMotorClient(
                Config.mongo_settings.get('mongodb_url'),
                maxPoolSize=Config.mongo_settings.get('max_db_conn_count'),
                minPoolSize=Config.mongo_settings.get('min_db_conn_count')
            )

            db = get_db(db_client)
            db_interface = MongoInterface(db)
            db_service = MessageService(db_interface)

            logging.info('Connected to mongo.')
        except Exception as e:
            logging.exception(f'Could not connect to mongo: {e}')
            raise


async def close_redis():
    global redis, redis_service
    if redis is None:
        logging.warning('Redis is None, nothing to close')
        return
    await redis.close()
    redis = None
    redis_service = None
    logging.info('Redis connection closed')

async def close_db_connect():
    global db_service, db_client

    if db_client is None:
        logging.warning('Service is None, nothing to close.')
        return

    db_client.close()
    db_client = None
    db_service = None
    logging.info('Mongo connection closed.')





