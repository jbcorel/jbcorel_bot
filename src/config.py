import os
import logging
from dotenv import load_dotenv
import logging
from src.common.error import InternalError

logging.basicConfig(level=logging.INFO)

load_dotenv('.../.env')


class Config:

    mongo_settings = {
        'db_name': 'tg_test',
        'mongodb_url': 'mongodb://localhost:27017',
        'max_db_conn_count': 15,
        'min_db_conn_count': 7,
    }
    
    redis_settings = {
        'host': 'localhost',
        'port': 6379,
        'db': 1,
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
