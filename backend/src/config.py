import os
import logging
from src.common.error import InternalError

logging.basicConfig(level=logging.INFO)



class Config:
    mongo_settings = {
        # 'db_name': 'tg_test',
        # 'mongodb_url': 'mongodb://localhost:27017',
        # 'max_db_conn_count': 15,
        # 'min_db_conn_count': 7,
        
        'db_name': os.getenv('MONGO_DB'),
        'mongodb_url': os.getenv('MONGO_URL'),
        'max_db_conn_count': os.getenv('MAX_CONNECTIONS_COUNT'),
        'min_db_conn_count': os.getenv('MIN_CONNECTIONS_COUNT'),
    }
    
    redis_settings = {
        'host': os.getenv('REDIS_HOST'),
        'port': os.getenv('REDIS_PORT'),
        'db': os.getenv('REDIS_DB'),
    }


    @classmethod
    def app_settings_validate(cls):
        for k, v in cls.mongo_settings.items():
            if not v:
                logging.error(f'Config variable error. {k} cannot be None')
                raise InternalError([{"message": "Server configure error"}])
            else:
                logging.info(f'Config variable {k} is {v}')
                
        for k, v in cls.redis_settings.items():
            if not v:
                logging.error(f'Config variable error. {k} cannot be None')
                raise InternalError([{"message": "Server configure error"}])
            else:
                logging.info(f'Config variable {k} is {v}')
